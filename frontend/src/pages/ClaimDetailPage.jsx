import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchClaimDetails, fetchActionItems } from '../api/api';
import Layout from '../components/Layout';
import ActionItemsTable from '../components/ActionItemsTable';
import EmailSubmissionForm from '../components/EmailSubmissionForm';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

const ClaimDetailPage = () => {
  const { id } = useParams();
  const [claim, setClaim] = useState(null);
  const [actionItems, setActionItems] = useState([]);
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadClaimData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch claim details
      const claimData = await fetchClaimDetails(id);
      setClaim(claimData);
      
      // Fetch action items
      const actionItemsData = await fetchActionItems(id);
      setActionItems(actionItemsData);
      
      // Emails would be part of the claim details in a real implementation
      if (claimData.email_threads) {
        setEmails(claimData.email_threads);
      }
    } catch (err) {
      console.error('Error fetching claim data:', err);
      setError('Failed to load claim details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      loadClaimData();
    }
  }, [id]);

  const handleActionItemUpdate = (updatedItem) => {
    setActionItems(prevItems => 
      prevItems.map(item => 
        item.id === updatedItem.id ? updatedItem : item
      )
    );
  };

  const handleEmailProcessed = (result) => {
    // Update action items with new ones from email processing
    if (result.action_items) {
      setActionItems(prevItems => [...result.action_items, ...prevItems]);
    }
    
    // Add the new email to the list
    if (result.email_thread) {
      setEmails(prevEmails => [result.email_thread, ...prevEmails]);
    }
  };

  if (loading) return (
    <Layout>
      <LoadingState message="Loading claim details..." />
    </Layout>
  );

  if (error) return (
    <Layout>
      <div className="flex items-center mb-4">
        <Link to="/" className="text-indigo-600 hover:text-indigo-900">
          &larr; Back to Claims
        </Link>
      </div>
      <ErrorState message={error} onRetry={loadClaimData} />
    </Layout>
  );

  if (!claim) return (
    <Layout>
      <div className="bg-white shadow sm:rounded-lg p-6">
        <p className="text-gray-500">Claim not found.</p>
        <Link to="/" className="mt-4 text-indigo-600 hover:text-indigo-900">
          Back to Claims
        </Link>
      </div>
    </Layout>
  );

  return (
    <Layout>
      <div className="flex items-center mb-4">
        <Link to="/" className="text-indigo-600 hover:text-indigo-900">
          &larr; Back to Claims
        </Link>
      </div>
      
      <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
        <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Claim #{claim.claim_number}
            </h2>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              {claim.external_id ? `External ID: ${claim.external_id}` : 'No external ID'}
            </p>
          </div>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            claim.status === 'open' ? 'bg-green-100 text-green-800' : 
            claim.status === 'closed' ? 'bg-gray-100 text-gray-800' : 
            'bg-yellow-100 text-yellow-800'
          }`}>
            {claim.status.toUpperCase()}
          </span>
        </div>
        <div className="border-t border-gray-200">
          <dl>
            <div className="bg-gray-50 px-4 py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Company</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{claim.company}</dd>
            </div>
            <div className="bg-white px-4 py-4 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">Created At</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {new Date(claim.created_at).toLocaleString()}
              </dd>
            </div>
          </dl>
        </div>
      </div>
      
      {/* Recent Emails */}
      {emails.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Emails</h3>
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            {emails.slice(0, 3).map((email) => (
              <div key={email.id} className="px-4 py-5 border-b border-gray-200 last:border-b-0">
                <p className="text-sm font-medium text-gray-900">{email.subject}</p>
                <p className="mt-1 text-xs text-gray-500">
                  {new Date(email.timestamp).toLocaleString()}
                </p>
                <div className="mt-2 text-sm text-gray-700 line-clamp-3">
                  {email.clean_body}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Action Items */}
      <div className="mb-6">
        <ActionItemsTable 
          actionItems={actionItems}
          onActionItemUpdate={handleActionItemUpdate}
        />
      </div>
      
      {/* Email Submission Form */}
      <EmailSubmissionForm 
        claimId={id}
        onEmailProcessed={handleEmailProcessed}
      />
    </Layout>
  );
};

export default ClaimDetailPage; 