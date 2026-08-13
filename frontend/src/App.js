import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container, Box, AppBar, Toolbar, Typography, Button } from '@mui/material';
import PatientForm from './components/PatientForm';
import AssessmentForm from './components/AssessmentForm';
import Results from './components/Results';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Health Risk Assessment System
          </Typography>
          <Button color="inherit" href="/">Home</Button>
          <Button color="inherit" href="/dashboard">Dashboard</Button>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/" element={<PatientForm />} />
          <Route path="/assessment/:patientId" element={<AssessmentForm />} />
          <Route path="/results/:assessmentId" element={<Results />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Container>
    </Box>
  );
}

export default App;
