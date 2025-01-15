# schemas.py
from pydantic import BaseModel, EmailStr, condecimal
from typing import Optional

# EmployeeCreate schema for adding a new employee
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    manager_id: Optional[int] = None  # Optional field for manager reference
    department: str

    class Config:
        orm_mode = True

# Employee schema for responding with employee data (excluding sensitive fields)
class Employee(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    manager_id: Optional[int] = None
    department: str

    class Config:
        orm_mode = True

# EmployeeUpdate schema for updating employee details
class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    manager_id: Optional[int] = None
    department: Optional[str] = None

    class Config:
        orm_mode = True

# EmployeeDelete schema for deletion (this could just be a response message)
class EmployeeDelete(BaseModel):
    message: str

    class Config:
        orm_mode = True
