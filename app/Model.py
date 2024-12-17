import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import shuffle


class TextClassificationModel:
    def __init__(self, file_path, max_features=2000, test_size=0.2, random_state=42, min_samples=2):
        self.file_path = file_path
        self.max_features = max_features
        self.test_size = test_size
        self.random_state = random_state
        self.min_samples = min_samples
        self.vectorizer = None
        self.model = None
        self.cleaned_texts = None
        self.labels = None
        self.tfidf_matrix = None

    def load_data(self):

        try:
            data = pd.read_csv(self.file_path)
            if 'cleaned_text' not in data.columns or 'cleaned_labels' not in data.columns:
                raise KeyError("Dosyada 'cleaned_text' veya 'cleaned_labels' sütunu bulunamadı.")
            self.cleaned_texts = data['cleaned_text']
            self.labels = data['cleaned_labels']

            label_counts = self.labels.value_counts()
            print("Sınıf Dağılımı:\n", label_counts)

            valid_labels = label_counts[label_counts >= self.min_samples].index
            self.cleaned_texts = self.cleaned_texts[self.labels.isin(valid_labels)].reset_index(drop=True)
            self.labels = self.labels[self.labels.isin(valid_labels)].reset_index(drop=True)
            print(f"{len(label_counts) - len(valid_labels)} sınıf çıkarıldı. Kalan sınıflar: {len(valid_labels)}")
        except Exception as e:
            print(f"Veri yükleme sırasında hata oluştu: {e}")
            raise

    def extract_features(self):

        try:
            self.vectorizer = TfidfVectorizer(max_features=self.max_features)
            self.tfidf_matrix = self.vectorizer.fit_transform(self.cleaned_texts)
            print(f"TF-IDF özellikleri başarıyla çıkarıldı. Özellik sayısı: {self.tfidf_matrix.shape[1]}")
        except Exception as e:
            print(f"Özellik çıkarımı sırasında hata oluştu: {e}")
            raise

    def split_data(self):

        try:
            num_classes = len(self.labels.unique())
            min_test_size = num_classes / len(self.labels)

            if self.test_size < min_test_size:
                print(f"Test seti boyutu çok küçük. Test seti minimum {min_test_size * 100:.2f}% olarak ayarlandı.")
                self.test_size = min_test_size + 0.1

            X_train, X_test, y_train, y_test = train_test_split(
                self.tfidf_matrix,
                self.labels,
                test_size=self.test_size,
                random_state=self.random_state,
                stratify=self.labels
            )
            print(f"Veriler başarıyla ayrıldı: Eğitim seti: {X_train.shape[0]}, Test seti: {X_test.shape[0]}")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            print(f"Veri ayırma sırasında hata oluştu: {e}")
            raise

    def train_model(self, X_train, y_train):

        try:
            self.model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=self.random_state)
            self.model.fit(X_train, y_train)
            print("Model başarıyla eğitildi.")
        except Exception as e:
            print(f"Model eğitimi sırasında hata oluştu: {e}")
            raise

    def evaluate_model(self, X_test, y_test):

        try:
            y_pred = self.model.predict(X_test)
            print("\nModel Değerlendirme Sonuçları:")
            print(classification_report(y_test, y_pred, zero_division=0))
            print(f"Doğruluk: {accuracy_score(y_test, y_pred) * 100:.2f}%")
        except Exception as e:
            print(f"Model değerlendirme sırasında hata oluştu: {e}")
            raise


if __name__ == "__main__":
    try:
        model = TextClassificationModel(file_path='cleaned_text.csv')

        model.load_data()

        model.extract_features()

        X_train, X_test, y_train, y_test = model.split_data()

        model.train_model(X_train, y_train)

        model.evaluate_model(X_test, y_test)

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
