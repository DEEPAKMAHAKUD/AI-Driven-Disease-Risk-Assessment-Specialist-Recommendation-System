from app import app
from models import db, Patient, Assessment, RiskScore, Specialist

def init_database():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add sample specialists
        specialists = [
            Specialist(
                name='Dr. Sarah Johnson',
                specialty='Cardiologist',
                sub_specialty='Interventional Cardiology',
                hospital='City Heart Center',
                location='New York',
                contact='555-0101'
            ),
            Specialist(
                name='Dr. Michael Chen',
                specialty='Endocrinologist',
                sub_specialty='Diabetes Management',
                hospital='Metabolic Health Institute',
                location='New York',
                contact='555-0102'
            ),
            Specialist(
                name='Dr. Emily Rodriguez',
                specialty='Pulmonologist',
                sub_specialty='Respiratory Medicine',
                hospital='Lung & Sleep Center',
                location='Los Angeles',
                contact='555-0103'
            ),
            Specialist(
                name='Dr. James Wilson',
                specialty='Oncologist',
                sub_specialty='Medical Oncology',
                hospital='Cancer Care Center',
                location='Boston',
                contact='555-0104'
            ),
            Specialist(
                name='Dr. Lisa Thompson',
                specialty='Neurologist',
                sub_specialty='Stroke & Neurology',
                hospital='Neurological Institute',
                location='Chicago',
                contact='555-0105'
            ),
            Specialist(
                name='Dr. David Kim',
                specialty='Gastroenterologist',
                sub_specialty='Digestive Health',
                hospital='Digestive Health Center',
                location='San Francisco',
                contact='555-0106'
            ),
            Specialist(
                name='Dr. Amanda Foster',
                specialty='Internal Medicine',
                sub_specialty='Primary Care',
                hospital='General Medical Center',
                location='New York',
                contact='555-0107'
            ),
            Specialist(
                name='Dr. Robert Martinez',
                specialty='General Practitioner',
                sub_specialty='Family Medicine',
                hospital='Community Health Clinic',
                location='Los Angeles',
                contact='555-0108'
            ),
            Specialist(
                name='Dr. Jennifer Lee',
                specialty='Rheumatologist',
                sub_specialty='Autoimmune Diseases',
                hospital='Arthritis & Autoimmune Center',
                location='Boston',
                contact='555-0109'
            ),
            Specialist(
                name='Dr. William Davis',
                specialty='Psychiatrist',
                sub_specialty='Mental Health & Mood Disorders',
                hospital='Mental Wellness Institute',
                location='Chicago',
                contact='555-0110'
            )
        ]
        
        # Check if specialists already exist
        if Specialist.query.count() == 0:
            for specialist in specialists:
                db.session.add(specialist)
            db.session.commit()
            print("Sample specialists added to database")
        else:
            print("Specialists already exist in database")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
