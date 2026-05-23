"""
Raíces Digitales — Backend honesto
Qué hace este archivo y por qué cada decisión es así.
"""

import sqlite3
import uuid
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Raíces Digitales API")

# ── CORS ────────────────────────────────────────────────────────────────────
# allow_origins=["*"] está bien para un MVP de hackathon.
# En producción pondrías el dominio exacto de tu frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── BASE DE DATOS ────────────────────────────────────────────────────────────
# SQLite funciona para un MVP local. En producción usarías PostgreSQL.
# ADVERTENCIA: Render en plan gratuito tiene filesystem efímero —
# los datos se pierden en cada redeploy. Para demo está bien; para
# producción real necesitas una BD externa (Render ofrece PostgreSQL gratis).

DB_PATH = "raices.db"

@contextmanager
def get_db():
    """Abre y cierra la conexión correctamente aunque haya errores."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # permite acceder columnas por nombre
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS huertos (
                id          TEXT PRIMARY KEY,
                nombre      TEXT NOT NULL,
                barrio      TEXT NOT NULL,
                tecnica     TEXT NOT NULL,
                descripcion TEXT,
                contacto    TEXT,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

init_db()

# ── MODELOS ──────────────────────────────────────────────────────────────────

class HuertoIn(BaseModel):
    nombre:      str = Field(..., min_length=2, max_length=100)
    barrio:      str = Field(..., min_length=2, max_length=100)
    tecnica:     str = Field(..., min_length=2, max_length=200)
    descripcion: str | None = Field(None, max_length=1000)
    contacto:    str | None = Field(None, max_length=200)

class HuertoOut(BaseModel):
    id:          str   # UUID — identificador único, sin pretensiones de "sello criptográfico"
    nombre:      str
    barrio:      str
    tecnica:     str
    descripcion: str | None
    contacto:    str | None
    created_at:  str

# ── RUTAS ────────────────────────────────────────────────────────────────────

@app.get("/")
def raiz():
    return {"proyecto": "Raíces Digitales", "status": "activo"}


@app.post("/huertos/", response_model=HuertoOut, status_code=201)
def registrar_huerto(datos: HuertoIn):
    """
    Registra un huerto y le asigna un UUID como identificador único.

    ¿Por qué UUID y no SHA-256?
    SHA-256 de nombre+barrio+técnica no oculta nada — quien conozca
    los datos puede regenerar el mismo hash. Un UUID es honesto:
    es un ID único, nada más, nada menos.
    """
    nuevo_id = str(uuid.uuid4())

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO huertos (id, nombre, barrio, tecnica, descripcion, contacto)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nuevo_id, datos.nombre, datos.barrio, datos.tecnica,
             datos.descripcion, datos.contacto),
        )

    return _get_huerto_o_404(nuevo_id)


@app.get("/huertos/", response_model=list[HuertoOut])
def listar_huertos(barrio: str | None = None):
    """Lista todos los huertos. Acepta ?barrio=Coecillo para filtrar."""
    with get_db() as conn:
        if barrio:
            rows = conn.execute(
                "SELECT * FROM huertos WHERE barrio LIKE ? ORDER BY created_at DESC",
                (f"%{barrio}%",),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM huertos ORDER BY created_at DESC"
            ).fetchall()

    return [dict(r) for r in rows]


@app.get("/huertos/{huerto_id}", response_model=HuertoOut)
def obtener_huerto(huerto_id: str):
    return _get_huerto_o_404(huerto_id)


@app.delete("/huertos/{huerto_id}", status_code=204)
def eliminar_huerto(huerto_id: str):
    _get_huerto_o_404(huerto_id)   # lanza 404 si no existe
    with get_db() as conn:
        conn.execute("DELETE FROM huertos WHERE id = ?", (huerto_id,))


# ── HELPERS ──────────────────────────────────────────────────────────────────

def _get_huerto_o_404(huerto_id: str) -> dict:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM huertos WHERE id = ?", (huerto_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Huerto no encontrado")
    return dict(row)
