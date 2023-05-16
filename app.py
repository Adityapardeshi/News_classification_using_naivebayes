from flask import Flask, render_template, request, session, redirect, url_for
from model import user_model
import requests
import json
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


obj = user_model()
app = Flask(__name__)

app.secret_key = "newsx"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration', methods=["GET", "POST"])
def register():
    if request.method=='POST':
        return obj.register(request.form)
    else:
        return render_template("registration.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=='POST':
        return obj.login(request.form)
    else:
        return render_template("login.html")

@app.route('/news')
def home():
    if 'email' in session:
        print('logged in as '+session['email'])

        with open('sample.json','r') as f: #get the user preferences from json file
            data=json.load(f) 
            for i in range(len(data["userPreference"])):
                if data["userPreference"][i]['email'] == session['email']:
                    categories = data["userPreference"][i]['categories']
                    break;
       
    else: 
        return redirect('/login')

    top_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=86b9cef2935244629fd8d031b95e6cc2"
    response = requests.get(top_url)
    top_articles = response.json()['articles']
    

    trend_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=86b9cef2935244629fd8d031b95e6cc2"
    response1 = requests.get(trend_url)
    trend_articles = response1.json()['articles']
    # print(articles)

    #save news title into json file 
    extracted_data = []
    for article in top_articles:
        content = article['content']
        
        article_data = {
            'content': content
        }
        
        extracted_data.append(article_data)
    
    with open('newscontent.json', 'w') as f:
        json.dump(extracted_data, f)

    #Load model and predict category
    pickled_model = pickle.load(open('newsmodel.pkl', 'rb'))
    
    text = "Royal Challengers Bangalore put in arguably their finest performance of the season, bundling out Rajasthan Royals for just 59 runs while defending their total of 171 in an Indian Premier League"
    text = re.sub(r'<[^>]*>', '', text)  # Remove HTML tags
    text = re.sub('[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([word for word in word_tokenize(text) if word not in stop_words])  # Remove stopwords
    text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(text)])  # Lemmatize words

    # Vectorize the preprocessed input
    vectorizer = TfidfVectorizer()
    X_test = vectorizer.transform([text])

    output = pickled_model.predict(X_test)
    print(output)

    return render_template("news.html", top_articles=top_articles, trend_articles=trend_articles)

@app.route('/select_interests', methods=["GET", "POST"])
def select_interests():
    if request.method=='POST':
        return obj.select_interests(request.form)
    else:
        return render_template("select_interests.html")



if __name__ == '__main__':
    app.run(host= "127.0.0.1", port=6500, debug=True)
