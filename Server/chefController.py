import RecommendationEngine.RecommendationEngine as re
import Server.serverFunctions as sf
import Server.detailedReviewHandler as drh
import Server.chefService as cs

def getRecommendedFoodItems():
    return re.getRecommendedFoodItems()

def rolloutMenu(requestData):
    return cs.rolloutMenu(requestData)

def notifyEmployees(requestData):
    return cs.notifyEmployees(requestData)

def generateReport():
    return cs.generateReport()

def getPoorPerformingItems(requestData):
    return drh.getPoorPerformingItems(requestData.get('threshold', 2), requestData.get('days', 30))

def discardFoodItem(requestData):
    return drh.discardFoodItem(requestData)

def requestDetailedReview(requestData):
    return drh.requestDetailedReview(requestData)
