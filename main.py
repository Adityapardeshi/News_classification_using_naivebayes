from flask import Flask, request, render_template
import requests
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Load the dataset and preprocess the text
dataset = pd.read_csv('/Users/Himanshu/Documents/BBC News Train.csv')
dataset['Text'] = dataset['Text'].apply(lambda x: re.sub(r'<[^>]*>', '', x)) # Remove HTML tags
dataset['Text'] = dataset['Text'].apply(lambda x: re.sub('[^a-zA-Z0-9\s]', '', x)) # Remove special characters
dataset['Text'] = dataset['Text'].apply(lambda x: x.lower()) # Convert to lowercase
stop_words = set(stopwords.words('english'))
dataset['Text'] = dataset['Text'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word not in stop_words])) # Remove stopwords
lemmatizer = WordNetLemmatizer()
dataset['Text'] = dataset['Text'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(x)])) # Lemmatize words
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(dataset['Text'])
y = dataset['Category']

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X, y)

# Define the home page where the user can input the news text
@app.route('/')
def home():
    return render_template('index.html')

# Define a function that preprocesses the user input and returns the predicted news category
def predict_category(text):
    text = re.sub(r'<[^>]*>', '', text) # Remove HTML tags
    text = re.sub('[^a-zA-Z0-9\s]', '', text) # Remove special characters
    text = text.lower() # Convert to lowercase
    text = ' '.join([word for word in word_tokenize(text) if word not in stop_words]) # Remove stopwords
    text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(text)]) # Lemmatize words
    X_test = vectorizer.transform([text])
    y_pred = clf.predict(X_test)
    return y_pred[0]

# Define the prediction page that displays the predicted news category
@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    category = predict_category(text)
    return render_template('predict.html', category=category)

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        # Get the selected category from the form
        category = request.form['category']
        
        # Fetch the news articles from the selected category using NewsAPI.org
        api_key = 'ac07102a9c124e568188d0e8bceb3a64'
        # url = 'https://newsapi.org/v2/top-headlines?country=india&category='category'&apiKey=ac07102a9c124e568188d0e8bceb3a64'
        # response = requests.get(url)
        # articles = response.json()['articles']
        
        # Render the news articles template with the fetched articles
        # return render_template('articles.html', articles=articles)
    
    # Render the index template with the news categories
    return render_template('api.html')

if __name__ == '__main__':
    app.run(debug=True)


w
if __name__ == '__main__':
    app.run(debug=True)
