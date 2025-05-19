import streamlit as st
from openai import OpenAI

# 🔑 Tu clave de API de OpenRouter
api_key = "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"  # ← Reemplaza con tu clave real

# Crear cliente con base_url para OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Configuración de la página
st.set_page_config(page_title="Asistente de Redacción", layout="centered")
st.title("✍️ Asistente de Redacción (OpenRouter)")

# Entrada de texto
user_input = st.text_area("Escribe tu texto aquí:", height=200)

# Botón para mejorar la redacción
if st.button("Mejorar redacción"):
    if user_input.strip() == "":
        st.warning("Por favor, escribe algo.")
    else:
        with st.spinner("Redactando dos versiones..."):
            try:
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct:free",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Eres un experto en redacción de textos. "
                                "Siempre responde en español. "
                                "Dado un texto, devuelve dos versiones distintas del mismo, bien redactadas, "
                                "claramente separadas como 'Opción 1:' y 'Opción 2:'. "
                                "No des ninguna explicación, solo muestra las dos versiones mejoradas."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Mejora este texto en dos versiones: {user_input}"
                        }
                    ],
                    temperature=0.9
                )
                resultado = response.choices[0].message.content
                st.success("Opciones generadas:")
                
                # Dividir en dos opciones (si el modelo usó los separadores correctamente)
                if "Opción 1:" in resultado and "Opción 2:" in resultado:
                    partes = resultado.split("Opción 2:")
                    st.markdown("### ✍️ Opción 1")
                    st.text_area("", value=partes[0].replace("Opción 1:", "").strip(), height=200)

                    st.markdown("### ✍️ Opción 2")
                    st.text_area("", value=partes[1].strip(), height=200)
                else:
                    # Si no se separaron bien, mostrar todo junto
                    st.text_area("Resultado:", value=resultado, height=300)
            except Exception as e:
                st.error(f"Ocurrió un error: {str(e)}")