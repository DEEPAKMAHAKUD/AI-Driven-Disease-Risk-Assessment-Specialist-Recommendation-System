from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "health_assessment.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db and models
from models import db, Patient, Assessment, RiskScore, Specialist

# Initialize db with app
db.init_app(app)
from risk_assessment import DiseaseRiskAssessment
from specialist_recommender import SpecialistRecommender

# Initialize assessment engine
risk_assessor = DiseaseRiskAssessment()
specialist_recommender = SpecialistRecommender()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        contact=data.get('contact', ''),
        email=data.get('email', '')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({"message": "Patient created", "patient_id": patient.id}), 201

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "contact": patient.contact,
        "email": patient.email,
        "created_at": patient.created_at.isoformat()
    })

@app.route('/api/assessments', methods=['POST'])
def create_assessment():
    data = request.json
    
    # Create assessment record
    assessment = Assessment(
        patient_id=data['patient_id'],
        symptoms=json.dumps(data['symptoms']) if isinstance(data['symptoms'], list) else data['symptoms'],
        medical_history=data.get('medical_history', ''),
        family_history=data.get('family_history', ''),
        lifestyle_factors=json.dumps(data.get('lifestyle_factors', {})),
        lab_results=json.dumps(data.get('lab_results', {}))
    )
    db.session.add(assessment)
    db.session.commit()
    
    # Calculate risk scores
    risk_results = risk_assessor.assess_risk(
        symptoms=data['symptoms'],
        medical_history=data.get('medical_history', ''),
        family_history=data.get('family_history', ''),
        lifestyle_factors=data.get('lifestyle_factors', {}),
        lab_results=data.get('lab_results', {}),
        age=data.get('age'),
        gender=data.get('gender')
    )
    
    # Store risk scores
    for disease, score_data in risk_results['disease_risks'].items():
        risk_score = RiskScore(
            assessment_id=assessment.id,
            disease_name=disease,
            risk_score=score_data['score'],
            risk_level=score_data['level'],
            confidence=score_data['confidence']
        )
        db.session.add(risk_score)
    
    # Get specialist recommendations
    recommendations = specialist_recommender.recommend_specialists(risk_results)
    
    db.session.commit()
    
    return jsonify({
        "assessment_id": assessment.id,
        "risk_results": risk_results,
        "specialist_recommendations": recommendations
    }), 201

@app.route('/api/assessments/<int:assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    risk_scores = RiskScore.query.filter_by(assessment_id=assessment_id).all()
    
    # Parse JSON fields
    try:
        symptoms = json.loads(assessment.symptoms) if assessment.symptoms else []
    except:
        symptoms = assessment.symptoms
    
    try:
        lifestyle_factors = json.loads(assessment.lifestyle_factors) if assessment.lifestyle_factors else {}
    except:
        lifestyle_factors = assessment.lifestyle_factors
    
    try:
        lab_results = json.loads(assessment.lab_results) if assessment.lab_results else {}
    except:
        lab_results = assessment.lab_results
    
    # Get patient data for age and gender
    patient = Patient.query.get(assessment.patient_id)
    
    # Re-calculate risk results to get full analysis
    risk_results = risk_assessor.assess_risk(
        symptoms=symptoms,
        medical_history=assessment.medical_history,
        family_history=assessment.family_history,
        lifestyle_factors=lifestyle_factors,
        lab_results=lab_results,
        age=patient.age if patient else None,
        gender=patient.gender if patient else None
    )
    
    # Get specialist recommendations
    recommendations = specialist_recommender.recommend_specialists(risk_results)
    
    return jsonify({
        "id": assessment.id,
        "patient_id": assessment.patient_id,
        "symptoms": symptoms,
        "medical_history": assessment.medical_history,
        "family_history": assessment.family_history,
        "lifestyle_factors": lifestyle_factors,
        "lab_results": lab_results,
        "created_at": assessment.created_at.isoformat(),
        "risk_scores": [{
            "disease_name": rs.disease_name,
            "risk_score": rs.risk_score,
            "risk_level": rs.risk_level,
            "confidence": rs.confidence
        } for rs in risk_scores],
        "risk_results": risk_results,
        "specialist_recommendations": recommendations
    })

@app.route('/api/patients/<int:patient_id>/assessments', methods=['GET'])
def get_patient_assessments(patient_id):
    assessments = Assessment.query.filter_by(patient_id=patient_id).all()
    return jsonify({
        "assessments": [{
            "id": a.id,
            "created_at": a.created_at.isoformat(),
            "symptoms": a.symptoms
        } for a in assessments]
    })

@app.route('/api/specialists', methods=['GET'])
def get_specialists():
    specialists = Specialist.query.all()
    return jsonify({
        "specialists": [{
            "id": s.id,
            "name": s.name,
            "specialty": s.specialty,
            "sub_specialty": s.sub_specialty,
            "hospital": s.hospital,
            "location": s.location,
            "contact": s.contact
        } for s in specialists]
    })

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    total_patients = Patient.query.count()
    total_assessments = Assessment.query.count()
    total_specialists = Specialist.query.count()
    
    # Get recent assessments
    recent_assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(5).all()
    
    return jsonify({
        "total_patients": total_patients,
        "total_assessments": total_assessments,
        "total_specialists": total_specialists,
        "recent_assessments": [{
            "id": a.id,
            "patient_id": a.patient_id,
            "created_at": a.created_at.isoformat(),
            "symptoms": a.symptoms
        } for a in recent_assessments]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
