from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, constr
from typing import List, Optional
from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Set up the database URL (SQLite)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Using async SQLite

# Set up the database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Set up the sessionmaker
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Set up the base class for SQLAlchemy models
Base = declarative_base()

# Define the Employee model
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    department = Column(String)
    manager_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))

    manager = relationship("Employee", remote_side=[id], backref="subordinates")

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


app = FastAPI()

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Pydantic model for employee
class EmployeeCreate(BaseModel):
    name: str
    email: str
    employee_id: str
    phone: str
    manager_id: Optional[str] = None
    department: str

class EmployeeInDB(EmployeeCreate):
    id: int


# Database initialization (Create tables)
async def init_db():
    async with engine.begin() as conn:
        # Create the tables
        await conn.run_sync(Base.metadata.create_all)

# Call init_db() on startup
@app.on_event("startup")
async def on_startup():
    await init_db()

# Endpoint to add a new employee (store in SQLite database)
@app.post("/employees/", response_model=EmployeeInDB)
async def add_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    db_employee = Employee(
        employee_id=employee.employee_id,
        name=employee.name,
        email=employee.email,
        phone=employee.phone,
        department=employee.department,
        manager_id=employee.manager_id,
    )
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

# Endpoint to get an employee by ID (from the database)
@app.get("/employees/{employee_id}", response_model=EmployeeInDB)
async def get_employee(employee_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).filter(Employee.employee_id == employee_id))
    employee = result.scalars().first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.get("/employees/", response_model=List[EmployeeInDB])
async def list_employees(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee))
    employees = result.scalars().all()
    return employees




# Endpoint to update an employee (store in SQLite database)
@app.put("/employees/{employee_id}", response_model=EmployeeInDB)
async def update_employee(employee_id: str, employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).filter(Employee.employee_id == employee_id))
    existing_employee = result.scalars().first()
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    # Check for duplicate email and employee_id
    if await db.execute(select(Employee).filter(Employee.email == employee.email).filter(Employee.id != existing_employee.id)).scalar():
        raise HTTPException(status_code=400, detail="Email already exists.")
    if await db.execute(select(Employee).filter(Employee.employee_id == employee.employee_id).filter(Employee.id != existing_employee.id)).scalar():
        raise HTTPException(status_code=400, detail="Employee ID already exists.")

    # Update employee details
    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.employee_id = employee.employee_id
    existing_employee.phone = employee.phone
    existing_employee.manager_id = employee.manager_id
    existing_employee.department = employee.department

    await db.commit()
    await db.refresh(existing_employee)
    return existing_employee

# Endpoint to delete an employee
@app.delete("/employees/{employee_id}", response_model=EmployeeInDB)
async def delete_employee(employee_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).filter(Employee.employee_id == employee_id))
    employee = result.scalars().first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
    
    # Ensure the employee being deleted is not a manager or has subordinates
    if employee.manager_id:
        subordinates = await db.execute(select(Employee).filter(Employee.manager_id == employee.id))
        if subordinates.scalars().first():
            raise HTTPException(status_code=400, detail="Manager has subordinates. Reassign before deletion.")

    await db.delete(employee)
    await db.commit()
    return employee

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Management API"}
