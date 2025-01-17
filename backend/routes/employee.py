from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import create_employee, get_employees  # Make sure these functions are correctly imported
from schemas import EmployeeCreate, Employee
from database import SessionLocal

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