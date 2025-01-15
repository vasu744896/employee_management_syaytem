from fastapi import FastAPI
from routes import employee  # Ensure this import is correct

app = FastAPI()

# Include the employee routes
app.include_router(employee.router)
