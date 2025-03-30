from fastapi import FastAPI
from routes.provincia_routes import router as provincia_router
from routes.delito_routes import router as delito_router
from routes.estadistica_routes import router as estadistica_router

app = FastAPI(title="Crime Statistics API", description="API for managing crime statistics in Argentina")

# Include routers
app.include_router(provincia_router)
app.include_router(delito_router)
app.include_router(estadistica_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crime Statistics API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)