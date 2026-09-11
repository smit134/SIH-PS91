from fastapi import FastAPI
from app.routers import finance, schemes

app = FastAPI(
    title="ThinkForge Financial Engine API",
    description="Financial Structuring and Scheme Routing Engine",
    version="1.0.0"
)

app.include_router(finance.router)
app.include_router(schemes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ThinkForge Financial Engine API"}
