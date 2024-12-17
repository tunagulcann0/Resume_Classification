import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):

    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = " ".join([word for word in text.split() if word not in stop_words])
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

def combine_and_clean_data(data):

    required_columns = ['summary', 'experience', 'skills', 'certifications', 'education', 'labels']
    for col in required_columns:
        if col not in data.columns:
            data[col] = ''

    data['cleaned_text'] = (
        data['summary'].fillna('') + ' ' +
        data['experience'].fillna('') + ' ' +
        data['skills'].fillna('') + ' ' +
        data['certifications'].fillna('') + ' ' +
        data['education'].fillna('')
    ).apply(clean_text)

    data['cleaned_labels'] = data['labels'].apply(clean_text)

    return data[['cleaned_text', 'cleaned_labels']]

def preprocess_csv(input_file='prepared_data.csv', output_file='cleaned_text.csv'):

    try:
        data = pd.read_csv(input_file)
        print(f"'{input_file}' dosyası başarıyla yüklendi.")

        print("Metin sütunları ve etiketler birleştiriliyor ve temizleniyor...")
        cleaned_data = combine_and_clean_data(data)

        cleaned_data.to_csv(output_file, index=False)
        print(f"Temizlenmiş veri '{output_file}' dosyasına kaydedildi.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    preprocess_csv()
