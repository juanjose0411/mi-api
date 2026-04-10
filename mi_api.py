from fastapi import FastAPI
import google.generativeai as genai
import os

app = FastAPI()

# Configura tu clave
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# ESTO NOS DIRÁ EN EL CMD QUÉ MODELOS TIENES ACTIVOS
print("--- MODELOS DISPONIBLES EN TU CUENTA ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
print("---------------------------------------")

# Intentaremos con el nombre más básico y universal
model = genai.GenerativeModel('gemini-2.5-flash')

@app.get("/preguntar")
def preguntar_a_gemini(mensaje: str):
    try:
        response = model.generate_content(mensaje)
        return {"respuesta": response.text}
    except Exception as e:
        return {"error": str(e)}
