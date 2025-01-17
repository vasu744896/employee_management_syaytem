from fastapi.testclient import TestClient
from .main import app  # Replace with your actual FastAPI app

client = TestClient(app)
def test_add_employee():
    # test code here
    # Define the test data
    employee_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "employee_id": "E12345",
        "phone_number": "+1234567890",
        "manager_assignment": "Manager ID",
        "department_assignment": "Department Name"
    }
    
    # Send a POST request to your endpoint
    response = client.post("/add_employee/", json=employee_data)

    # Check the status code
    assert response.status_code == 200

    # Check if the employee is added (customize as needed based on response)
    assert response.json()["employee_id"] == "E12345"
