import Server.serverFunctions as sf
import Server.detailedReviewHandler as drh
import employeeService as es

def viewDailyMenu(requestData):
    return es.handleViewDailyMenu(requestData)

def viewNotifications():
    return es.handleViewNotifications()

def orderFood(requestData):
    return es.handleOrderFood(requestData)

def giveFeedback(requestData):
    return es.handleGiveFeedback(requestData)

def requestFeedbackItems(requestData):
    return es.handleRequestFeedbackItems(requestData)

def checkDetailedFeedback(requestData):
    return drh.checkDetailedFeedback(requestData)

def submitDetailedFeedback(requestData):
    return drh.submitDetailedFeedback(requestData)
