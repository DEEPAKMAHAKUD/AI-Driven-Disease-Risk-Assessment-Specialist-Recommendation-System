import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  CircularProgress,
  Chip,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  Avatar
} from '@mui/material';
import {
  LocalHospital,
  Warning,
  CheckCircle,
  Info,
  Person,
  Star
} from '@mui/icons-material';

const Results = () => {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetchResults();
  }, [assessmentId]);

  const fetchResults = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/assessments/${assessmentId}`);
      setResults(response.data);
    } catch (err) {
      setError('Failed to load assessment results');
      console.error('Error fetching results:', err);
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

  const getRiskIcon = (level) => {
    switch (level) {
      case 'high': return <Warning sx={{ color: getRiskColor('high') }} />;
      case 'medium': return <Info sx={{ color: getRiskColor('medium') }} />;
      case 'low': return <CheckCircle sx={{ color: getRiskColor('low') }} />;
      default: return <Info />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'error';
      case 'routine': return 'warning';
      case 'lifestyle': return 'info';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!results) {
    return <Alert severity="info">No results available</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom align="center">
        Health Risk Assessment Results
      </Typography>

      {/* Overall Risk Summary */}
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Overall Health Risk
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {getRiskIcon(results.risk_results?.overall_risk?.level)}
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" sx={{ color: getRiskColor(results.risk_results?.overall_risk?.level) }}>
              {results.risk_results?.overall_risk?.level?.toUpperCase()} RISK
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Risk Score: {results.risk_results?.overall_risk?.score}/100
            </Typography>
          </Box>
        </Box>
        <LinearProgress
          variant="determinate"
          value={results.risk_results?.overall_risk?.score || 0}
          sx={{
            mt: 2,
            height: 10,
            borderRadius: 5,
            backgroundColor: '#e0e0e0',
            '& .MuiLinearProgress-bar': {
              backgroundColor: getRiskColor(results.risk_results?.overall_risk?.level)
            }
          }}
        />
      </Paper>

      <Grid container spacing={3}>
        {/* Disease Risk Breakdown - Focus on Top Risks */}
        <Grid item xs={12} md={7}>
          <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Top Disease Risks
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Based on your symptoms, these are the conditions with the highest probability:
            </Typography>
            <List>
              {Object.entries(results.risk_results?.disease_risks || {})
                .filter(([_, risk]) => risk.level === 'high' || risk.level === 'medium')
                .sort(([_, a], [__, b]) => b.score - a.score)
                .slice(0, 3)
                .map(([disease, risk]) => (
                <React.Fragment key={disease}>
                  <ListItem>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="subtitle1" sx={{ textTransform: 'capitalize', fontWeight: 'bold' }}>
                            {disease}
                          </Typography>
                          <Chip
                            label={`${Math.round(risk.score)}% CHANCE`}
                            sx={{
                              backgroundColor: getRiskColor(risk.level),
                              color: 'white',
                              fontWeight: 'bold',
                              fontSize: '1rem'
                            }}
                          />
                        </Box>
                      }
                      secondary={
                        <Box sx={{ mt: 1 }}>
                          <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                            Risk Level: {risk.level.toUpperCase()}
                          </Typography>
                          <LinearProgress
                            variant="determinate"
                            value={risk.score}
                            sx={{
                              mt: 1,
                              height: 8,
                              borderRadius: 4,
                              backgroundColor: '#e0e0e0',
                              '& .MuiLinearProgress-bar': {
                                backgroundColor: getRiskColor(risk.level)
                              }
                            }}
                          />
                          {risk.key_factors && risk.key_factors.length > 0 && (
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="subtitle2" fontWeight="bold" color="text.primary">
                                Reasons for this risk:
                              </Typography>
                              <Box sx={{ mt: 1 }}>
                                {risk.key_factors.map((factor, idx) => (
                                  <Typography key={idx} variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                                    • {factor}
                                  </Typography>
                                ))}
                              </Box>
                            </Box>
                          )}
                        </Box>
                      }
                    />
                  </ListItem>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* Specialist Recommendations */}
        <Grid item xs={12} md={5}>
          <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Recommended Specialist
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Based on your highest risk, you should consult:
            </Typography>
            {results.specialist_recommendations?.slice(0, 1).map((rec, index) => (
              <Card key={index} sx={{ mb: 2, borderLeft: `6px solid ${getRiskColor('high')}`, backgroundColor: '#f5f5f5' }}>
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <Avatar sx={{ bgcolor: '#1976d2', width: 56, height: 56 }}>
                      <LocalHospital sx={{ fontSize: 32 }} />
                    </Avatar>
                    <Box>
                      <Typography variant="h5" fontWeight="bold">
                        {rec.specialist.name}
                      </Typography>
                      <Typography variant="body1" color="text.secondary" sx={{ fontWeight: 'medium' }}>
                        {rec.specialist.specialty}
                        {rec.specialist.sub_specialty && ` - ${rec.specialist.sub_specialty}`}
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom sx={{ fontWeight: 'medium' }}>
                    🏥 {rec.specialist.hospital} | 📍 {rec.specialist.location}
                  </Typography>
                  <Typography variant="body1" gutterBottom sx={{ mt: 1, fontWeight: 'bold' }}>
                    Why this specialist?
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {rec.reason}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Star sx={{ fontSize: 20, color: '#ffc107' }} />
                      <Typography variant="body1" fontWeight="bold">{rec.specialist.rating}</Typography>
                    </Box>
                    <Typography variant="body1" color="text.secondary" sx={{ fontWeight: 'medium' }}>
                      📞 {rec.specialist.contact}
                    </Typography>
                  </Box>
                  <Chip
                    label="URGENT CONSULTATION RECOMMENDED"
                    size="medium"
                    sx={{ mt: 2, fontWeight: 'bold' }}
                    color="error"
                  />
                </CardContent>
              </Card>
            ))}
            {results.specialist_recommendations?.length > 1 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Additional specialists available if needed:
                </Typography>
                {results.specialist_recommendations?.slice(1, 3).map((rec, index) => (
                  <Box key={index} sx={{ mt: 1, p: 1, backgroundColor: '#f9f9f9', borderRadius: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      {rec.specialist.name} - {rec.specialist.specialty}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {rec.specialist.contact}
                    </Typography>
                  </Box>
                ))}
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Health Recommendations */}
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Health Recommendations
            </Typography>
            <List>
              {results.risk_results?.recommendations?.map((rec, index) => (
                <ListItem key={index}>
                  <Chip
                    label={rec.priority.toUpperCase()}
                    size="small"
                    sx={{ mr: 2 }}
                    color={getPriorityColor(rec.priority)}
                  />
                  <ListItemText primary={rec.text} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 2 }}>
        <Button
          variant="contained"
          onClick={() => navigate('/')}
          startIcon={<Person />}
        >
          New Assessment
        </Button>
        <Button
          variant="outlined"
          onClick={() => navigate('/dashboard')}
        >
          View Dashboard
        </Button>
      </Box>
    </Box>
  );
};

export default Results;
