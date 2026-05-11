import sqlite3
import hashlib # <-- La herramienta matemática para encriptar
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

@app.get("/")
def leer_raiz():
    return {"mensaje": "API de Raíces Digitales: Memoria y Seguridad Activas"}

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
