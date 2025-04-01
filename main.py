from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.provincia_routes import router as provincia_router
from routes.delito_routes import router as delito_router
from routes.estadistica_routes import router as estadistica_router
from routes.estadistica_calculada_routes import router as estadistica_calculada_router

app = FastAPI(title="Crime Statistics API", description="API for managing crime statistics in Argentina")

#app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Incluir routers: se especifica un prefijo y etiquetas para cada uno
app.include_router(provincia_router)
app.include_router(delito_router)
app.include_router(estadistica_router)
app.include_router(estadistica_calculada_router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
