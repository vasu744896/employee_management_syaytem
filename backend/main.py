from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, constr
from typing import List, Optional
from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:8080",  # Frontend running at port 8080
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample Employee Data (In-memory storage)
employees_db = []

# Pydantic model for employee
class Employee(BaseModel):
    name: constr(pattern=r'^[A-Za-z ]+$')  # Only letters and spaces
    email: str
    employee_id: str
    phone: str
    manager_id: Optional[str] = None
    department: str

# Employee InDB model (with ID)
class EmployeeInDB(Employee):
    id: str

# Endpoint to add a new employee
@app.post("/employees/", response_model=EmployeeInDB)
async def add_employee(employee: Employee):
    # Check for unique employee_id
    if any(emp.employee_id == employee.employee_id for emp in employees_db):
        raise HTTPException(status_code=400, detail="Employee ID already exists.")
    # Check if email is unique
    if any(emp.email == employee.email for emp in employees_db):
        raise HTTPException(status_code=400, detail="Email already exists.")
    
    # Generate unique ID for employee
    employee_id = str(uuid4())
    new_employee = EmployeeInDB(id=employee_id, **employee.dict())
    employees_db.append(new_employee)
    return new_employee

# Endpoint to get an employee by ID
@app.get("/employees/{employee_id}", response_model=EmployeeInDB)
async def get_employee(employee_id: str):
    employee = next((emp for emp in employees_db if emp.id == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return employee

# Endpoint to list all employees with pagination
@app.get("/employees/", response_model=List[EmployeeInDB])
async def list_employees(skip: int = 0, limit: int = 10):
    return employees_db[skip: skip + limit]

# Endpoint to update employee details
@app.put("/employees/{employee_id}", response_model=EmployeeInDB)
async def update_employee(employee_id: str, employee: Employee):
    existing_employee = next((emp for emp in employees_db if emp.id == employee_id), None)
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    # Check for duplicate email and employee_id
    if any(emp.email == employee.email and emp.id != employee_id for emp in employees_db):
        raise HTTPException(status_code=400, detail="Email already exists.")
    if any(emp.employee_id == employee.employee_id and emp.id != employee_id for emp in employees_db):
        raise HTTPException(status_code=400, detail="Employee ID already exists.")

    # Update employee details
    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.employee_id = employee.employee_id
    existing_employee.phone = employee.phone
    existing_employee.manager_id = employee.manager_id
    existing_employee.department = employee.department
    return existing_employee

# Endpoint to delete an employee
@app.delete("/employees/{employee_id}", response_model=EmployeeInDB)
async def delete_employee(employee_id: str):
    employee = next((emp for emp in employees_db if emp.id == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    # Ensure the employee being deleted is not a manager or has subordinates
    if employee.manager_id:
        subordinates = [emp for emp in employees_db if emp.manager_id == employee.id]
        if subordinates:
            raise HTTPException(status_code=400, detail="Manager has subordinates. Reassign before deletion.")

    employees_db.remove(employee)
    return employee

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Management API"}
