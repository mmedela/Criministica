from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.provincia_routes import router as provincia_router
from routes.delito_routes import router as delito_router
from routes.estadistica_routes import router as estadistica_router
from routes.estadistica_calculada_routes import router as estadistica_calculada_router

app = FastAPI(title="Crime Statistics API", description="API for managing crime statistics in Argentina", version="0.1.3")

#app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "about:blank", 
            "title": "Error" if not isinstance(exc.detail, str) else exc.detail,
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "type": "about:blank",
            "title": "Internal Server Error",
            "status": 500,
            "detail": str(exc),
            "instance": str(request.url)
        }
    )

app.include_router(provincia_router)
app.include_router(delito_router)
app.include_router(estadistica_router)
app.include_router(estadistica_calculada_router)



@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/poblaciones-provincias", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("poblaciones_provincias.html", {"request": request})

@app.get("/estadisticas-generales", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("estadisticas_generales.html", {"request": request})

@app.get("/version")
def get_version():
    return {"version": app.version}

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "Running"}

@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("provincias_upload.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
