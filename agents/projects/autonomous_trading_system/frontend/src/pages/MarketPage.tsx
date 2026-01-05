import React from 'react';
import { Typography, Box } from '@mui/material';

const MarketPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Market Data
      </Typography>
      <Typography variant="body1">
        Market overview page - to be implemented with market status,
        stock prices, market summary, and data source information.
      </Typography>
    </Box>
  );
};

export default MarketPage;