import pickle
import spacy

from sklearn.feature_extraction.text import CountVectorizer

# Load the pre-trained ML model
with open('/Users/liamtwomey/Desktop/my_project_V2/models/pre-trained-model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load Spacy model for text preprocessing
nlp = spacy.load('en_core_web_sm')

# Define pre-processing function
def preprocess(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove trailing and leading whitespaces
    text = text.strip()

    # Replace contractions
    text = text.replace("n't", " not").replace("'s", " is").replace("'m", " am").replace("'re", " are")\
               .replace("'d", " would").replace("'ll", " will").replace("'ve", " have")

    # Remove punctuations
    text = ''.join(c for c in text if c not in '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')

    # Remove extra whitespaces
    text = ' '.join(text.split())

    # Lemmatize text
    doc = nlp(text)
    lemmatized_tokens = [token.lemma_ for token in doc]
    text = ' '.join(lemmatized_tokens)

    return text

# Example input data
visit_reason = "I have a fever and a headache"
symptoms = "I feel tired and my throat hurt"

# Preprocess the input text
visit_reason = preprocess(visit_reason)
symptoms = preprocess(symptoms)

# Initialize the BoW vectorizer
vectorizer = CountVectorizer()

# Fit the vectorizer with example data
corpus = [
    "I have a fever and a headache",
    "I feel tired and my throat hurts"
]
vectorizer.fit_transform([preprocess(doc) for doc in corpus])

# Vectorize the input text
X = vectorizer.transform([visit_reason, symptoms])

# Make the prediction
prediction = model.predict(X)[0]

print("Prediction:", prediction)
