# sentiment_analysis_model.py

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
from food_comments_data import comments, labels

# Convert labels to numpy array
labels = np.array(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(comments, labels, test_size=0.2, random_state=42)

# Create a TfidfVectorizer to convert text to numerical features
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train a Linear Support Vector Classifier
classifier = LinearSVC()
classifier.fit(X_train_vectorized, y_train)

# Make predictions on the test set
y_pred = classifier.predict(X_test_vectorized)

# Print the accuracy and classification report
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Negative', 'Neutral', 'Positive']))

# Function to predict sentiment for new comments
def predict_sentiment(comment):
    vectorized_comment = vectorizer.transform([comment])
    prediction = classifier.predict(vectorized_comment)
    if prediction[0] == 0:
        return "Negative"
    elif prediction[0] == 1:
        return "Neutral"
    else:
        return "Positive"

# Test the model with new comments
new_comments = [
    "The food was okay, but the service was slow",
    "Absolutely amazing experience, will definitely come back!",
    "Not worth the price, wouldn't recommend",
    "It was fine, nothing special",
    "Decent food, good prices, nice ambiance"
]

for comment in new_comments:
    print(f"Comment: '{comment}'")
    print(f"Predicted sentiment: {predict_sentiment(comment)}\n")