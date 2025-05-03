import React from 'react';
import { Link } from 'react-router-dom';

const ClaimCard = ({ claim }) => {
  return (
    <Link 
      to={`/claims/${claim.id}`}
      className="block rounded-lg shadow bg-white p-6 hover:shadow-md transition-shadow"
    >
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">Claim #{claim.claim_number}</h3>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          claim.status === 'open' ? 'bg-green-100 text-green-800' : 
          claim.status === 'closed' ? 'bg-gray-100 text-gray-800' : 
          'bg-yellow-100 text-yellow-800'
        }`}>
          {claim.status.toUpperCase()}
        </span>
      </div>
      
      <div className="mt-2 flex flex-col space-y-1">
        <p className="text-sm text-gray-600">External ID: {claim.external_id || 'N/A'}</p>
        <p className="text-sm text-gray-600">Company: {claim.company}</p>
      </div>
      
      <div className="mt-4 text-sm text-indigo-600">
        View details →
      </div>
    </Link>
  );
};

export default ClaimCard; 