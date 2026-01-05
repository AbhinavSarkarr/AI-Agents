import React, { useState, useEffect } from 'react';
import { 
  Grid, 
  Card, 
  CardContent, 
  CardActions,
  Typography, 
  Box,
  CircularProgress,
  Alert,
  Button,
  IconButton,
  Chip
} from '@mui/material';
import { 
  PlayArrow as PlayIcon, 
  Stop as StopIcon,
  Refresh as RefreshIcon 
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';

// API functions
const fetchAccounts = async () => {
  const response = await fetch('/api/accounts/');
  if (!response.ok) {
    throw new Error('Failed to fetch accounts');
  }
  return response.json();
};

const fetchAgentsStatus = async () => {
  const response = await fetch('/api/agents/status');
  if (!response.ok) {
    throw new Error('Failed to fetch agents status');
  }
  return response.json();
};

const startAllAgents = async () => {
  const response = await fetch('/api/agents/start-all', { method: 'POST' });
  if (!response.ok) {
    throw new Error('Failed to start agents');
  }
  return response.json();
};

const stopAllAgents = async () => {
  const response = await fetch('/api/agents/stop-all', { method: 'POST' });
  if (!response.ok) {
    throw new Error('Failed to stop agents');
  }
  return response.json();
};

const startAgent = async (accountName: string) => {
  const response = await fetch(`/api/agents/${accountName}/start`, { method: 'POST' });
  if (!response.ok) {
    throw new Error('Failed to start agent');
  }
  return response.json();
};

const stopAgent = async (accountName: string) => {
  const response = await fetch(`/api/agents/${accountName}/stop`, { method: 'POST' });
  if (!response.ok) {
    throw new Error('Failed to stop agent');
  }
  return response.json();
};

const Dashboard: React.FC = () => {
  const queryClient = useQueryClient();
  
  // Fetch accounts data
  const { data: accounts, isLoading, error } = useQuery({
    queryKey: ['accounts'],
    queryFn: fetchAccounts,
    refetchInterval: 3000, // Refresh every 3 seconds
  });

  // Fetch agents status
  const { data: agentsStatus } = useQuery({
    queryKey: ['agentsStatus'],
    queryFn: fetchAgentsStatus,
    refetchInterval: 2000, // Refresh every 2 seconds
  });

  // Mutations for agent control
  const startAllMutation = useMutation({
    mutationFn: startAllAgents,
    onSuccess: (data) => {
      toast.success(data.message || 'All agents started');
      queryClient.invalidateQueries({ queryKey: ['agentsStatus'] });
    },
    onError: () => {
      toast.error('Failed to start agents');
    }
  });

  const stopAllMutation = useMutation({
    mutationFn: stopAllAgents,
    onSuccess: (data) => {
      toast.success(data.message || 'All agents stopped');
      queryClient.invalidateQueries({ queryKey: ['agentsStatus'] });
    },
    onError: () => {
      toast.error('Failed to stop agents');
    }
  });

  const startAgentMutation = useMutation({
    mutationFn: startAgent,
    onSuccess: (data) => {
      toast.success(data.message);
      queryClient.invalidateQueries({ queryKey: ['agentsStatus'] });
    },
    onError: () => {
      toast.error('Failed to start agent');
    }
  });

  const stopAgentMutation = useMutation({
    mutationFn: stopAgent,
    onSuccess: (data) => {
      toast.success(data.message);
      queryClient.invalidateQueries({ queryKey: ['agentsStatus'] });
    },
    onError: () => {
      toast.error('Failed to stop agent');
    }
  });

  const isAgentActive = (accountName: string) => {
    return agentsStatus?.agents?.[accountName]?.is_active || false;
  };

  const getAgentMode = (accountName: string) => {
    return agentsStatus?.agents?.[accountName]?.mode || 'idle';
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        Failed to load accounts: {(error as Error).message}
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Trading Dashboard
        </Typography>
        
        <Box display="flex" gap={2}>
          <Button
            variant="contained"
            color="success"
            startIcon={<PlayIcon />}
            onClick={() => startAllMutation.mutate()}
            disabled={agentsStatus?.is_running}
          >
            Start All Traders
          </Button>
          <Button
            variant="contained"
            color="error"
            startIcon={<StopIcon />}
            onClick={() => stopAllMutation.mutate()}
            disabled={!agentsStatus?.is_running}
          >
            Stop All Traders
          </Button>
        </Box>
      </Box>

      {agentsStatus?.is_running && (
        <Alert severity="info" sx={{ mb: 2 }}>
          Trading system is active. Agents are executing trades every minute.
        </Alert>
      )}
      
      <Grid container spacing={3}>
        {accounts?.map((account: any) => (
          <Grid item xs={12} sm={6} md={3} key={account.name}>
            <Card sx={{ position: 'relative' }}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="h6" component="div">
                    {account.display_name}
                  </Typography>
                  <Chip 
                    label={isAgentActive(account.name) ? getAgentMode(account.name) : 'idle'}
                    color={isAgentActive(account.name) ? 'success' : 'default'}
                    size="small"
                  />
                </Box>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="h4" color="primary">
                    ${account.total_portfolio_value.toLocaleString()}
                  </Typography>
                  <Typography 
                    variant="body2" 
                    color={account.total_profit_loss >= 0 ? 'success.main' : 'error.main'}
                  >
                    {account.total_profit_loss >= 0 ? '+' : ''}${account.total_profit_loss.toLocaleString()}
                  </Typography>
                </Box>
                
                <Typography variant="body2" color="text.secondary">
                  Cash: ${account.balance.toLocaleString()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Holdings: {Object.keys(account.holdings || {}).length} positions
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Win Rate: {(account.win_rate * 100).toFixed(1)}%
                </Typography>
              </CardContent>
              
              <CardActions>
                <Button
                  size="small"
                  variant={isAgentActive(account.name) ? 'outlined' : 'contained'}
                  color={isAgentActive(account.name) ? 'error' : 'primary'}
                  startIcon={isAgentActive(account.name) ? <StopIcon /> : <PlayIcon />}
                  onClick={() => {
                    if (isAgentActive(account.name)) {
                      stopAgentMutation.mutate(account.name);
                    } else {
                      startAgentMutation.mutate(account.name);
                    }
                  }}
                  fullWidth
                >
                  {isAgentActive(account.name) ? 'Stop Trading' : 'Start Trading'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {(!accounts || accounts.length === 0) && (
        <Alert severity="info" sx={{ mt: 2 }}>
          No trading accounts found. Initialize the system to create default accounts.
        </Alert>
      )}
    </Box>
  );
};

export default Dashboard;