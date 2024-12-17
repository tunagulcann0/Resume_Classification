from pymongo import MongoClient
import pandas as pd

def load_data():
    client = MongoClient('mongodb://localhost:27017')
    db = client['Resume_Classification']
    collection = db['resumes']

    resumes = list(collection.find())
    data = pd.DataFrame(resumes)
    return data

def prepare_data(data):
    selected_columns = ['summary', 'experience', 'skills', 'labels', 'education']
    data = data[selected_columns]

    data = data.fillna('')

    data['education'] = data['education'].apply(
        lambda x: " ".join([f"{edu['degree']} {edu['institution']}" for edu in x]) if isinstance(x, list) else ''
    )

    data['experience'] = data['experience'].apply(
        lambda x: " ".join([f"{exp['position']} {exp['company']} ({exp['duration']})" for exp in x]) if isinstance(x, list) else ''
    )

    data['skills'] = data['skills'].apply(
        lambda x: " ".join(x) if isinstance(x, list) else ''
    )

    return data

if __name__ == "__main__":
    raw_data = load_data()

    prepared_data = prepare_data(raw_data)

    print("Hazırlanan veri:")
    print(prepared_data.head())

    prepared_data.to_csv('prepared_data.csv', index=False)
    print("Veri hazırlanıp 'prepared_data.csv' dosyasına kaydedildi.")
