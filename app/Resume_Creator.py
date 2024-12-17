from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient("mongodb://localhost:27017/")
db = client["Resume_Classification"]

def add_resume(name, gender, birth_date, summary, experience, education, skills, certifications, labels, location):
    resume = {
        "name": name,
        "gender": gender,
        "birth_date": birth_date,
        "summary": summary,
        "experience": experience,
        "education": education,
        "skills": skills,
        "certifications": certifications,
        "location": location,
        "labels": labels,
        "updated_date": datetime.now(timezone.utc)
    }
    db.resumes.insert_one(resume)
    print("CV başarıyla eklendi.")

add_resume(
    name="Mehmet Yıldız",
    gender="Male",
    birth_date="1990-09-25",
    summary="Sales representative specializing in B2C consumer electronics and customer acquisition.",
    experience=[
        {"position": "Sales Representative", "company": "TechMart Ltd.", "duration": "6 years"},
        {"position": "Customer Engagement Specialist", "company": "RetailPro", "duration": "3 years"}
    ],
    education=[
        {"degree": "BBA in Marketing", "institution": "Marmara University", "year": 2012}
    ],
    skills=["Consumer Electronics Sales", "Customer Acquisition", "Lead Generation"],
    certifications=["Certified Sales Professional"],
    location="Ankara",
    labels=["Sales group", "Consumer electronics", "Customer acquisition"]
)



