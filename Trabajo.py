import streamlit as st
from openai import OpenAI
import re

# Clave de API
api_key = "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"
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# Configuración de página
st.set_page_config(page_title="Reescribir texto", layout="centered")
st.markdown("## 📝 Reescribe el siguiente texto...")

# Entrada de texto
user_input = st.text_area("Texto:", height=150, max_chars=2048)
st.caption(f"{len(user_input)} / 2048 caracteres")

# Controles: Tono, Variantes, Estructura
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    tono_opciones = {
        "🧑‍💼 Profesional": "profesional",
        "🏛️ Formal": "formal",
        "😊 Amistoso": "amistoso",
        "😎 Informal": "informal",
        "🤝 Diplomático": "diplomático"
    }
    tono_seleccionado = st.selectbox("Tono", list(tono_opciones.keys()), index=0)

with col2:
    cantidad = st.selectbox("Generar", ["1 variante", "2 variantes"])

with col3:
    editar_estructura = st.toggle("Editar estructura", value=False)

# Estilo del botón
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ff7900;
    color: white;
    font-weight: bold;
    border-radius: 5px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# Botón de acción
if st.button("✨ Reescribir párrafo"):
    if not user_input.strip():
        st.warning("Por favor, escribe algo.")
    else:
        with st.spinner("Reescribiendo..."):
            try:
                n_variantes = 2 if "2" in cantidad else 1
                estructura_msg = "Modifica también la estructura del texto." if editar_estructura else "Conserva la estructura del texto."

                if n_variantes == 2:
                    prompt = (
                        f"Reescribe el siguiente texto en español con un tono {tono_opciones[tono_seleccionado]}. "
                        f"{estructura_msg} Devuelve exactamente dos versiones claramente separadas como 'Opción 1:' y 'Opción 2:'. "
                        "No des ninguna explicación adicional."
                    )
                else:
                    prompt = (
                        f"Reescribe el siguiente texto en español con un tono {tono_opciones[tono_seleccionado]}. "
                        f"{estructura_msg} Devuelve solo una versión, sin usar etiquetas como 'Opción 1:' ni 'Opción 2:'. "
                        "No des ninguna explicación adicional."
                    )

                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct:free",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7
                )

                resultado = response.choices[0].message.content.strip()

                if "Opción 1:" in resultado and "Opción 2:" in resultado and n_variantes == 2:
                    match = re.search(r"Opción 1:(.*?)Opción 2:(.*)", resultado, re.DOTALL)
                    if match:
                        opcion_1 = match.group(1).strip()
                        opcion_2 = match.group(2).strip()
                        st.markdown("### 📝 Opción 1")
                        st.success(opcion_1)
                        st.markdown("### 📝 Opción 2")
                        st.success(opcion_2)
                    else:
                        st.markdown("### 📝 Resultado")
                        st.success(resultado)
                else:
                    st.markdown("### 📝 Versión mejorada")
                    st.success(resultado)

            except Exception as e:
                st.error(f"Error: {str(e)}")