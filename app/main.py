# main.py
from fastapi import FastAPI
from productos import router as productos_router
from roles import router as roles_router
import uvicorn
import threading
import webbrowser
import time
from config import API_HOSTING,API_PORT

app = FastAPI()

# Incluir las rutas del archivo productos.py
app.include_router(productos_router)
app.include_router(roles_router)

def open_docs():
    time.sleep(3)
    webbrowser.open(f"http://{API_HOSTING}:{API_PORT}/docs")

if __name__ == "__main__":
    threading.Thread(target=open_docs).start()  
    uvicorn.run(app, host=f"{API_HOSTING}", port=f'{API_PORT}')
