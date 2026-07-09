from app.database.session import SessionLocal, engine
from app.database.models import Base, Organization, Team, Advisor, Customer, Call, TranscriptSegment, Score, Issue
from app.api.routes.upload import process_call_pipeline
import os
import shutil

def seed_db():
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        
        org = Organization(name="FitNova Bangalore")
        db.add(org)
        db.commit()
        db.refresh(org)
        
        team_alpha = Team(name="Team Alpha", organization_id=org.id)
        team_beta = Team(name="Team Beta", organization_id=org.id)
        db.add_all([team_alpha, team_beta])
        db.commit()
        db.refresh(team_alpha)
        db.refresh(team_beta)
        
        amit = Advisor(name="Amit", email="amit.sharma@fitnova.com", team_id=team_alpha.id, organization_id=org.id)
        rohan = Advisor(name="Rohan", email="rohan.das@fitnova.com", team_id=team_alpha.id, organization_id=org.id)
        priya = Advisor(name="Priya", email="priya.patel@fitnova.com", team_id=team_beta.id, organization_id=org.id)
        karan = Advisor(name="Karan", email="karan.singh@fitnova.com", team_id=team_beta.id, organization_id=org.id)
        db.add_all([amit, rohan, priya, karan])
        db.commit()
        db.refresh(amit)
        db.refresh(rohan)
        db.refresh(priya)
        db.refresh(karan)
        
        team_alpha.team_leader_id = amit.id
        team_beta.team_leader_id = priya.id
        db.commit()
        
        cust1 = Customer(name="Rajesh Kumar", phone="9876543210", email="rajesh@gmail.com")
        cust2 = Customer(name="Suresh Patel", phone="9123456789", email="suresh@gmail.com")
        cust3 = Customer(name="Anjali Sharma", phone="9988776655", email="anjali@gmail.com")
        db.add_all([cust1, cust2, cust3])
        db.commit()
        db.refresh(cust1)
        db.refresh(cust2)
        db.refresh(cust3)
        
        print("Database seeded with Organizations, Teams, and Advisors.")
        
        mock_uploads_dir = "./data/uploads"
        os.makedirs(mock_uploads_dir, exist_ok=True)
        
        calls_to_create = []
        
        for c_info in calls_to_create:
            mock_path = os.path.join(mock_uploads_dir, c_info["filename"])
            with open(mock_path, "wb") as f:
                f.write(b"MOCK_AUDIO_DATA_FOR_SEED")
                
            db_call = Call(
                filename=c_info["filename"],
                advisor_id=c_info["adv"].id,
                team_id=c_info["adv"].team_id,
                organization_id=org.id,
                customer_id=c_info["cust"].id,
                source="folder",
                audio_path=mock_path,
                status="processing"
            )
            db.add(db_call)
            db.commit()
            db.refresh(db_call)
            
            process_call_pipeline(db_call.id, SessionLocal)
            
        print("Completed processing seeded calls.")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
