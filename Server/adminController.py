import Server.serverFunctions as sf
import adminService

def handleAddFoodItem(requestData):
    return adminService.handleAddFoodItem(requestData)

def handleUpdateFoodItem(requestData):
    return adminService.handleUpdateFoodItem(requestData)

def handleDeleteFoodItem(requestData):
    return adminService.handleDeleteFoodItem(requestData)

def handleViewMenu():
    return adminService.handleViewMenu()
