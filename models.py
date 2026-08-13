from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assessments = db.relationship('Assessment', backref='patient', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)  # Will store JSON string
    medical_history = db.Column(db.Text)
    family_history = db.Column(db.Text)
    lifestyle_factors = db.Column(db.Text)  # Will store JSON string
    lab_results = db.Column(db.Text)  # Will store JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    risk_scores = db.relationship('RiskScore', backref='assessment', lazy=True)

class RiskScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    disease_name = db.Column(db.String(100), nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

class Specialist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    sub_specialty = db.Column(db.String(50))
    hospital = db.Column(db.String(100))
    location = db.Column(db.String(100))
    contact = db.Column(db.String(20))
