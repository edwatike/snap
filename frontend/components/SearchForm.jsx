import React, { useState } from 'react';

const SearchForm = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await onSearch({ query, category });
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label 
            htmlFor="query" 
            className="block text-sm font-medium text-gray-700"
          >
            Поисковый запрос
          </label>
          <input
            type="text"
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            placeholder="Например: поставщики мебели"
            required
          />
        </div>

        <div>
          <label 
            htmlFor="category" 
            className="block text-sm font-medium text-gray-700"
          >
            Категория
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          >
            <option value="">Все категории</option>
            <option value="furniture">Мебель</option>
            <option value="electronics">Электроника</option>
            <option value="clothing">Одежда</option>
            <option value="food">Продукты питания</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
            loading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Поиск...' : 'Найти поставщиков'}
        </button>
      </form>
    </div>
  );
};

export default SearchForm; 