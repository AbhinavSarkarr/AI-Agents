import React from 'react';
import { Typography, Box } from '@mui/material';

const AccountPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Account Details
      </Typography>
      <Typography variant="body1">
        Individual account page - to be implemented with detailed portfolio view, 
        transaction history, performance charts, and trading controls.
      </Typography>
    </Box>
  );
};

export default AccountPage;