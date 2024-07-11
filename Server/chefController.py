import RecommendationEngine.RecommendationEngine as re
import Server.serverFunctions as sf
import Server.detailedReviewHandler as drh

def getRecommendedFoodItems():
    return re.getRecommendedFoodItems()

def rolloutMenu(request_data):
    return sf.rolloutMenu(request_data)

def notifyEmployees(request_data):
    return sf.notifyEmployees(request_data)

def generateReport():
    return sf.generateReport()

def getPoorPerformingItems(request_data):
    return drh.get_poor_performing_items(request_data.get('threshold', 2), request_data.get('days', 30))

def discardFoodItem(request_data):
    return drh.discard_food_item(request_data)

def requestDetailedReview(request_data):
    return drh.request_detailed_review(request_data)
