from fastapi import FastAPI, UploadFile, File, Form
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura tu clave
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# ESTO NOS DIRÁ EN EL CMD QUÉ MODELOS TIENES ACTIVOS
print("--- MODELOS DISPONIBLES EN TU CUENTA ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
print("---------------------------------------")

# Intentaremos con el nombre más básico y universal
model = genai.GenerativeModel('gemini-2.0-flash')

@app.post("/preguntar")
async def preguntar_a_gemini(mensaje: str = Form(...), file: UploadFile = File(None)):
    try:
        content = [mensaje]
        
        # Si el usuario subió una foto, la procesamos
        if file:
            image_data = await file.read()
            content.append({"mime_type": file.content_type, "data": image_data})
        
        response = model.generate_content(content)
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": str(e)}
