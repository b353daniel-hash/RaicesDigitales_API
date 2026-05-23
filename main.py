from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import hashlib # <-- La herramienta matemática para encriptar
from fastapi import FastAPI
from fastapi.responses import HTMLResponse # <-- Nueva importación para servir tu interfaz
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # El asterisco significa "permitir de cualquier origen"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("raices_digitales.db")
    cursor = conn.cursor()
    # Ahora la tabla tiene un espacio para el sello_digital
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

# --- LA LÓGICA DE RESISTENCIA: EL HASHING ---
def generar_sello(nombre, barrio, tecnica):
    # Unimos toda la información en un solo texto
    datos_unidos = f"{nombre}{barrio}{tecnica}"
    # Pasamos ese texto por la licuadora matemática (SHA-256)
    sello = hashlib.sha256(datos_unidos.encode()).hexdigest()
    return sello

class Huerto(BaseModel):
    nombre: str
    barrio: str
    tecnica_cultivo: str
    historia_oral: str
    contacto_enlace: str
    coordenadas_zona: str
    excedentes_disponibles: list  # Ej. ["Hierbas de olor", "Flores comestibles", "Plántulas"]
    capacidad_comercial: bool     # True si están abiertos a proveer a locales

# --- EL PUENTE WEB: TU DASHBOARD P2P ---
@app.get("/", response_class=HTMLResponse)
async def mostrar_plataforma():
    # El servidor lee tu archivo dashboard.html y lo manda al navegador
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            codigo_html = f.read()
        return HTMLResponse(content=codigo_html, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: No se encontró dashboard.html</h1><p>Asegúrate de que el archivo se llame exactamente así y esté en la misma carpeta que main.py.</p>", 
            status_code=404
        )

# --- RUTAS DE LA API (BACKEND) ---
@app.post("/registrar_huerto/")
def registrar(huerto: Huerto):
    # Generamos la huella dactilar ANTES de guardar
    sello_unico = generar_sello(huerto.nombre, huerto.barrio, huerto.tecnica_cultivo)
    
    conn = sqlite3.connect("raices_digitales.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO huertos (nombre, barrio, tecnica_cultivo, sello_digital) VALUES (?, ?, ?, ?)",
        (huerto.nombre, huerto.barrio, huerto.tecnica_cultivo, sello_unico)
    )
    conn.commit()
    conn.close()
    
    # Devolvemos el "Certificado de Autenticidad"
    return {
        "estatus": "Protegido",
        "mensaje": f"El huerto '{huerto.nombre}' ha sido blindado.",
        "sello_digital": sello_unico
    }

@app.get("/lista_huertos/")
def obtener_huertos():
    conn = sqlite3.connect("raices_digitales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, barrio, tecnica_cultivo, sello_digital FROM huertos")
    datos = cursor.fetchall()
    conn.close()
    
    lista = []
    for d in datos:
        lista.append({"nombre": d[0], "barrio": d[1], "tecnica": d[2], "sello": d[3]})
    return {"huertos_protegidos": lista}

