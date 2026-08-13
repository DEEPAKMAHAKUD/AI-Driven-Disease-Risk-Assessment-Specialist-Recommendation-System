class SpecialistRecommender:
    def __init__(self):
        self.specialty_mapping = {
            'cardiovascular': {
                'primary': 'Cardiologist',
                'secondary': ['Internal Medicine', 'General Practitioner'],
                'keywords': ['heart', 'cardiac', 'vascular', 'blood pressure', 'cholesterol']
            },
            'diabetes': {
                'primary': 'Endocrinologist',
                'secondary': ['Internal Medicine', 'General Practitioner', 'Dietitian'],
                'keywords': ['diabetes', 'blood sugar', 'insulin', 'metabolic']
            },
            'respiratory': {
                'primary': 'Pulmonologist',
                'secondary': ['Internal Medicine', 'General Practitioner', 'Allergist'],
                'keywords': ['lung', 'respiratory', 'breathing', 'asthma', 'copd']
            },
            'cancer': {
                'primary': 'Oncologist',
                'secondary': ['General Practitioner', 'Surgeon', 'Radiologist'],
                'keywords': ['cancer', 'tumor', 'malignant', 'oncology']
            },
            'neurological': {
                'primary': 'Neurologist',
                'secondary': ['Internal Medicine', 'General Practitioner', 'Neurosurgeon'],
                'keywords': ['brain', 'nerve', 'neurological', 'spine', 'headache']
            },
            'gastrointestinal': {
                'primary': 'Gastroenterologist',
                'secondary': ['Internal Medicine', 'General Practitioner'],
                'keywords': ['stomach', 'digestive', 'gastrointestinal', 'liver', 'intestine']
            },
            'autoimmune': {
                'primary': 'Rheumatologist',
                'secondary': ['Immunologist', 'Internal Medicine', 'General Practitioner'],
                'keywords': ['autoimmune', 'rheumatology', 'immune system', 'inflammation']
            },
            'mental_health': {
                'primary': 'Psychiatrist',
                'secondary': ['Psychologist', 'General Practitioner', 'Therapist'],
                'keywords': ['mental health', 'psychiatry', 'depression', 'anxiety', 'psychological']
            }
        }
        
        self.sample_specialists = self._load_sample_specialists()
    
    def _load_sample_specialists(self):
        """Load sample specialist database"""
        return [
            {
                'id': 1,
                'name': 'Dr. Sarah Johnson',
                'specialty': 'Cardiologist',
                'sub_specialty': 'Interventional Cardiology',
                'hospital': 'City Heart Center',
                'location': 'New York',
                'contact': '555-0101',
                'rating': 4.8
            },
            {
                'id': 2,
                'name': 'Dr. Michael Chen',
                'specialty': 'Endocrinologist',
                'sub_specialty': 'Diabetes Management',
                'hospital': 'Metabolic Health Institute',
                'location': 'New York',
                'contact': '555-0102',
                'rating': 4.7
            },
            {
                'id': 3,
                'name': 'Dr. Emily Rodriguez',
                'specialty': 'Pulmonologist',
                'sub_specialty': 'Respiratory Medicine',
                'hospital': 'Lung & Sleep Center',
                'location': 'Los Angeles',
                'contact': '555-0103',
                'rating': 4.9
            },
            {
                'id': 4,
                'name': 'Dr. James Wilson',
                'specialty': 'Oncologist',
                'sub_specialty': 'Medical Oncology',
                'hospital': 'Cancer Care Center',
                'location': 'Boston',
                'contact': '555-0104',
                'rating': 4.6
            },
            {
                'id': 5,
                'name': 'Dr. Lisa Thompson',
                'specialty': 'Neurologist',
                'sub_specialty': 'Stroke & Neurology',
                'hospital': 'Neurological Institute',
                'location': 'Chicago',
                'contact': '555-0105',
                'rating': 4.8
            },
            {
                'id': 6,
                'name': 'Dr. David Kim',
                'specialty': 'Gastroenterologist',
                'sub_specialty': 'Digestive Health',
                'hospital': 'Digestive Health Center',
                'location': 'San Francisco',
                'contact': '555-0106',
                'rating': 4.7
            },
            {
                'id': 7,
                'name': 'Dr. Amanda Foster',
                'specialty': 'Internal Medicine',
                'sub_specialty': 'Primary Care',
                'hospital': 'General Medical Center',
                'location': 'New York',
                'contact': '555-0107',
                'rating': 4.5
            },
            {
                'id': 8,
                'name': 'Dr. Robert Martinez',
                'specialty': 'General Practitioner',
                'sub_specialty': 'Family Medicine',
                'hospital': 'Community Health Clinic',
                'location': 'Los Angeles',
                'contact': '555-0108',
                'rating': 4.6
            },
            {
                'id': 9,
                'name': 'Dr. Jennifer Lee',
                'specialty': 'Rheumatologist',
                'sub_specialty': 'Autoimmune Diseases',
                'hospital': 'Arthritis & Autoimmune Center',
                'location': 'Boston',
                'contact': '555-0109',
                'rating': 4.8
            },
            {
                'id': 10,
                'name': 'Dr. William Davis',
                'specialty': 'Psychiatrist',
                'sub_specialty': 'Mental Health & Mood Disorders',
                'hospital': 'Mental Wellness Institute',
                'location': 'Chicago',
                'contact': '555-0110',
                'rating': 4.7
            }
        ]
    
    def recommend_specialists(self, risk_results):
        """Recommend specialists based on the highest risk disease"""
        disease_risks = risk_results['disease_risks']
        recommendations = []
        
        if not disease_risks:
            # If no significant risks, recommend general practitioner
            gps = self._find_specialists_by_specialty('General Practitioner', 50)
            for gp in gps:
                recommendations.append({
                    'specialist': gp,
                    'reason': 'General health consultation for preventive care',
                    'priority': 'low',
                    'disease': 'general',
                    'risk_score': 50
                })
            return recommendations[:2]
        
        # Get the highest risk disease
        top_disease, top_risk_data = max(disease_risks.items(), key=lambda x: x[1]['score'])
        
        if top_disease in self.specialty_mapping:
            mapping = self.specialty_mapping[top_disease]
            
            # Primary specialist for the top risk
            primary_specialists = self._find_specialists_by_specialty(
                mapping['primary'], 
                top_risk_data['score']
            )
            
            for specialist in primary_specialists:
                recommendations.append({
                    'specialist': specialist,
                    'reason': f'Highest risk: {top_disease} ({round(top_risk_data["score"])}% chance). Based on your symptoms and risk factors, you should see a {mapping["primary"]} for proper diagnosis and treatment.',
                    'priority': 'high' if top_risk_data['level'] == 'high' else 'medium',
                    'disease': top_disease,
                    'risk_score': top_risk_data['score']
                })
            
            # Add one secondary specialist if high risk
            if top_risk_data['level'] == 'high' and mapping['secondary']:
                secondary = mapping['secondary'][0]  # Get first secondary
                secondary_specialists = self._find_specialists_by_specialty(
                    secondary, 
                    top_risk_data['score'] * 0.9
                )
                
                for specialist in secondary_specialists:
                    recommendations.append({
                        'specialist': specialist,
                        'reason': f'Secondary opinion specialist for {top_disease} risk',
                        'priority': 'medium',
                        'disease': top_disease,
                        'risk_score': top_risk_data['score'] * 0.9
                    })
        
        # Sort by priority and risk score
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: (priority_order[x['priority']], -x['risk_score']))
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _find_specialists_by_specialty(self, specialty, risk_score):
        """Find specialists by specialty, sorted by rating"""
        specialists = [
            specialist for specialist in self.sample_specialists
            if specialist['specialty'] == specialty
        ]
        
        # Sort by rating
        specialists.sort(key=lambda x: x['rating'], reverse=True)
        
        return specialists
    
    def get_specialist_by_id(self, specialist_id):
        """Get specialist details by ID"""
        for specialist in self.sample_specialists:
            if specialist['id'] == specialist_id:
                return specialist
        return None
    
    def search_specialists(self, query):
        """Search specialists by name, specialty, or location"""
        query_lower = query.lower()
        results = []
        
        for specialist in self.sample_specialists:
            if (query_lower in specialist['name'].lower() or
                query_lower in specialist['specialty'].lower() or
                query_lower in specialist['location'].lower() or
                (specialist['sub_specialty'] and query_lower in specialist['sub_specialty'].lower())):
                results.append(specialist)
        
        return results
