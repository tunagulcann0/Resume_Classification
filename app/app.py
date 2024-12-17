from pymongo import MongoClient

def fetch_single_resume():
    client = MongoClient('mongodb://localhost:27017')
    db = client['Resume_Classification']
    collection = db['resumes']

    resume = collection.find_one()
    return resume

if __name__ == "__main__":
    resume = fetch_single_resume()
    print("Veritabanından çekilen tek veri:")
    for key, value in resume.items():
        print(f"{key}: {value}")



