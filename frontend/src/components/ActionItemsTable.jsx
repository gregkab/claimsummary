import React, { useState } from 'react';
import { updateActionItem } from '../api/api';

const ActionItemsTable = ({ actionItems, onActionItemUpdate }) => {
  const [filter, setFilter] = useState('all'); // 'all', 'pending', 'completed'

  const filteredItems = actionItems.filter(item => {
    if (filter === 'all') return true;
    if (filter === 'pending') return item.status !== 'completed';
    if (filter === 'completed') return item.status === 'completed';
    return true;
  });

  const handleStatusChange = async (actionItem) => {
    try {
      const newStatus = actionItem.status === 'completed' ? 'pending' : 'completed';
      const updatedItem = await updateActionItem(actionItem.id, { 
        status: newStatus,
        completed_at: newStatus === 'completed' ? new Date().toISOString() : null
      });
      
      if (onActionItemUpdate) {
        onActionItemUpdate(updatedItem);
      }
    } catch (error) {
      console.error('Error updating action item:', error);
    }
  };

  return (
    <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
      <div className="p-4 bg-white border-b border-gray-200">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">Action Items</h2>
          <div className="flex space-x-2">
            <button
              className={`px-3 py-1 text-sm rounded-md ${filter === 'all' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-600 hover:bg-gray-100'}`}
              onClick={() => setFilter('all')}
            >
              All
            </button>
            <button
              className={`px-3 py-1 text-sm rounded-md ${filter === 'pending' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-600 hover:bg-gray-100'}`}
              onClick={() => setFilter('pending')}
            >
              Pending
            </button>
            <button
              className={`px-3 py-1 text-sm rounded-md ${filter === 'completed' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-600 hover:bg-gray-100'}`}
              onClick={() => setFilter('completed')}
            >
              Completed
            </button>
          </div>
        </div>
      </div>
      
      <table className="min-w-full divide-y divide-gray-300">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">Description</th>
            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Assignee</th>
            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Due Date</th>
            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Confidence</th>
            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Status</th>
            <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
              <span className="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 bg-white">
          {filteredItems.length > 0 ? (
            filteredItems.map((item) => (
              <tr key={item.id}>
                <td className="whitespace-normal py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">{item.description}</td>
                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{item.assignee || 'Unassigned'}</td>
                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                  {item.due_date ? new Date(item.due_date).toLocaleDateString() : 'No date'}
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                  {item.confidence ? `${Math.round(item.confidence * 100)}%` : 'N/A'}
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    item.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {item.status.toUpperCase()}
                  </span>
                </td>
                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                  <button
                    onClick={() => handleStatusChange(item)}
                    className="text-indigo-600 hover:text-indigo-900"
                  >
                    {item.status === 'completed' ? 'Mark as Pending' : 'Mark as Completed'}
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" className="py-6 text-center text-sm text-gray-500">
                No action items found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ActionItemsTable; 