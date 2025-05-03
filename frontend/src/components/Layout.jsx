import React from 'react';
import { Link } from 'react-router-dom';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <Link to="/">
            <h1 className="text-2xl font-bold text-indigo-600">Claim Action Intelligence</h1>
          </Link>
          <nav>
            <ul className="flex space-x-4">
              <li>
                <Link to="/" className="text-gray-600 hover:text-indigo-600">Home</Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
};

export default Layout; 