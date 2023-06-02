import os
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

# Load the BBC News Train Dataset
data_path = 'BBC News Train.csv'
df = pd.read_csv(data_path)

# Extract the text column from the dataset
texts = df['Text'].tolist()

# Preprocess the text (if needed)
# ...

# Vectorize the text using TF-IDF
vectorizer = TfidfVectorizer(max_features=10000)
X = vectorizer.fit_transform(texts)

# Train the Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X, df['Category'])

# Transform the training data into topic space
topic_vectors = classifier.feature_log_prob_

# Normalize the topic vectors
topic_vectors_norm = normalize(topic_vectors, norm='l2', axis=1)

def recommend(text, n=5):
    # Preprocess the input text (if needed)
    # ...

    # Vectorize the input text
    input_vec = vectorizer.transform([text])

    # Predict the topic probabilities for the input text
    input_topic_probs = classifier.predict_log_proba(input_vec)

    # Normalize the input topic probabilities
    input_topic_probs_norm = normalize(input_topic_probs, norm='l2', axis=1)

    # Calculate cosine similarity between input vector and topic vectors
    similarities = cosine_similarity(input_topic_probs_norm, topic_vectors_norm[:, :input_topic_probs_norm.shape[1]])

    # Get the indices of the most similar documents
    indices = np.argsort(similarities, axis=1)[:, ::-1][:, :n]

    # Retrieve the recommended texts
    recommended_texts = [texts[idx] for idx in indices[0]]

    return recommended_texts

# Example usage
rawtext = """
IPL 2023 cup won by Chennai Super Kings! What a batting from Ravindra Jadeja.
"""

recommended_texts = recommend(rawtext, n=5)

for i, doc in enumerate(recommended_texts):
    print('Result #%s' % (i + 1))
    print('Text:\n')
    print(doc[:500])
    print()
