from flask import Flask, render_template, request
from model import user_model
import requests

obj = user_model()
app = Flask(__name__)


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
    top_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=86b9cef2935244629fd8d031b95e6cc2"
    response = requests.get(top_url)
    top_articles = response.json()['articles']

    trend_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=86b9cef2935244629fd8d031b95e6cc2"
    response1 = requests.get(trend_url)
    trend_articles = response1.json()['articles']
    # print(articles)
    return render_template("news.html", top_articles=top_articles, trend_articles=trend_articles)

@app.route('/categories')
def categories():
    return render_template("select_interests.html")


@app.route('/getdata')
def hello_world():
    
    return obj.user_signup()

if __name__ == '__main__':
    app.run(host= "127.0.0.1", port=6500)
