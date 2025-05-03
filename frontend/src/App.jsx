import React from 'react';
import { BrowserRouter as Router, Routes, Route, createRoutesFromElements, createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ClaimDetailPage from './pages/ClaimDetailPage';
import './index.css';

function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<HomePage />} />
        <Route path="/claims/:id" element={<ClaimDetailPage />} />
      </>
    ),
    {
      future: {
        v7_startTransition: true,
        v7_relativeSplatPath: true
      }
    }
  );

  return <RouterProvider router={router} />;
}

export default App; 