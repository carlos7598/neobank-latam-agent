# =====================================================================
# CHALLENGE ALURA: AGENTE INTELIGENTE FINTECH (BUGFIX DATA PARSING V3.8)
# ARCHITECTURE: TRANSFORMERS + QWEN-0.5B + GRADIO (ZERO-API-KEY)
# AUTHOR: Senior Software Engineer (10 YoE)
# =====================================================================

# 1. INSTALACIÓN DE DEPENDENCIAS COMPATIBLES
print("🛠️ INFRASTRUCTURE: Instalando librerías de IA y componentes web...")
!pip install PyPDF2 transformers torch gradio -q

import os
import PyPDF2
import torch
import gradio as gr
from transformers import pipeline

# 2. CAPA DE EXTRACCIÓN DE DATOS (DATA LAYER)
def extraer_texto_pdf(ruta_pdf: str) -> str:
    if not os.path.exists(ruta_pdf):
        raise FileNotFoundError(f"❌ IO_ERROR: Archivo '{ruta_pdf}' no encontrado. Cárgalo en el panel izquierdo (📁).")
    texto_completo = ""
    with open(ruta_pdf, "rb") as archivo:
        lector_pdf = PyPDF2.PdfReader(archivo)
        for num_pagina in range(len(lector_pdf.pages)):
            pagina = lector_pdf.pages[num_pagina]
            texto_completo += pagina.extract_text() + "\n"
    print("✅ DATA_LAYER: Documento PDF financiero parseado con éxito.")
    return texto_completo

# 3. CARGA DEL MODELO DE INTELIGENCIA ARTIFICIAL LOCAL
print("📥 MODEL_LAYER: Descargando y cargando el modelo de lenguaje en la memoria...")
generator = pipeline(
    "text-generation", 
    model="Qwen/Qwen2.5-0.5B-Instruct", 
    torch_dtype="auto", 
    device_map="auto"
)
print("✅ MODEL_LAYER: Cerebro de IA local inicializado correctamente.")

# Carga global estática del documento
archivo_pdf = "politicas_y_faq_fintech.pdf"
contexto_global = extraer_texto_pdf(archivo_pdf)

# 4. FUNCIÓN CONECTADA A LA INTERFAZ GRÁFICA (BUGFIX APLICADO HERE)
def interfaz_soporte_fintech(pregunta_usuario: str, historial) -> str:
    """Procesa la pregunta del chat y genera la respuesta controlando el formato de salida."""
    messages = [
        {"role": "system", "content": (
            "Eres el Agente Inteligente de Soporte de la Fintech 'NeoBank Latam'. "
            "Responde de forma amable, clara y en español a las dudas de los usuarios. "
            "REGLA OBLIGATORIA: Responde utilizando ÚNICAMENTE la información del 'Contexto del Documento' provisto. "
            "Si la respuesta no se encuentra explícitamente en el texto, di textualmente: "
            "'Lo siento, como asistente de NeoBank Latam no poseo esa información en mis registros de operaciones actuales. Por favor, comunícate con un asesor humano.'"
        )},
        {"role": "user", "content": f"Contexto del Documento:\n{contexto_global}\n\nPregunta del Usuario: {pregunta_usuario}"}
    ]
    try:
        prompt = generator.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        resultado = generator(prompt, max_new_tokens=150, do_sample=False, temperature=0.0)
        
        # SENIOR PARSE BUGFIX: Maneja de forma segura si la respuesta viene en formato lista o diccionario
        if isinstance(resultado, list):
            texto_generado = resultado[0]['generated_text']
        else:
            texto_generado = resultado['generated_text']
            
        respuesta_final = texto_generado.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
        return respuesta_final
    except Exception as e:
        return f"❌ AI_ERROR: Error en el pipeline: {e}"

# =====================================================================
# 5. ORQUESTACIÓN DEL DESPLIEGUE WEB (SHARE DEPLOY)
# =====================================================================
demo = gr.ChatInterface(
    fn=interfaz_soporte_fintech,
    title="🏦 Soporte Inteligente - NeoBank Latam",
    description="Canal de atención automatizado en la nube para consultas operacionales de cuentas de ahorro y crédito.",
    examples=["¿Cuál es el límite estándar para transferencias interbancarias diaria?", "¿Me cobran alguna comisión por tener la cuenta abierta?", "¿Puedo usar el chatbot para comprar criptomonedas o acciones virtuales?"]
)

if __name__ == "__main__":
    print("\n🚀 INFRASTRUCTURE: Inicializando túnel de despliegue público en internet...")
    demo.launch(share=True, debug=True)
