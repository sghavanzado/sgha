import os
import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

# 📌 Configurar el modelo StarCoder
modelo = "bigcode/starcoder"
torch_dtype=torch.float32
tokenizer = AutoTokenizer.from_pretrained(modelo)
modelo = AutoModelForCausalLM.from_pretrained(modelo, torch_dtype=torch.float16, 
device_map="auto")

def analizar_codigo(codigo):
    """Analiza código y sugiere mejoras usando StarCoder."""
    entrada = tokenizer(f"### Analiza este código y sugiere mejoras:\n\n{codigo}", 
return_tensors="pt").to("cpu")
    salida = modelo.generate(**entrada, max_new_tokens=300)
    return tokenizer.decode(salida[0], skip_special_tokens=True)

def obtener_archivos(ruta_proyecto, extensiones=(".py", ".js", ".ts", ".tsx")):
    """Obtiene todos los archivos de código en un proyecto."""
    archivos = []
    for ruta, _, files in os.walk(ruta_proyecto):
        for file in files:
            if file.endswith(extensiones):
                archivos.append(os.path.join(ruta, file))
    return archivos

# 📂 Directorios del proyecto SGHA
backend_dir = "./backend"
frontend_dir = "./frontend"

# 🔍 Obtener archivos del backend y frontend
archivos_backend = obtener_archivos(backend_dir, extensiones=(".py",))
archivos_frontend = obtener_archivos(frontend_dir, extensiones=(".js", ".ts", ".tsx"))

# 📊 Generar reporte de análisis
with open("reporte_SGHA.md", "w", encoding="utf-8") as reporte:
    for archivo in tqdm(archivos_backend + archivos_frontend, desc="📊 Analizando archivos"):
        with open(archivo, "r", encoding="utf-8") as file:
            codigo = file.read()

        print(f"\n📂 Analizando {archivo}...")
        comentarios = analizar_codigo(codigo)

        reporte.write(f"## 📌 Análisis de {archivo}\n\n")
        reporte.write(comentarios + "\n\n")

print("\n✅ Análisis completado. Revisa el archivo reporte_SGHA.md")

