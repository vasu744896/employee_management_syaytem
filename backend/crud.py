from sqlalchemy.orm import Session
from models import Employee  # Ensure that this points to your models file correctly
from schemas import EmployeeCreate


# Create a new employee
def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        employee_id=employee.employee_id,
        phone=employee.phone,
        department=employee.department,
        manager_id=employee.manager_id,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# Get all employees
def get_employees(db: Session):
    return db.query(Employee).all()
