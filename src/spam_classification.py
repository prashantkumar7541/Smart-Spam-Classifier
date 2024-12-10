# -*- coding: utf-8 -*-
"""spam-classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cA9R0l1ixAPRxUeu9wEmWZpnLbS3P22y
"""

print("hello world")

import pandas as pd

# Load the dataset
data = pd.read_csv('/spam.csv')  # Replace with the actual path of your dataset
print(data.head())

import re
from nltk.corpus import stopwords

# Download stopwords from NLTK if you haven't already
import nltk
nltk.download('stopwords')

# Define a function to clean the emails
def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert text to lowercase
    text = text.lower()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Apply cleaning function to the 'Email' column
data['cleaned_text'] = data['Email'].apply(clean_text)
print(data.head())

from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=3000)

# Convert the cleaned text to numerical features
X = vectorizer.fit_transform(data['cleaned_text']).toarray()
y = data['label']  # Assuming the label column is named 'label' (spam = 1, ham = 0)

from sklearn.model_selection import train_test_split

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.naive_bayes import MultinomialNB

# Initialize and train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Predict on the test set
y_pred = model.predict(X_test)

# Print performance metrics
print('Accuracy:', accuracy_score(y_test, y_pred))
print('Classification Report:\n', classification_report(y_test, y_pred))
print('Confusion Matrix:\n', confusion_matrix(y_test, y_pred))

import seaborn as sns
import matplotlib.pyplot as plt

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()