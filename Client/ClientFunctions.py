import adminFunctions as af
import chefFunctions as cf
import employeeFunctions as ef

def adminHandler(adminUser, client):
    af.adminHandler(adminUser, client)

def chefHandler(chefUser, client):
    cf.chefHandler(chefUser, client)

def employeeHandler(employeeUser, client):
    ef.employeeHandler(employeeUser, client)
