from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(comment):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_dict = analyzer.polarity_scores(comment)
    
    # Determine sentiment based on compound score
    if sentiment_dict['compound'] >= 0.05:
        sentiment = "Positive"
    elif sentiment_dict['compound'] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment

# Example usage
# comment = "I love this product! It's amazing."
# print(analyze_sentiment(comment))  # Output: Positive

# comment = "This is the worst experience I've ever had."
# print(analyze_sentiment(comment))  # Output: Negative

# comment = "It's okay, not great but not terrible either."
# print(analyze_sentiment(comment))  # Output: Neutral
