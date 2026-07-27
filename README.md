# 🏦 NeoBank Latam - Agente Inteligente de Soporte Fintech

Este proyecto es un asistente virtual desarrollado para resolver dudas de usuarios sobre políticas, comisiones y límites de un banco digital de forma automatizada.

Para garantizar la disponibilidad del servicio y mitigar errores de cuotas de APIs externas, implementé una arquitectura de Inteligencia Artificial 100% Local.

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.10+
- **Procesamiento de Documentos:** PyPDF2 (Para la extracción de texto del PDF).
- **Core de Inteligencia Artificial:** Hugging Face Transformers.
- **Modelo de IA Local:** Qwen/Qwen2.5-0.5B-Instruct (Ejecutándose en entorno local).

## 🚀 Resultados del Runtime de Pruebas
El agente fue verificado con éxito con la suite de pruebas del Challenge, arrojando las siguientes respuestas:
- **Caso 1 (Límites):** Identificó con precisión el límite estándar de $50,000 MXN diarios.
- **Caso 2 (Comisiones):** Confirmó de forma semántica que no se cobra comisión por apertura ($0 MXN).
- **Caso 3 (Seguridad/Criptomonedas):** Activó el filtro RAG y declinó responder al no estar en las políticas oficiales.
