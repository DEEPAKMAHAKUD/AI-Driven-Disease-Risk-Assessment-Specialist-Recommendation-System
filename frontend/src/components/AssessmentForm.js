import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Checkbox,
  FormControlLabel
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const AssessmentForm = () => {
  const navigate = useNavigate();
  const { patientId } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [patient, setPatient] = useState(null);
  
  const [symptoms, setSymptoms] = useState([]);
  const [customSymptom, setCustomSymptom] = useState('');
  
  const commonSymptoms = [
    'chest pain', 'chest pressure', 'shortness of breath', 'palpitations',
    'fatigue', 'dizziness', 'fainting', 'swelling', 'nausea',
    'increased thirst', 'frequent urination', 'blurred vision', 'slow healing',
    'unexplained weight loss', 'numbness', 'tingling', 'dry skin',
    'chronic cough', 'wheezing', 'chest tightness', 'mucus production',
    'persistent pain', 'skin changes', 'lumps', 'unusual bleeding',
    'headaches', 'memory loss', 'confusion', 'coordination problems',
    'abdominal pain', 'vomiting', 'diarrhea', 'constipation', 'bloating',
    'joint pain', 'joint swelling', 'muscle weakness', 'fever',
    'persistent sadness', 'anxiety', 'sleep problems', 'concentration problems'
  ];

  const [formData, setFormData] = useState({
    medical_history: '',
    family_history: '',
    lifestyle_factors: {
      smoking: false,
      alcohol: false,
      exercise: false,
      diet: false
    },
    lab_results: {}
  });

  useEffect(() => {
    fetchPatient();
  }, [patientId]);

  const fetchPatient = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/patients/${patientId}`);
      setPatient(response.data);
    } catch (err) {
      setError('Failed to load patient information');
      console.error('Error fetching patient:', err);
    }
  };

  const handleSymptomToggle = (symptom) => {
    setSymptoms(prev => 
      prev.includes(symptom) 
        ? prev.filter(s => s !== symptom)
        : [...prev, symptom]
    );
  };

  const handleAddCustomSymptom = () => {
    if (customSymptom.trim() && !symptoms.includes(customSymptom.trim())) {
      setSymptoms([...symptoms, customSymptom.trim()]);
      setCustomSymptom('');
    }
  };

  const handleLifestyleChange = (factor) => {
    setFormData({
      ...formData,
      lifestyle_factors: {
        ...formData.lifestyle_factors,
        [factor]: !formData.lifestyle_factors[factor]
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (symptoms.length === 0) {
      setError('Please select at least one symptom');
      setLoading(false);
      return;
    }

    try {
      const assessmentData = {
        patient_id: parseInt(patientId),
        symptoms: symptoms,
        medical_history: formData.medical_history,
        family_history: formData.family_history,
        lifestyle_factors: formData.lifestyle_factors,
        lab_results: formData.lab_results,
        age: patient?.age,
        gender: patient?.gender
      };

      const response = await axios.post('http://localhost:5000/api/assessments', assessmentData);
      navigate(`/results/${response.data.assessment_id}`);
    } catch (err) {
      setError('Failed to create assessment. Please try again.');
      console.error('Error creating assessment:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!patient) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto' }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          Health Assessment
        </Typography>
        <Typography variant="subtitle1" gutterBottom align="center" color="text.secondary">
          Patient: {patient.name} | Age: {patient.age} | Gender: {patient.gender}
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <form onSubmit={handleSubmit}>
          {/* Symptoms Section */}
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Symptoms
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
            {commonSymptoms.map((symptom) => (
              <Chip
                key={symptom}
                label={symptom}
                onClick={() => handleSymptomToggle(symptom)}
                color={symptoms.includes(symptom) ? 'primary' : 'default'}
                clickable
              />
            ))}
          </Box>
          
          <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
            <TextField
              fullWidth
              label="Other symptoms"
              value={customSymptom}
              onChange={(e) => setCustomSymptom(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddCustomSymptom())}
            />
            <Button variant="outlined" onClick={handleAddCustomSymptom}>
              Add
            </Button>
          </Box>

          {/* Selected Symptoms */}
          {symptoms.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Selected: {symptoms.join(', ')}
              </Typography>
            </Box>
          )}

          {/* Medical History */}
          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Medical History
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Previous medical conditions, surgeries, treatments"
            value={formData.medical_history}
            onChange={(e) => setFormData({...formData, medical_history: e.target.value})}
            margin="normal"
          />

          {/* Family History */}
          <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
            Family History
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Family medical history, hereditary conditions"
            value={formData.family_history}
            onChange={(e) => setFormData({...formData, family_history: e.target.value})}
            margin="normal"
          />

          {/* Lifestyle Factors */}
          <Accordion sx={{ mt: 3 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Lifestyle Factors</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.lifestyle_factors.smoking}
                    onChange={() => handleLifestyleChange('smoking')}
                  />
                }
                label="Smoking"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.lifestyle_factors.alcohol}
                    onChange={() => handleLifestyleChange('alcohol')}
                  />
                }
                label="Alcohol Consumption"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.lifestyle_factors.exercise}
                    onChange={() => handleLifestyleChange('exercise')}
                  />
                }
                label="Regular Exercise"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.lifestyle_factors.diet}
                    onChange={() => handleLifestyleChange('diet')}
                  />
                }
                label="Balanced Diet"
              />
            </AccordionDetails>
          </Accordion>

          {/* Lab Results */}
          <Accordion sx={{ mt: 2 }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Lab Results (Optional)</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <TextField
                fullWidth
                label="Cholesterol (mg/dL)"
                type="number"
                value={formData.lab_results.cholesterol || ''}
                onChange={(e) => setFormData({
                  ...formData,
                  lab_results: {...formData.lab_results, cholesterol: parseFloat(e.target.value)}
                })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Blood Glucose (mg/dL)"
                type="number"
                value={formData.lab_results.glucose || ''}
                onChange={(e) => setFormData({
                  ...formData,
                  lab_results: {...formData.lab_results, glucose: parseFloat(e.target.value)}
                })}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Blood Pressure (systolic)"
                type="number"
                value={formData.lab_results.blood_pressure || ''}
                onChange={(e) => setFormData({
                  ...formData,
                  lab_results: {...formData.lab_results, blood_pressure: parseFloat(e.target.value)}
                })}
                margin="normal"
              />
            </AccordionDetails>
          </Accordion>

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            sx={{ mt: 4 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Analyze Health Risks'}
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default AssessmentForm;
