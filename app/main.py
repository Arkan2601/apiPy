# main.py
from fastapi import FastAPI
from productos import router as productos_router
import uvicorn
import threading
import webbrowser
import time

app = FastAPI()

# Incluir las rutas del archivo productos.py
app.include_router(productos_router)

def open_docs():
    time.sleep(3)
    webbrowser.open("http://192.168.0.100:8000/docs")

if __name__ == "__main__":
    threading.Thread(target=open_docs).start()  
    uvicorn.run(app, host="192.168.0.100", port=8000)
