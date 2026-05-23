from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import hashlib
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de Base de Datos
def init_db():
    conn = sqlite3.connect("raices_digitales.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS huertos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            barrio TEXT,
            tecnica_cultivo TEXT,
            sello_digital TEXT 
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Modelo de datos
class Huerto(BaseModel):
    nombre: str
    barrio: str
    tecnica_cultivo: str
    historia_oral: str
    contacto_enlace: str
    coordenadas_zona: str
    excedentes_disponibles: list
    capacidad_comercial: bool

# Función de Hashing
def generar_sello(nombre, barrio, tecnica):
    datos_unidos = f"{nombre}{barrio}{tecnica}"
    return hashlib.sha256(datos_unidos.encode()).hexdigest()

# --- RUTA RAÍZ (Dashboard) ---
@app.get("/", response_class=HTMLResponse)
async def mostrar_plataforma():
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            codigo_html = f.read()
        return HTMLResponse(content=codigo_html, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: dashboard.html no encontrado</h1>", status_code=404)

# --- RUTAS DE API ---
@app.post("/registrar_huerto/")
def registrar(huerto: Huerto):
    sello_unico = generar_sello(huerto.nombre, huerto.barrio, huerto.tecnica_cultivo)
    conn = sqlite3.connect("raices_digitales.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO huertos (nombre, barrio, tecnica_cultivo, sello_digital) VALUES (?, ?, ?, ?)",
        (huerto.nombre, huerto.barrio, huerto.tecnica_cultivo, sello_unico)
    )
    conn.commit()
    conn.close()
    return {"estatus": "Protegido", "sello_digital": sello_unico}

@app.get("/lista_huertos/")
def obtener_huertos():
    conn = sqlite3.connect("raices_digitales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, barrio, tecnica_cultivo, sello_digital FROM huertos")
    datos = cursor.fetchall()
    conn.close()
    return {"huertos_protegidos": [{"nombre": d[0], "barrio": d[1], "tecnica": d[2], "sello": d[3]} for d in datos]}
