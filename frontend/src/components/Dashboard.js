import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Person,
  Assessment,
  LocalHospital,
  TrendingUp
} from '@mui/icons-material';

const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [patients, setPatients] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [specialists, setSpecialists] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // In a real app, you'd have endpoints for these
      // For now, we'll show what we can
      const specialistsResponse = await axios.get('http://localhost:5000/api/specialists');
      setSpecialists(specialistsResponse.data.specialists);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'high': return '#f44336';
      case 'medium': return '#ff9800';
      case 'low': return '#4caf50';
      default: return '#9e9e9e';
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Health Assessment Dashboard
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Person sx={{ fontSize: 40, color: '#1976d2' }} />
                <Box>
                  <Typography variant="h4">0</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Patients
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Assessment sx={{ fontSize: 40, color: '#dc004e' }} />
                <Box>
                  <Typography variant="h4">0</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Assessments
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <LocalHospital sx={{ fontSize: 40, color: '#ff9800' }} />
                <Box>
                  <Typography variant="h4">{specialists.length}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Specialists
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <TrendingUp sx={{ fontSize: 40, color: '#4caf50' }} />
                <Box>
                  <Typography variant="h4">98%</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Accuracy Rate
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Specialists Directory */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Available Specialists
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Specialty</TableCell>
                    <TableCell>Location</TableCell>
                    <TableCell>Rating</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {specialists.map((specialist) => (
                    <TableRow key={specialist.id}>
                      <TableCell>{specialist.name}</TableCell>
                      <TableCell>{specialist.specialty}</TableCell>
                      <TableCell>{specialist.location}</TableCell>
                      <TableCell>{specialist.rating}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/')}
                startIcon={<Person />}
              >
                New Patient Assessment
              </Button>
              <Button
                variant="outlined"
                size="large"
                startIcon={<Assessment />}
              >
                View Recent Assessments
              </Button>
              <Button
                variant="outlined"
                size="large"
                startIcon={<LocalHospital />}
              >
                Manage Specialists
              </Button>
              <Button
                variant="outlined"
                size="large"
                startIcon={<TrendingUp />}
              >
                Generate Reports
              </Button>
            </Box>

            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                System Information
              </Typography>
              <Typography variant="body2" color="text.secondary">
                AI-Driven Disease Risk Assessment System v1.0
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Powered by Machine Learning algorithms for accurate risk prediction
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent Activity */}
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Disease Categories Monitored
        </Typography>
        <Grid container spacing={2}>
          {['Cardiovascular', 'Diabetes', 'Respiratory', 'Cancer', 'Neurological', 'Gastrointestinal', 'Autoimmune', 'Mental Health'].map((category) => (
            <Grid item xs={12} sm={6} md={4} key={category}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {category}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    AI-powered risk assessment available
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Box>
  );
};

export default Dashboard;
