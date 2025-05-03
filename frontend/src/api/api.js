import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchClaims = async (searchParams) => {
  const response = await api.get('/api/claims/', { params: searchParams });
  return response.data;
};

export const fetchClaimDetails = async (claimId) => {
  const response = await api.get(`/api/claims/${claimId}`);
  return response.data;
};

export const fetchActionItems = async (claimId) => {
  const response = await api.get(`/api/claims/${claimId}/action-items/`);
  return response.data;
};

export const updateActionItem = async (actionItemId, data) => {
  const response = await api.patch(`/api/action-items/${actionItemId}`, data);
  return response.data;
};

export const submitEmail = async (claimId, emailData) => {
  const response = await api.post('/api/summarize/', {
    claim_id: claimId,
    ...emailData,
  });
  return response.data;
};

export default api; 