from flask import Flask, render_template, request, jsonify
import pickle
import spacy

from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

# Load the pre-trained ML model
with open('/Users/liamtwomey/Desktop/my_project_V2/models/pre-trained-model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load Spacy model for text preprocessing
nlp = spacy.load('en_core_web_sm')

# Initialize the BoW vectorizer
vectorizer = CountVectorizer()

# Define the route for the form display
@app.route('/')
def form():
    return render_template('form.html')

# Define the route for the form submission
@app.route('/', methods=['POST'])
def predict():
    # Get the form data
    visit_reason = request.form['visit_reason']
    symptoms = request.form['symptoms']
    
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
    
    # Preprocess the input text
    visit_reason = preprocess(visit_reason)
    symptoms = preprocess(symptoms)
    
    # Vectorize the input text
    X = vectorizer.transform([visit_reason, symptoms])
    
    # Make the prediction
    prediction = model.predict(X)[0]
    
    # Display the classification result as a pop-up message
    return jsonify({'classification': prediction})

if __name__ == '__main__':
    app.run(debug=True)
