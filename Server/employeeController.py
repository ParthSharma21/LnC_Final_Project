import Server.serverFunctions as sf
import Server.detailedReviewHandler as drh

def viewDailyMenu(request_data):
    return sf.handle_view_daily_menu(request_data)

def viewNotifications():
    return sf.handle_view_notifications()

def orderFood(request_data):
    return sf.handle_order_food(request_data)

def giveFeedback(request_data):
    return sf.handle_give_feedback(request_data)

def requestFeedbackItems(request_data):
    return sf.handle_request_feedback_items(request_data)

def checkDetailedFeedback(request_data):
    return drh.check_detailed_feedback(request_data)

def submitDetailedFeedback(request_data):
    return drh.submit_detailed_feedback(request_data)
