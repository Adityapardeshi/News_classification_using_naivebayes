from flask import Flask, request, render_template
import pickle
import requests
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB



dataset = pd.read_csv('BBC News Train.csv')
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


clf = MultinomialNB()
clf.fit(X, y)


# Load the saved model
with open('newsmodel.pkl', 'rb') as file:
    clf = pickle.load(file)

#Input as a News Headline
#text = input("Enter your News: ")


# text = re.sub(r'<[^>]*>', '', text) # Remove HTML tags
# text = re.sub('[^a-zA-Z0-9\s]', '', text) # Remove special characters
# text = text.lower() # Convert to lowercase
# text = ' '.join([word for word in word_tokenize(text) if word not in stop_words]) # Remove stopwords
# text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(text)]) # Lemmatize words
# X_test = vectorizer.transform([text])
# y_pred = clf.predict(X_test)












