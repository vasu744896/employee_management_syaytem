from pydantic import BaseModel, EmailStr
from typing import Optional

# Employee model
class Employee(BaseModel):
    id: Optional[int]  # Employee ID (will be assigned automatically by DB)
    name: str  # Full name of the employee
    email: EmailStr  # Email address (valid email format)
    phone_number: str  # Phone number of the employee
    manager_id: Optional[int]  # The ID of the manager, nullable
    department: str  # The department the employee belongs to
    
    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models (like SQLAlchemy)

# To be used when creating or updating an employee
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    manager_id: Optional[int] = None  # Manager can be assigned later or left as None
    department: str

# To be used when updating an existing employee
class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    manager_id: Optional[int] = None
    department: Optional[str] = None

# Example of how a response model could look
class EmployeeResponse(Employee):
    pass
