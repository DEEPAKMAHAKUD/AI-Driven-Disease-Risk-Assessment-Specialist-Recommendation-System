# AI-Driven Disease Risk Assessment & Specialist Recommendation System

A comprehensive healthcare application that uses artificial intelligence to assess disease risks and recommend appropriate medical specialists based on patient symptoms, medical history, and lifestyle factors.

## Features

### Core Functionality
- **Patient Registration**: Collect and manage patient demographic information
- **Health Assessment**: Comprehensive symptom and medical data collection
- **AI-Powered Risk Analysis**: Machine learning-based disease risk scoring for 6 major disease categories
- **Specialist Recommendations**: Intelligent matching with appropriate medical specialists
- **Interactive Dashboard**: Real-time monitoring and analytics
- **Data Visualization**: Visual representation of risk scores and trends

### Disease Categories Covered
1. **Cardiovascular** - Heart disease, hypertension, cholesterol, arrhythmias
2. **Diabetes** - Type 1 & 2 diabetes, metabolic disorders, blood sugar issues
3. **Respiratory** - Asthma, COPD, lung conditions, chronic cough
4. **Cancer** - Various cancer types and early detection
5. **Neurological** - Stroke, memory disorders, nerve conditions, headaches
6. **Gastrointestinal** - Digestive system disorders, stomach issues
7. **Autoimmune** - Rheumatoid arthritis, lupus, autoimmune diseases
8. **Mental Health** - Depression, anxiety, mood disorders

### Risk Assessment Factors
- Symptom analysis and pattern matching
- Medical history evaluation
- Family history consideration
- Lifestyle factor assessment (smoking, alcohol, exercise, diet)
- Laboratory results integration
- Age and gender-based risk profiling

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Machine Learning**: scikit-learn for risk algorithms
- **Data Processing**: pandas, numpy

### Frontend
- **Framework**: React.js
- **UI Library**: Material-UI (MUI)
- **Charts**: Recharts for data visualization
- **HTTP Client**: Axios
- **Routing**: React Router

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the project directory:
```bash
cd "C:\Users\DEEPAK\Desktop\risk management"
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Start the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

### 1. Patient Registration
- Open the application in your browser
- Enter patient demographic information (name, age, gender, contact)
- Click "Continue to Assessment"

### 2. Health Assessment
- Select symptoms from common symptoms list or add custom symptoms
- Provide medical history (previous conditions, surgeries)
- Enter family history (hereditary conditions)
- Select lifestyle factors (smoking, alcohol, exercise, diet)
- Optionally add lab results (cholesterol, glucose, blood pressure)
- Click "Analyze Health Risks"

### 3. View Results
- Overall health risk summary with risk score
- Detailed disease risk breakdown by category
- Risk levels (High/Medium/Low) with visual indicators
- Key contributing factors for each risk
- Specialist recommendations with contact information
- Personalized health recommendations

### 4. Dashboard
- View system statistics
- Browse available specialists
- Access quick actions
- Monitor disease categories

## API Endpoints

### Patient Management
- `POST /api/patients` - Create new patient
- `GET /api/patients/:id` - Get patient details
- `GET /api/patients/:id/assessments` - Get patient assessments

### Assessment
- `POST /api/assessments` - Create health assessment
- `GET /api/assessments/:id` - Get assessment results

### Specialists
- `GET /api/specialists` - Get all specialists

### Health
- `GET /api/health` - System health check

## Risk Assessment Algorithm

The system uses a multi-factor risk assessment approach:

1. **Symptom Matching** (40% weight): Compares patient symptoms against disease patterns
2. **Risk Factor Analysis** (30% weight): Evaluates medical history, family history, and lifestyle
3. **Age-Based Risk** (20% weight): Considers age-related risk patterns
4. **Lab Results** (10% weight): Integrates laboratory data when available

### Risk Levels
- **High** (70-100): Immediate medical attention recommended
- **Medium** (40-69): Routine check-up recommended
- **Low** (0-39): Continue regular monitoring

## Specialist Recommendation Logic

Specialists are recommended based on:
1. Primary specialty for high-risk diseases
2. Secondary specialties for comprehensive care
3. Geographic location
4. Priority level (urgent/routine/lifestyle)
5. Specialist ratings and availability

## Database Schema

### Tables
- **patients**: Demographic information
- **assessments**: Health assessment data
- **risk_scores**: Calculated risk scores by disease
- **specialists**: Medical specialist directory

## Project Structure

```
risk management/
├── app.py                      # Flask application and API routes
├── models.py                   # Database models
├── risk_assessment.py          # Risk assessment algorithms
├── specialist_recommender.py   # Specialist recommendation logic
├── init_db.py                  # Database initialization
├── requirements.txt            # Python dependencies
├── frontend/
│   ├── package.json           # Node.js dependencies
│   ├── public/
│   │   └── index.html         # HTML template
│   └── src/
│       ├── index.js           # React entry point
│       ├── App.js             # Main application component
│       └── components/
│           ├── PatientForm.js      # Patient registration
│           ├── AssessmentForm.js   # Health assessment form
│           ├── Results.js          # Results display
│           └── Dashboard.js        # System dashboard
└── README.md                  # This file
```

## Customization

### Adding New Diseases
Edit `risk_assessment.py` to add new disease patterns in the `_load_disease_patterns` method.

### Adding New Specialists
Edit `specialist_recommender.py` to add specialists to the `sample_specialists` list.

### Modifying Risk Weights
Adjust the weight coefficients in the `assess_risk` method in `risk_assessment.py`.

## Security Considerations

- This is a demonstration system and should not be used for actual medical diagnosis
- Always consult qualified healthcare professionals for medical advice
- Patient data should be encrypted in production environments
- Implement proper authentication and authorization for production use
- Ensure HIPAA compliance for handling protected health information

## Future Enhancements

- [ ] Electronic Health Record (EHR) integration
- [ ] Real-time monitoring and alerts
- [ ] Machine learning model retraining with new data
- [ ] Mobile application (iOS/Android)
- [ ] Telemedicine integration
- [ ] Advanced reporting and analytics
- [ ] Multi-language support
- [ ] Integration with wearable devices

## License

This project is for educational and demonstration purposes.

## Support

For issues, questions, or contributions, please contact the development team.

---

**Disclaimer**: This system is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
