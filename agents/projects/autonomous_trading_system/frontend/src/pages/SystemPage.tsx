import React from 'react';
import { Typography, Box } from '@mui/material';

const SystemPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        System Management
      </Typography>
      <Typography variant="body1">
        System administration page - to be implemented with system status,
        configuration management, database controls, and health monitoring.
      </Typography>
    </Box>
  );
};

export default SystemPage;