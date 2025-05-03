import React, { useState } from 'react';
import { submitEmail } from '../api/api';

const EmailSubmissionForm = ({ claimId, onEmailProcessed }) => {
  const [emailContent, setEmailContent] = useState('');
  const [subject, setSubject] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!emailContent) {
      setError('Email content is required');
      return;
    }

    setIsSubmitting(true);
    setError(null);
    
    try {
      const result = await submitEmail(claimId, {
        subject,
        raw_body: emailContent,
      });
      
      setEmailContent('');
      setSubject('');
      
      if (onEmailProcessed) {
        onEmailProcessed(result);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process email');
      console.error('Error submitting email:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white shadow sm:rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Submit New Email</h3>
      
      {error && (
        <div className="mb-4 bg-red-50 p-4 rounded-md">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="subject" className="block text-sm font-medium text-gray-700">Subject</label>
          <input
            type="text"
            id="subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="Email Subject"
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="email-content" className="block text-sm font-medium text-gray-700">Email Content</label>
          <textarea
            id="email-content"
            rows={6}
            value={emailContent}
            onChange={(e) => setEmailContent(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="Paste the forwarded email here..."
          />
          <p className="mt-1 text-xs text-gray-500">
            Paste the entire forwarded email, including headers and signature.
          </p>
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
              isSubmitting ? 'opacity-75 cursor-not-allowed' : ''
            }`}
          >
            {isSubmitting ? 'Processing...' : 'Process Email'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default EmailSubmissionForm; 