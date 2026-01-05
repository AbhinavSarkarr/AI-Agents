import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Container } from '@mui/material';

import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import AccountPage from './pages/AccountPage';
import MarketPage from './pages/MarketPage';
import SystemPage from './pages/SystemPage';

function App() {
  return (
    <div className="App">
      <Header />
      <Container maxWidth="xl" sx={{ mt: 2, mb: 2 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/account/:accountName" element={<AccountPage />} />
          <Route path="/market" element={<MarketPage />} />
          <Route path="/system" element={<SystemPage />} />
        </Routes>
      </Container>
    </div>
  );
}

export default App;