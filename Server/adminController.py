import Server.serverFunctions as sf

def handle_add_food_item(request_data):
    return sf.handle_add_food_item(request_data)

def handle_update_food_item(request_data):
    return sf.handle_update_food_item(request_data)

def handle_delete_food_item(request_data):
    return sf.handle_delete_food_item(request_data)

def handle_view_menu():
    return sf.handle_view_menu()
