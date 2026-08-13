import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import json

class DiseaseRiskAssessment:
    def __init__(self):
        self.disease_patterns = self._load_disease_patterns()
        self.risk_factors = self._load_risk_factors()
        self.scaler = StandardScaler()
        
    def _load_disease_patterns(self):
        """Load disease-symptom patterns and risk factors"""
        return {
            'cardiovascular': {
                'key_symptoms': [
                    'chest pain', 'chest pressure', 'chest tightness', 'chest discomfort',
                    'shortness of breath', 'dyspnea', 'breathlessness',
                    'palpitations', 'irregular heartbeat', 'rapid heartbeat', 'arrhythmia',
                    'fatigue', 'weakness', 'tiredness', 'exhaustion',
                    'dizziness', 'lightheadedness', 'fainting', 'syncope',
                    'swelling', 'edema', 'leg swelling', 'ankle swelling',
                    'nausea', 'indigestion', 'heartburn', 'stomach pain',
                    'cold sweats', 'clammy skin', 'pale skin',
                    'back pain', 'jaw pain', 'arm pain', 'neck pain',
                    'cough', 'wheezing', 'difficulty breathing when lying down'
                ],
                'secondary_symptoms': [
                    'anxiety', 'sleep problems', 'reduced exercise tolerance',
                    'appetite loss', 'weight gain', 'confusion'
                ],
                'risk_factors': ['hypertension', 'diabetes', 'smoking', 'obesity', 'high cholesterol', 'family history', 'sedentary lifestyle', 'stress', 'alcohol'],
                'age_risk': {'low': 40, 'medium': 55, 'high': 65},
                'weight': 0.95,
                'symptom_combinations': {
                    'high_risk': [['chest pain', 'shortness of breath'], ['chest pain', 'sweating'], ['shortness of breath', 'fatigue']],
                    'medium_risk': [['palpitations', 'dizziness'], ['fatigue', 'swelling'], ['chest discomfort', 'nausea']]
                }
            },
            'diabetes': {
                'key_symptoms': [
                    'increased thirst', 'excessive thirst', 'polydipsia', 'dry mouth',
                    'frequent urination', 'excessive urination', 'polyuria', 'night urination',
                    'fatigue', 'tiredness', 'weakness', 'lethargy',
                    'blurred vision', 'vision changes', 'floaters', 'dark vision',
                    'slow healing', 'poor wound healing', 'frequent infections',
                    'increased hunger', 'excessive hunger', 'polyphagia',
                    'unexplained weight loss', 'weight loss despite increased appetite',
                    'numbness', 'tingling', 'burning sensation', 'nerve pain',
                    'dry skin', 'itchy skin', 'skin infections',
                    'yeast infections', 'frequent yeast infections',
                    'darkened skin', 'skin patches', 'acanthosis nigricans'
                ],
                'secondary_symptoms': [
                    'irritability', 'mood changes', 'difficulty concentrating',
                    'slow healing sores', 'gum disease', 'erectile dysfunction'
                ],
                'risk_factors': ['obesity', 'family history', 'sedentary lifestyle', 'high blood pressure', 'age', 'prediabetes', 'gestational diabetes', 'ethnicity', 'stress'],
                'age_risk': {'low': 35, 'medium': 45, 'high': 55},
                'weight': 0.9,
                'symptom_combinations': {
                    'high_risk': [['increased thirst', 'frequent urination'], ['increased thirst', 'fatigue'], ['frequent urination', 'weight loss']],
                    'medium_risk': [['blurred vision', 'fatigue'], ['slow healing', 'infections'], ['numbness', 'tingling']]
                }
            },
            'respiratory': {
                'key_symptoms': [
                    'cough', 'chronic cough', 'persistent cough', 'dry cough', 'productive cough',
                    'shortness of breath', 'dyspnea', 'breathlessness', 'difficulty breathing',
                    'wheezing', 'whistling sound', 'chest tightness', 'chest constriction',
                    'mucus production', 'phlegm', 'sputum', 'excessive mucus',
                    'chest pain', 'chest discomfort', 'chest pressure',
                    'difficulty breathing when lying down', 'orthopnea',
                    'night sweats', 'fever', 'chills',
                    'hoarseness', 'voice changes', 'throat irritation',
                    'nasal congestion', 'runny nose', 'sinus pressure',
                    'loss of smell', 'loss of taste', 'breath sounds'
                ],
                'secondary_symptoms': [
                    'fatigue', 'weakness', 'exercise intolerance',
                    'anxiety', 'panic attacks', 'sleep disturbances',
                    'coughing up blood', 'hemoptysis', 'weight loss'
                ],
                'risk_factors': ['smoking', 'pollution exposure', 'family history', 'respiratory infections', 'occupational exposure', 'allergies', 'asthma', 'copd'],
                'age_risk': {'low': 30, 'medium': 50, 'high': 65},
                'weight': 0.85,
                'symptom_combinations': {
                    'high_risk': [['shortness of breath', 'wheezing'], ['chronic cough', 'mucus production'], ['chest tightness', 'difficulty breathing']],
                    'medium_risk': [['cough', 'chest discomfort'], ['wheezing', 'chest tightness'], ['shortness of breath', 'fatigue']]
                }
            },
            'cancer': {
                'key_symptoms': [
                    'unexplained weight loss', 'weight loss without trying', 'significant weight loss',
                    'fatigue', 'extreme tiredness', 'persistent exhaustion', 'weakness',
                    'pain', 'persistent pain', 'bone pain', 'headaches', 'back pain',
                    'skin changes', 'skin discoloration', 'new moles', 'changing moles', 'skin lesions',
                    'lumps', 'masses', 'thickening', 'swelling', 'unusual lumps',
                    'changes in bowel habits', 'constipation', 'diarrhea', 'blood in stool',
                    'changes in bladder habits', 'blood in urine', 'frequent urination',
                    'unusual bleeding', 'bruising', 'abnormal bleeding',
                    'persistent cough', 'hoarseness', 'voice changes', 'difficulty swallowing',
                    'fever', 'night sweats', 'recurrent fevers',
                    'sores that do not heal', 'persistent sores', 'non-healing wounds',
                    'difficulty swallowing', 'dysphagia', 'food getting stuck'
                ],
                'secondary_symptoms': [
                    'anemia', 'pale skin', 'shortness of breath', 'dizziness',
                    'loss of appetite', 'nausea', 'vomiting', 'indigestion',
                    'abdominal pain', 'bloating', 'fullness', 'swelling'
                ],
                'risk_factors': ['family history', 'age', 'smoking', 'radiation exposure', 'chemical exposure', 'sun exposure', 'obesity', 'alcohol', 'certain infections', 'immunosuppression'],
                'age_risk': {'low': 40, 'medium': 55, 'high': 70},
                'weight': 0.98,
                'symptom_combinations': {
                    'high_risk': [['unexplained weight loss', 'fatigue'], ['unexplained weight loss', 'pain'], ['persistent cough', 'weight loss']],
                    'medium_risk': [['fatigue', 'pain'], ['skin changes', 'lumps'], ['changes in bowel habits', 'abdominal pain']]
                }
            },
            'neurological': {
                'key_symptoms': [
                    'headaches', 'migraines', 'severe headaches', 'persistent headaches',
                    'memory loss', 'forgetfulness', 'confusion', 'disorientation',
                    'seizures', 'convulsions', 'episodes', 'spasms',
                    'numbness', 'tingling', 'pins and needles', 'sensation loss',
                    'weakness', 'muscle weakness', 'paralysis', 'difficulty moving',
                    'coordination problems', 'balance issues', 'clumsiness', 'stumbling',
                    'tremors', 'shaking', 'involuntary movements', 'muscle twitches',
                    'vision problems', 'double vision', 'vision loss', 'blurred vision',
                    'speech problems', 'slurred speech', 'difficulty speaking', 'word finding',
                    'dizziness', 'vertigo', 'spinning sensation', 'loss of balance',
                    'sleep problems', 'insomnia', 'excessive sleeping', 'sleep disturbances'
                ],
                'secondary_symptoms': [
                    'mood changes', 'depression', 'anxiety', 'personality changes',
                    'cognitive decline', 'thinking problems', 'concentration issues',
                    'fatigue', 'exhaustion', 'loss of motivation', 'apathy'
                ],
                'risk_factors': ['family history', 'age', 'head trauma', 'infections', 'vascular conditions', 'stroke', 'autoimmune disorders', 'environmental toxins'],
                'age_risk': {'low': 45, 'medium': 60, 'high': 75},
                'weight': 0.9,
                'symptom_combinations': {
                    'high_risk': [['headaches', 'vision problems'], ['numbness', 'weakness'], ['memory loss', 'confusion']],
                    'medium_risk': [['dizziness', 'coordination problems'], ['speech problems', 'weakness'], ['tremors', 'coordination problems']]
                }
            },
            'gastrointestinal': {
                'key_symptoms': [
                    'abdominal pain', 'stomach pain', 'belly pain', 'cramping',
                    'nausea', 'feeling sick', 'urge to vomit', 'queasiness',
                    'vomiting', 'throwing up', 'emesis', 'projectile vomiting',
                    'diarrhea', 'loose stools', 'frequent bowel movements', 'watery stool',
                    'constipation', 'difficulty passing stool', 'hard stools', 'infrequent bowel movements',
                    'bloating', 'abdominal distension', 'feeling full', 'gas',
                    'heartburn', 'acid reflux', 'gerd', 'chest burning',
                    'indigestion', 'dyspepsia', 'stomach upset', 'discomfort after eating',
                    'loss of appetite', 'reduced hunger', 'not feeling hungry',
                    'blood in stool', 'rectal bleeding', 'dark stool', 'tarry stool',
                    'difficulty swallowing', 'dysphagia', 'food getting stuck',
                    'weight loss', 'unexplained weight loss', 'unintentional weight loss'
                ],
                'secondary_symptoms': [
                    'fatigue', 'weakness', 'dehydration', 'dry mouth',
                    'fever', 'chills', 'body aches', 'malaise',
                    'mouth sores', 'tongue problems', 'difficulty tasting'
                ],
                'risk_factors': ['diet', 'infections', 'medications', 'stress', 'family history', 'alcohol', 'smoking', 'obesity', 'autoimmune conditions'],
                'age_risk': {'low': 30, 'medium': 50, 'high': 65},
                'weight': 0.8,
                'symptom_combinations': {
                    'high_risk': [['abdominal pain', 'vomiting'], ['diarrhea', 'dehydration'], 'blood in stool', 'weight loss'],
                    'medium_risk': [['nausea', 'bloating'], ['heartburn', 'indigestion'], ['abdominal pain', 'diarrhea']]
                }
            },
            'autoimmune': {
                'key_symptoms': [
                    'joint pain', 'joint swelling', 'joint stiffness', 'morning stiffness',
                    'muscle pain', 'muscle weakness', 'muscle aches',
                    'fatigue', 'extreme tiredness', 'chronic fatigue', 'exhaustion',
                    'fever', 'low-grade fever', 'recurrent fever', 'fever of unknown origin',
                    'skin rashes', 'butterfly rash', 'skin lesions', 'photosensitivity',
                    'hair loss', 'alopecia', 'thinning hair',
                    'dry eyes', 'dry mouth', 'sicca symptoms',
                    'numbness', 'tingling', 'sensation changes',
                    'swelling', 'edema', 'generalized swelling',
                    'weight changes', 'weight loss', 'weight gain',
                    'cold sensitivity', 'heat sensitivity', 'temperature intolerance'
                ],
                'secondary_symptoms': [
                    'raynauds', 'color changes in fingers', 'finger color changes',
                    'mouth ulcers', 'oral ulcers', 'canker sores',
                    'chest pain', 'pleuritic pain', 'shortness of breath',
                    'headaches', 'migraines', 'cognitive fog'
                ],
                'risk_factors': ['family history', 'gender', 'age', 'infections', 'environmental triggers', 'other autoimmune diseases', 'stress'],
                'age_risk': {'low': 20, 'medium': 35, 'high': 50},
                'weight': 0.85,
                'symptom_combinations': {
                    'high_risk': [['joint pain', 'fatigue'], ['skin rashes', 'joint pain'], ['fever', 'joint swelling']],
                    'medium_risk': [['fatigue', 'muscle pain'], ['dry eyes', 'dry mouth'], ['skin rashes', 'fever']]
                }
            },
            'mental_health': {
                'key_symptoms': [
                    'persistent sadness', 'depressed mood', 'hopelessness', 'worthlessness',
                    'loss of interest', 'anhedonia', 'no pleasure', 'withdrawal',
                    'anxiety', 'excessive worry', 'nervousness', 'restlessness',
                    'sleep problems', 'insomnia', 'hypersomnia', 'sleep disturbances',
                    'appetite changes', 'increased appetite', 'decreased appetite',
                    'concentration problems', 'difficulty focusing', 'memory issues',
                    'fatigue', 'low energy', 'lack of motivation', 'lethargy',
                    'irritability', 'mood swings', 'anger', 'frustration',
                    'physical symptoms', 'unexplained pain', 'headaches', 'stomach problems',
                    'thoughts of death', 'suicidal thoughts', 'self-harm thoughts'
                ],
                'secondary_symptoms': [
                    'social withdrawal', 'isolation', 'relationship problems',
                    'substance use', 'alcohol use', 'drug use',
                    'guilt', 'shame', 'self-criticism', 'negative thinking'
                ],
                'risk_factors': ['family history', 'trauma', 'stress', 'chronic illness', 'substance use', 'personality factors', 'life changes'],
                'age_risk': {'low': 15, 'medium': 25, 'high': 40},
                'weight': 0.75,
                'symptom_combinations': {
                    'high_risk': [['persistent sadness', 'loss of interest'], ['anxiety', 'sleep problems'], ['fatigue', 'concentration problems']],
                    'medium_risk': [['sleep problems', 'appetite changes'], ['irritability', 'fatigue'], ['concentration problems', 'low energy']]
                }
            }
        }
    
    def _load_risk_factors(self):
        """Load risk factor weights"""
        return {
            'smoking': 0.3,
            'obesity': 0.25,
            'family_history': 0.35,
            'sedentary_lifestyle': 0.2,
            'alcohol': 0.15,
            'stress': 0.1
        }
    
    def assess_risk(self, symptoms, medical_history, family_history, lifestyle_factors, lab_results, age, gender):
        """Assess disease risk based on multiple factors"""
        disease_risks = {}
        
        symptoms_list = [s.lower() for s in symptoms] if isinstance(symptoms, list) else symptoms.lower().split(',')
        medical_history_lower = medical_history.lower() if medical_history else ''
        family_history_lower = family_history.lower() if family_history else ''
        
        for disease, pattern in self.disease_patterns.items():
            # Symptom matching score
            symptom_score = self._calculate_symptom_score(
                symptoms_list, 
                pattern['key_symptoms'],
                pattern.get('secondary_symptoms', []),
                pattern.get('symptom_combinations', {})
            )
            
            # Risk factor score
            risk_factor_score = self._calculate_risk_factor_score(
                medical_history_lower, 
                family_history_lower, 
                lifestyle_factors,
                pattern['risk_factors']
            )
            
            # Age-based risk
            age_score = self._calculate_age_score(age, pattern['age_risk'])
            
            # Lab results impact
            lab_score = self._calculate_lab_score(lab_results, disease)
            
            # Combine scores with weights
            total_score = (
                symptom_score * 0.4 +
                risk_factor_score * 0.3 +
                age_score * 0.2 +
                lab_score * 0.1
            ) * pattern['weight']
            
            # Normalize to 0-100
            total_score = min(100, max(0, total_score * 100))
            
            # Determine risk level
            risk_level = self._determine_risk_level(total_score)
            
            # Calculate confidence based on data completeness
            confidence = self._calculate_confidence(
                symptoms_list, 
                medical_history, 
                family_history, 
                lifestyle_factors,
                lab_results
            )
            
            disease_risks[disease] = {
                'score': round(total_score, 2),
                'level': risk_level,
                'confidence': round(confidence, 2),
                'key_factors': self._identify_key_factors(
                    symptoms_list, 
                    medical_history_lower, 
                    family_history_lower,
                    pattern
                )
            }
        
        # Sort by risk score and filter to show only significant risks
        sorted_risks = dict(sorted(disease_risks.items(), key=lambda x: x[1]['score'], reverse=True))
        
        # Focus on top risks (high, medium, and top low risks)
        significant_risks = {
            disease: risk for disease, risk in sorted_risks.items() 
            if risk['level'] in ['high', 'medium'] or risk['score'] >= 30
        }
        
        # If no significant risks, show at least the top 2
        if not significant_risks:
            significant_risks = dict(list(sorted_risks.items())[:2])
        
        return {
            'disease_risks': significant_risks,
            'overall_risk': self._calculate_overall_risk(significant_risks),
            'recommendations': self._generate_recommendations(significant_risks)
        }
    
    def _calculate_symptom_score(self, symptoms, key_symptoms, secondary_symptoms=None, symptom_combinations=None):
        """Calculate how well symptoms match disease pattern"""
        if not symptoms:
            return 0.0
        
        # Primary symptom matching
        primary_matches = sum(1 for symptom in symptoms if any(key in symptom for key in key_symptoms))
        primary_score = primary_matches / len(key_symptoms) if key_symptoms else 0.0
        
        # Secondary symptom matching (with lower weight)
        secondary_score = 0.0
        if secondary_symptoms:
            secondary_matches = sum(1 for symptom in symptoms if any(key in symptom for key in secondary_symptoms))
            secondary_score = (secondary_matches / len(secondary_symptoms)) * 0.5 if secondary_symptoms else 0.0
        
        # Symptom combination bonus
        combination_bonus = 0.0
        if symptom_combinations:
            for combo_level, combinations in symptom_combinations.items():
                bonus_multiplier = 0.3 if combo_level == 'high_risk' else 0.15
                for combo in combinations:
                    if all(any(combo_symptom in symptom for symptom in symptoms) for combo_symptom in combo):
                        combination_bonus += bonus_multiplier
        
        # Cap the combination bonus
        combination_bonus = min(0.5, combination_bonus)
        
        # Weighted combination
        total_score = (primary_score * 0.6) + (secondary_score * 0.2) + combination_bonus
        
        return min(1.0, total_score)
    
    def _calculate_risk_factor_score(self, medical_history, family_history, lifestyle_factors, risk_factors):
        """Calculate risk factor contribution"""
        score = 0.0
        total_factors = len(risk_factors)
        
        if total_factors == 0:
            return 0.0
        
        for factor in risk_factors:
            factor_lower = factor.lower().replace(' ', '_')
            
            # Check medical history
            if factor_lower in medical_history.replace(' ', '_'):
                score += 0.5
            
            # Check family history
            if factor_lower in family_history.replace(' ', '_'):
                score += 0.3
            
            # Check lifestyle factors
            if lifestyle_factors:
                for key, value in lifestyle_factors.items():
                    if key.lower() in factor_lower and value:
                        score += 0.2
        
        return score / total_factors
    
    def _calculate_age_score(self, age, age_risk):
        """Calculate age-based risk score"""
        if age < age_risk['low']:
            return 0.2
        elif age < age_risk['medium']:
            return 0.5
        elif age < age_risk['high']:
            return 0.7
        else:
            return 0.9
    
    def _calculate_lab_score(self, lab_results, disease):
        """Calculate lab results contribution to risk"""
        if not lab_results:
            return 0.0
        
        score = 0.0
        
        # Disease-specific lab indicators
        lab_indicators = {
            'cardiovascular': ['cholesterol', 'ldl', 'hdl', 'triglycerides', 'blood_pressure'],
            'diabetes': ['glucose', 'hba1c', 'insulin'],
            'respiratory': ['oxygen_saturation', 'lung_function'],
            'cancer': ['tumor_markers', 'blood_count'],
            'neurological': ['brain_imaging', 'nerve_conduction'],
            'gastrointestinal': ['liver_enzymes', 'digestive_enzymes']
        }
        
        indicators = lab_indicators.get(disease, [])
        
        for indicator in indicators:
            if indicator in lab_results:
                value = lab_results[indicator]
                # Simplified abnormal range detection
                if isinstance(value, (int, float)):
                    if indicator in ['cholesterol', 'ldl', 'triglycerides', 'glucose', 'hba1c']:
                        if value > 200:  # Simplified threshold
                            score += 0.3
                    elif indicator in ['hdl']:
                        if value < 40:  # Simplified threshold
                            score += 0.3
                    else:
                        score += 0.2
        
        return min(1.0, score)
    
    def _determine_risk_level(self, score):
        """Determine risk level based on score"""
        if score >= 70:
            return 'high'
        elif score >= 40:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_confidence(self, symptoms, medical_history, family_history, lifestyle_factors, lab_results):
        """Calculate confidence in assessment based on data completeness"""
        confidence = 0.0
        
        if symptoms and (isinstance(symptoms, list) and len(symptoms) > 0 or len(symptoms) > 0):
            confidence += 0.3
        
        if medical_history:
            confidence += 0.2
        
        if family_history:
            confidence += 0.2
        
        if lifestyle_factors and len(lifestyle_factors) > 0:
            confidence += 0.2
        
        if lab_results and len(lab_results) > 0:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _identify_key_factors(self, symptoms, medical_history, family_history, pattern):
        """Identify key contributing factors"""
        factors = []
        
        # Symptom matches
        for symptom in symptoms:
            for key_symptom in pattern['key_symptoms']:
                if key_symptom in symptom:
                    factors.append(f"Symptom: {symptom}")
                    break
        
        # Risk factor matches
        for risk_factor in pattern['risk_factors']:
            if risk_factor.lower() in medical_history:
                factors.append(f"Medical history: {risk_factor}")
            if risk_factor.lower() in family_history:
                factors.append(f"Family history: {risk_factor}")
        
        return factors[:5]  # Return top 5 factors
    
    def _calculate_overall_risk(self, disease_risks):
        """Calculate overall health risk based on significant risks"""
        if not disease_risks:
            return {'score': 0, 'level': 'low'}
        
        # Take the highest risk as the overall risk
        max_risk = max(disease_risks.values(), key=lambda x: x['score'])
        
        return {
            'score': round(max_risk['score'], 2),
            'level': max_risk['level']
        }
    
    def _generate_recommendations(self, disease_risks):
        """Generate health recommendations based on risks"""
        recommendations = []
        
        high_risk_diseases = [d for d, r in disease_risks.items() if r['level'] == 'high']
        
        if high_risk_diseases:
            recommendations.append({
                'priority': 'urgent',
                'text': 'Immediate medical consultation recommended due to high-risk indicators'
            })
        
        medium_risk_diseases = [d for d, r in disease_risks.items() if r['level'] == 'medium']
        
        if medium_risk_diseases:
            recommendations.append({
                'priority': 'routine',
                'text': 'Schedule routine check-up to monitor medium-risk conditions'
            })
        
        general_recommendations = [
            'Maintain a balanced diet rich in fruits and vegetables',
            'Engage in regular physical activity (150 minutes moderate exercise per week)',
            'Ensure adequate sleep (7-9 hours per night)',
            'Manage stress through relaxation techniques',
            'Stay hydrated and limit alcohol consumption'
        ]
        
        recommendations.extend([
            {'priority': 'lifestyle', 'text': rec} for rec in general_recommendations
        ])
        
        return recommendations
