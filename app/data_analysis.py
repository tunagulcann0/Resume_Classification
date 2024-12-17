import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pymongo import MongoClient
import pandas as pd


def load_data():
    client = MongoClient('mongodb://localhost:27017')
    db = client['Resume_Classification']
    collection = db['resumes']

    resumes = list(collection.find())
    data = pd.DataFrame(resumes)
    return data


def plot_class_distribution(data):
    plt.figure(figsize=(10, 6))
    data['labels'].explode().value_counts().plot(kind='bar', color='skyblue')
    plt.title('Sınıf Dağılımı', fontsize=16)
    plt.xlabel('Sınıf', fontsize=14)
    plt.ylabel('Örnek Sayısı', fontsize=14)
    plt.xticks(rotation=45)
    plt.show()


def generate_wordcloud(data):
    text_all = " ".join(
        data['summary'].fillna("") + " " +
        data['experience'].apply(lambda x: " ".join(
            [f"{exp['position']} {exp['company']}" for exp in x]) if isinstance(x, list) else "") + " " +
        data['skills'].apply(lambda x: " ".join(x) if isinstance(x, list) else "")
    )

    top_classes = data['labels'].explode().value_counts().head(20)

    plt.figure(figsize=(12, 6))
    top_classes.plot(kind='bar', color='skyblue')
    plt.title('En Yaygın 20 Sınıfın Dağılımı', fontsize=16)
    plt.xlabel('Sınıf', fontsize=14)
    plt.ylabel('Örnek Sayısı', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = load_data()

    print("Sınıf dağılımı grafiği hazırlanıyor...")
    plot_class_distribution(data)

    print("Kelime bulutu oluşturuluyor...")
    generate_wordcloud(data)
