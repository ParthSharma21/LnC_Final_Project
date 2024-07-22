from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyzeSentiment(comment):
    analyzer = SentimentIntensityAnalyzer()
    sentimentDict = analyzer.polarity_scores(comment)
    
    # Determine sentiment based on compound score
    # if sentimentDict['compound'] >= 0.5:
    #     # print(sentimentDict['compound'])
    #     sentiment = "Positive"
    # elif sentimentDict['compound'] <= -0.5:
    #     # print(sentimentDict['compound'])
    #     sentiment = "Negative"
    # else:
    #     # print(sentimentDict['compound'])
    #     sentiment = "Neutral"
    
    return sentimentDict['compound'] # sentiment

# comment = 'The parathas were amazing'
# print(analyzeSentiment(comment))  

# comment = "This is the worst experience I've ever had."
# print(analyzeSentiment(comment))  
