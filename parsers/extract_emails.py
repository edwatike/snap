import re
import requests

def extract_emails_from_site(url: str) -> list:
    try:
        r = requests.get(url, timeout=10)
        found = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", r.text)
        return list(set(found))
    except:
        return [] 