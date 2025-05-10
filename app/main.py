
from fastapi import FastAPI
import uvicorn
import threading
import webbrowser
import time
from config import API_HOSTING,API_PORT
""" modulos """
from productos import router as productos_router
from roles import router as roles_router
from login import router as login_router
from detalleRoles import router as detalleRoles_router



app = FastAPI()

app.include_router(productos_router)
app.include_router(login_router)
app.include_router(detalleRoles_router)
app.include_router(roles_router)

def open_docs():
    time.sleep(3)
    webbrowser.open(f"http://{API_HOSTING}:{API_PORT}/docs")

if __name__ == "__main__":
    threading.Thread(target=open_docs).start()  
uvicorn.run(app, host=f"{API_HOSTING}", port=int(API_PORT))

