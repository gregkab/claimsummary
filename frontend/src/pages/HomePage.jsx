import React, { useState, useEffect } from 'react';
import { fetchClaims } from '../api/api';
import Layout from '../components/Layout';
import ClaimCard from '../components/ClaimCard';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

const HomePage = () => {
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const loadClaims = async (query = '') => {
    setLoading(true);
    setError(null);
    
    try {
      const searchParams = {};
      if (query) {
        searchParams.search = query;
      }
      
      const data = await fetchClaims(searchParams);
      setClaims(data);
    } catch (err) {
      console.error('Error fetching claims:', err);
      setError('Failed to load claims. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadClaims();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    loadClaims(searchQuery);
  };

  return (
    <Layout>
      <div className="pb-5 border-b border-gray-200 sm:flex sm:items-center sm:justify-between">
        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">Claims</h2>
        <div className="mt-3 sm:mt-0 sm:ml-4">
          <form onSubmit={handleSearch} className="flex rounded-md shadow-sm">
            <input
              type="text"
              name="search"
              id="search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full rounded-md sm:text-sm border-gray-300"
              placeholder="Search claims..."
            />
            <button
              type="submit"
              className="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Search
            </button>
          </form>
        </div>
      </div>

      {loading ? (
        <LoadingState message="Loading claims..." />
      ) : error ? (
        <ErrorState message={error} onRetry={() => loadClaims(searchQuery)} />
      ) : (
        <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {claims.length > 0 ? (
            claims.map((claim) => (
              <ClaimCard key={claim.id} claim={claim} />
            ))
          ) : (
            <div className="sm:col-span-3 bg-white shadow rounded-lg p-6 text-center">
              <p className="text-gray-500">No claims found. Try a different search query.</p>
            </div>
          )}
        </div>
      )}
    </Layout>
  );
};

export default HomePage; 