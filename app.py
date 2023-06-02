from flask import Flask, render_template, request, session, redirect, url_for
from model import user_model
import requests
import json
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
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
                    categories = None
       
    else: 
        return redirect('/login')

    top_url = "https://newsapi.org/v2/top-headlines?country=in&pageSize=100&apiKey=86b9cef2935244629fd8d031b95e6cc2"
    response = requests.get(top_url)
    top_articles = response.json()['articles']
    

    trend_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=86b9cef2935244629fd8d031b95e6cc2"
    response1 = requests.get(trend_url)
    trend_articles = response1.json()['articles']

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


    session['age'] = obj.get_age()

    # Load the pickled model
    pickled_model = pickle.load(open('newsmodel.pkl', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

    with open('newscontent.json','r+') as content:
        headlines = json.load(content)

    index = 0
    indexes = []
    crime_indexes = []    
    for headline in headlines:
        if headline['content'] == None :
            index = index + 1
            continue
        text = headline['content']
        index = index + 1

        # text = "Age is just a number for Ashish Vidyarthi! Actor gets married for the second time at 60"
        text = re.sub(r'<[^>]*>', '', text)  # Remove HTML tags
        text = re.sub('[^a-zA-Z0-9\s]', '', text)  # Remove special characters
        text = text.lower()  # Convert to lowercase
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        text = ' '.join([word for word in word_tokenize(text) if word not in stop_words])  # Remove stopwords
        text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(text)])  # Lemmatize words

        # Vectorize the preprocessed input
        X_test = vectorizer.transform([text])  # Transform the test input using the trained vectorizer
        output = pickled_model.predict(X_test)
        
        if categories != None:
            for category in categories:
                if category == output[0]:
                    indexes.append(index)
        else:
            if session['age']<18 and output[0] != 'Crime':  #if age is less than 18 do not show crime news
                indexes.append(index)
            else:
                indexes.append(index)
            if output[0]=='Crime':
                crime_indexes.append(index)

        
    #get other news data
    other_indexes = []
    for i in range (len(indexes)):
        if session['age']<18:
            if(i!=indexes[i] and i not in crime_indexes):
                other_indexes.append(i)
        else:
            if(i!=indexes[i]):
                other_indexes.append(i)
            

    def update_json(id, new_index):
        with open('indexes.json', 'r+') as file:
            json_data = json.load(file)
            index_data = json_data['indexData']
            for data in index_data:
                if data['id'] == id:
                    data['index'] = indexes
                    file.seek(0)  # Move the file pointer to the beginning
                    json.dump(json_data, file, indent=4)
                    file.truncate()  # Remove any remaining content
                    return

            # If id not found, create a new object
            index_data.append(new_index)
            file.seek(0)  # Move the file pointer to the beginning
            json.dump(json_data, file, indent=4)
            file.truncate()
    

    indexData = {"id": session['email'],
                "index": indexes}

    update_json(session["email"], indexData)           

    #select only those article which are related to user
    def getindex():
        with open('indexes.json', 'r') as file:
            # data_of_file = None
            json_data = json.load(file)
            index_data = json_data['indexData']
            for data in index_data:
                if data['id'] == session['email']:
                    return data['index']

    news = []
    data = getindex()
    for d in data:
        news.append(top_articles[d-1])
    # print(news)

    other_data = []
    for i in other_indexes:
        other_data.append(top_articles[i-1])
        
    return render_template("news.html", top_articles=news, trend_articles=other_data)


@app.route('/select_interests', methods=["GET", "POST"])
def select_interests():
    if request.method=='POST':
        return obj.select_interests(request.form)
    else:
         with open("sample.json", 'r+') as file:
            file_data = json.load(file)
            for i in range(len(file_data["userPreference"])):
                if file_data["userPreference"][i]['email'] == session['email']:
                    return render_template("select_interests.html", categories=file_data["userPreference"][i]['categories'])

    return render_template("select_interests.html")


@app.route('/logout', methods=["POST"])
def logout():
    session.pop('email', None)
    session.pop('age', None)
    return redirect(url_for('index'))


@app.route('/test1', methods = ["GET"])
def test():
    res = requests.get("https://newsapi.org/v2/top-headlines?country=in&pageSize=100&apiKey=86b9cef2935244629fd8d031b95e6cc2")
    data = res.json()
    return data



if __name__ == '__main__':
    app.run(host= "127.0.0.1", port=6500, debug=True)
