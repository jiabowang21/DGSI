import os
import openai
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from utils import procesar_datos
# Cargar la clave API desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Configurar templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

    
# Ruta para servir la página del chatbot
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para manejar los mensajes del chatbot
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    chunks = procesar_datos()
    prompt = f"""Eres un asistente experto en responder preguntas basándote en información fragmentada en múltiples chunks almacenados en ChromaDB. A continuación, te proporcionaré un fragmento de información que necesitas aprender para usar en el futuro para responder preguntas relacionadas. El fragmento de información es el siguiente:
{chunks}

Por favor, recuerda este fragmento de información y utilízalo cuando te realicen preguntas sobre este contenido.

Para cada pregunta, sigue estos pasos:

Recuperación: Busca en ChromaDB los chunks más relevantes relacionados con la consulta.
Síntesis: Analiza la información recuperada y combínala en una respuesta coherente y clara.
Ampliación del Contexto: Además de la información encontrada en los chunks, integra otros datos o detalles relacionados con el concepto de la pregunta. Por ejemplo, si la pregunta es sobre "DGSI", no limites la respuesta a definir la asignatura y sus nombres completos; incluye además información complementaria, como que es una asignatura obligatoria del máster en Ingeniería Informática de la Facultad de Informática de Barcelona, y otros detalles relevantes o contextuales.
Explicación: Si la información provista es incompleta o ambigua, indícalo y sugiere posibles interpretaciones o fuentes adicionales.
Formato: Responde en un estilo natural y conciso, asegurando que la información fluya de manera lógica.
Ejemplo de respuesta:

Pregunta: "¿Cuál es la capital de Francia?"
Chunks recuperados: ["París es la ciudad más poblada de Francia y su centro político.", "Francia tiene su capital en París desde hace siglos."]
Respuesta generada: "La capital de Francia es París, que también es su ciudad más poblada y centro político."
Si no encuentras información relevante en los chunks almacenados, responde con: "No encontré información suficiente en la base de datos para responder con certeza. ¿Quieres que intente reformular la búsqueda o consulte otra fuente?"

Mi pregunta es: {user_message}"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # O el modelo que prefieras
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return JSONResponse(content={"reply": bot_reply})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

