import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Tu API Key (Recuerda poner la tuya)
os.environ["GOOGLE_API_KEY"] = "AIzaSyAH7d8JvoEbfqmuj98t52Jfy0K-D_kU9tk"

# 2. Inicializar el Cerebro
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# 3. Rol
instrucciones = SystemMessage(content="""
Eres el Agente UX/UI de Raíces Digitales. 
Entrega únicamente el código HTML/CSS solicitado, sin texto extra ni comillas invertidas.
Mantén la estética: fondo oscuro (#1a1d1a), tipografía Courier New, acentos verde neón (#00ff00).
""")

# 4. La Orden B2B P2P
orden = HumanMessage(content="""
Genera el código HTML y CSS en un solo archivo para el 'Dashboard B2B' principal de Raíces Digitales. 
Estructura: 
- Una barra lateral izquierda (Sidebar) oscura con un logo en texto verde y enlaces de menú ('Mercado', 'Mis Contratos', 'Auditoría Criptográfica').
- Un área principal (Main Content) a la derecha.
En el área principal:
- Un título grande: 'Terminal de Operaciones P2P'.
- Una cuadrícula (CSS Grid) con 3 tarjetas de huertos diferentes. 
- Cada tarjeta debe tener: Nombre del huerto, un hash SHA-256 falso simulando una terminal negra, kilos disponibles, y un botón verde que diga EXACTAMENTE 'Conectar y Acordar Entrega'. 
IMPORTANTE: No menciones ninguna app de reparto externa.
""")

# 5. Ejecutar
print("Pensando y escribiendo código...\n")
respuesta = llm.invoke([instrucciones, orden])
print(respuesta.content)