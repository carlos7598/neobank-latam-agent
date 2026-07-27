# =====================================================================
# CHALLENGE ALURA: AGENTE INTELIGENTE FINTECH (NATIVE TEXT-GEN INFERENCE)
# ARCHITECTURE: TRANSFORMERS + QWEN-0.5B (ZERO-API-KEY / IMMUNE TO 429)
# AUTHOR: Senior Software Engineer (10 YoE)
# =====================================================================

# 1. INSTALACIÓN DE DEPENDENCIAS COMPATIBLES
print("🛠️ INFRASTRUCTURE: Instalando librerías de IA nativas de Python...")
!pip install PyPDF2 transformers torch -q

import os
import PyPDF2
import torch
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

# 3. CARGA DEL PIPELINE DE TEXT-GENERATION VIGENTE
print("📥 MODEL_LAYER: Descargando y cargando el modelo de lenguaje en la memoria...")
# Usamos Qwen2.5-0.5B-Instruct, un modelo ultra rápido, moderno y compatible con la tarea 'text-generation'
generator = pipeline(
    "text-generation", 
    model="Qwen/Qwen2.5-0.5B-Instruct", 
    torch_dtype="auto", 
    device_map="auto"
)
print("✅ MODEL_LAYER: Cerebro de IA local inicializado correctamente.")

# 4. PIPELINE RAG LOCAL INTELIGENTE
def consultar_agente_inteligente(pregunta_usuario: str, contexto_pdf: str) -> str:
    """Procesa la pregunta combinando inteligencia semántica real sin servidores externos."""
    
    # Construcción de la estructura de Chat compatible con los modelos Instruct modernos
    messages = [
        {"role": "system", "content": (
            "Eres el Agente Inteligente de Soporte de la Fintech 'NeoBank Latam'. "
            "Responde de forma amable, clara y en español a las dudas de los usuarios. "
            "REGLA OBLIGATORIA: Responde utilizando ÚNICAMENTE la información del 'Contexto del Documento' provisto. "
            "Si la respuesta no se encuentra explícitamente en el texto, di textualmente: "
            "'Lo siento, como asistente de NeoBank Latam no poseo esa información en mis registros de operaciones actuales. Por favor, comunícate con un asesor humano.'"
        )},
        {"role": "user", "content": f"Contexto del Documento:\n{contexto_pdf}\n\nPregunta del Usuario: {pregunta_usuario}"}
    ]
    
    try:
        # Generación de la respuesta aplicando el template del modelo
        prompt = generator.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        resultado = generator(prompt, max_new_tokens=150, do_sample=False, temperature=0.0)
        
        # Extracción y limpieza del texto generado
        texto_generado = resultado[0]['generated_text']
        respuesta_final = texto_generado.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
        
        return respuesta_final
        
    except Exception as e:
        return f"❌ AI_ERROR: Error en el pipeline de inferencia local: {e}"

# =====================================================================
# 5. ORQUESTACIÓN PRINCIPAL Y SUITE DE PRUEBAS
# =====================================================================
archivo_pdf = "politicas_y_faq_fintech.pdf"

if __name__ == "__main__":
    try:
        # Carga del contexto financiero estático
        contexto = extraer_texto_pdf(archivo_pdf)
        
        # Suite de pruebas requeridas por la rúbrica del Challenge de Alura
        preguntas_de_prueba = [
            "¿Cuál es el límite estándar para transferencias interbancarias diaria?",
            "¿Me cobran alguna comisión por tener la cuenta abierta o por apertura?",
            "¿Puedo usar el chatbot para comprar criptomonedas o acciones virtuales?"  # Caso fuera de contexto
        ]
        
        print("\n--- INICIANDO RUNTIME DE PRUEBAS DEL AGENTE FINTECH LOCAL ---")
        for i, pregunta in enumerate(preguntas_de_prueba, 1):
            print(f"\n🔹 [Caso {i}] Test-Input: '{pregunta}'")
            respuesta_ia = consultar_agente_inteligente(pregunta, contexto)
            print(f"🤖 Agente NeoBank Local:\n{respuesta_ia}")
            
        print("\n🎉 ARCHITECTURE_SUCCESS: El sistema local respondió con éxito y sin dependencias externas.")
        
    except Exception as runtime_err:
        print(f"💥 RUNTIME_CRASH: Error fatal en la orquestación: {runtime_err}")
