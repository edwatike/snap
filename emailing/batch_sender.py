import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import asyncio
import aiosmtplib
from jinja2 import Environment, FileSystemLoader
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EmailBatchSender:
    def __init__(
        self,
        smtp_configs: List[Dict],
        batch_size: int = 25,
        rate_limit: int = 100,  # emails per hour
        template_dir: str = "emailing/templates"
    ):
        self.smtp_configs = smtp_configs
        self.batch_size = batch_size
        self.rate_limit = rate_limit
        self.current_smtp_index = 0
        self.sent_count = 0
        self.last_reset = datetime.now()
        
        # Настройка Jinja2
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
        
    def _get_next_smtp_config(self) -> Dict:
        """Ротация SMTP-серверов"""
        config = self.smtp_configs[self.current_smtp_index]
        self.current_smtp_index = (self.current_smtp_index + 1) % len(self.smtp_configs)
        return config
    
    def _check_rate_limit(self):
        """Проверка ограничения количества писем"""
        now = datetime.now()
        if (now - self.last_reset) > timedelta(hours=1):
            self.sent_count = 0
            self.last_reset = now
            
        if self.sent_count >= self.rate_limit:
            wait_time = 3600 - (now - self.last_reset).seconds
            raise Exception(f"Rate limit reached. Wait {wait_time} seconds")
    
    async def send_batch(
        self,
        recipients: List[Dict],
        template_name: str,
        subject: str,
        campaign_id: str = None
    ) -> List[Dict]:
        """
        Отправка пакета писем с использованием шаблона
        
        recipients: [{"email": "...", "name": "...", "company": "...", ...}]
        """
        results = []
        template = self.jinja_env.get_template(template_name)
        
        # Разбиваем на пакеты
        for i in range(0, len(recipients), self.batch_size):
            batch = recipients[i:i + self.batch_size]
            
            # Проверяем лимиты
            self._check_rate_limit()
            
            # Получаем конфигурацию SMTP
            smtp_config = self._get_next_smtp_config()
            
            try:
                async with aiosmtplib.SMTP(
                    hostname=smtp_config['host'],
                    port=smtp_config['port'],
                    use_tls=True
                ) as smtp:
                    await smtp.login(smtp_config['username'], smtp_config['password'])
                    
                    for recipient in batch:
                        try:
                            # Формируем письмо
                            msg = MIMEMultipart()
                            msg['From'] = smtp_config['from_email']
                            msg['To'] = recipient['email']
                            msg['Subject'] = subject
                            
                            # Рендерим шаблон
                            html = template.render(**recipient)
                            msg.attach(MIMEText(html, 'html'))
                            
                            # Отправляем
                            await smtp.send_message(msg)
                            
                            results.append({
                                'email': recipient['email'],
                                'status': 'sent',
                                'campaign_id': campaign_id,
                                'sent_at': datetime.now().isoformat()
                            })
                            
                            self.sent_count += 1
                            
                        except Exception as e:
                            logger.error(f"Error sending to {recipient['email']}: {e}")
                            results.append({
                                'email': recipient['email'],
                                'status': 'failed',
                                'error': str(e),
                                'campaign_id': campaign_id
                            })
                            
                        await asyncio.sleep(1)  # Небольшая пауза между письмами
                        
            except Exception as e:
                logger.error(f"SMTP error with config {smtp_config['host']}: {e}")
                # Помечаем все письма в батче как failed
                results.extend([
                    {
                        'email': r['email'],
                        'status': 'failed',
                        'error': str(e),
                        'campaign_id': campaign_id
                    } for r in batch
                ])
                
            await asyncio.sleep(5)  # Пауза между батчами
            
        return results 