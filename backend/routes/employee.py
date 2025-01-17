from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import create_employee, get_employees  # Make sure these functions are correctly imported
from schemas import EmployeeCreate, Employee
from database import SessionLocal
from pydantic import BaseModel
from typing import Optional

# Pydantic model for request data (for POST, PUT requests)
class Employee(BaseModel):
    name: str
    email: str
    employee_id: str
    phone: str
    manager_id: Optional[str] = None
    department: Optional[str] = None

# Pydantic model for the data you return (e.g., after insertion, updating)
class EmployeeInDB(Employee):
    id: int


router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create a new employee
@router.post("/employees/", response_model=Employee)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db=db, employee=employee)

# Route to get all employees
@router.get("/employees/", response_model=list[Employee])
def read_employees(db: Session = Depends(get_db)):
    return get_employees(db=db)