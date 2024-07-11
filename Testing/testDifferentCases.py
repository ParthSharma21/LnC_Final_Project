import unittest
import socket
import json
import threading
import Server.server as server
import Client.classes as classes

# Server host and port
HOST = '127.0.0.1'
PORT = 12345

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=server.start_server, daemon=True)
        cls.server_thread.start()

    def setUp(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

    def tearDown(self):
        self.client.close()

    def login(self, user_type, user_id, password):
        user = {"action": "login", "userType": user_type, "userID": user_id, "password": password}
        self.client.send(json.dumps(user).encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        return json.loads(response)

    def test_admin_login(self):
        response = self.login(1, "1", "1234")
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)
        print("Admin login successful")

    def test_chef_login(self):
        response = self.login(2, "2", "1234")
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)
        print("Chef login successful")

    def test_employee_login(self):
        response = self.login(3, "3", "1234")
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)
        print("Employee login successful")

    def test_another_employee_login(self):
        response = self.login(3, "5", "1234")
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)
        print("Another employee login successful")

    def test_add_food_item(self):
        self.login(1, "1", "1234")
        request = {"action": "addFoodItem", "foodItemName": "Pizza", "foodItemPrice": 15}
        self.client.send(json.dumps(request).encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        print("Add food item successful")

    def test_view_menu(self):
        self.login(1, "1", "1234")
        request = {"action": "viewMenu"}
        self.client.send(json.dumps(request).encode('utf-8'))
        response = self.client.recv(4096).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        self.assertTrue(len(response["data"]) > 0)
        print("View menu successful")

    def test_rollout_menu(self):
        self.login(2, "2", "1234")
        request = {"action": "getRecommendedFoodItems"}
        self.client.send(json.dumps(request).encode('utf-8'))
        response = self.client.recv(4096).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        recommended_items = response["data"]
        self.assertTrue(len(recommended_items) > 0)
        print("Get recommended food items successful")

        items_to_rollout = [item['foodItemID'] for item in recommended_items]
        request = {"action": "rolloutMenu", "foodItemIDs": items_to_rollout}
        self.client.send(json.dumps(request).encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        print("Rollout menu successful")

    def test_order_food(self):
        self.login(3, "3", "1234")
        request = {"action": "viewDailyMenu", "userID": "3"}
        self.client.send(json.dumps(request).encode('utf-8'))
        response = self.client.recv(4096).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        daily_menu = response["data"]
        self.assertTrue(len(daily_menu) > 0)
        print("View daily menu successful")

        food_item_ids = [item[0] for item in daily_menu]
        request = {"action": "orderFood", "foodItemIDs": food_item_ids, "userID": "3"}
        self.client.send(json.dumps(request).encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        print("Order food successful")

    def test_provide_feedback(self):
        self.login(3, "3", "1234")
        request = {"action": "requestFeedbackItems", "userID": "3"}
        self.client.send(json.dumps(request).encode('utf-8'))
        response = self.client.recv(4096).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        items_to_feedback = response["data"]
        self.assertTrue(len(items_to_feedback) > 0)
        print("Request feedback items successful")

        for item in items_to_feedback:
            feedback_request = {
                "action": "giveFeedback",
                "foodItemID": item['FoodItemID'],
                "rating": 4,
                "comments": "Good",
                "userID": "3"
            }
            self.client.send(json.dumps(feedback_request).encode('utf-8'))
            feedback_response = self.client.recv(1024).decode('utf-8')
            feedback_response = json.loads(feedback_response)
            self.assertEqual(feedback_response["status"], "success")
            print(f"Feedback for {item['FoodItemName']} submitted successfully")

    def test_update_profile(self):
        self.login(3, "3", "1234")
        profile_data = {
            "action": "updateProfile",
            "userID": "3",
            "foodType": "1",
            "spiceLevel": "2",
            "cuisineType": "1",
            "sweetPreference": "1"
        }
        self.client.send(json.dumps(profile_data).encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        response = json.loads(response)
        self.assertEqual(response["status"], "success")
        print("Profile updated successfully")

if __name__ == "__main__":
    testingSuite = unittest.TestLoader().loadTestsFromTestCase(TestApp)
    result = unittest.TextTestRunner(verbosity=2).run(testingSuite)
    
    print("\nSummary of Test Results:")
    print(f"Total tests run: {result.testsRun}")
    print(f"Total tests failed: {len(result.failures)}")
    print(f"Total tests errors: {len(result.errors)}")
