import streamlit as st
from logica import calcular_resultado


st.set_page_config(
    page_title="Grupo MOR | VeriLógica",
    page_icon="MOR",
    layout="centered",
)

st.markdown(
    """
    <style>
        /* Fondo general */
        .stApp {
            background-color: #FFF7FB;
        }

        /* Encabezado principal */
        .bloque-principal {
            padding: 1.8rem;
            border-radius: 22px;
            background: linear-gradient(120deg, #F48FB1, #C4B5FD);
            color: #3B1630;
            margin-bottom: 1.5rem;
            text-align: center;
            border: 3px solid #6B2145;
            box-shadow: 0 8px 18px rgba(107, 33, 69, 0.20);
        }

        .bloque-principal h1 {
            margin-bottom: 0.3rem;
            font-size: 3rem;
            color: #3B1630;
        }

        .bloque-principal p {
            margin-bottom: 0;
            font-size: 1.1rem;
            color: #6B2145;
        }

        /* Títulos */
        h2, h3 {
            color: #6B2145;
        }

        /* Tarjetas de métricas */
        div[data-testid="stMetric"] {
            background-color: #FCE4EC;
            border: 2px solid #C4B5FD;
            border-radius: 14px;
            padding: 0.8rem;
            box-shadow: 0 4px 10px rgba(107, 33, 69, 0.08);
        }

        /* Botón principal */
        div.stButton > button {
            width: 100%;
            border-radius: 14px;
            border: 2px solid #6B2145;
            background-color: #F48FB1;
            color: #3B1630;
            font-weight: 700;
            font-size: 1rem;
            padding: 0.6rem;
        }

        div.stButton > button:hover {
            background-color: #C4B5FD;
            color: #3B1630;
            border-color: #6B2145;
        }

        /* Caja del formulario */
        div[data-testid="stForm"] {
            background-color: #FFFFFF;
            border: 2px solid #E9D5FF;
            border-radius: 18px;
            padding: 1.2rem;
            box-shadow: 0 4px 14px rgba(107, 33, 69, 0.08);
        }

        /* Entradas de texto */
        div[data-baseweb="input"] > div {
            border-radius: 12px;
            border-color: #C4B5FD;
            background-color: #FFFFFF;
        }

        div[data-baseweb="textarea"] > div {
            border-radius: 12px;
            border-color: #C4B5FD;
            background-color: #FFFFFF;
        }

        /* Barra lateral */
        section[data-testid="stSidebar"] {
            background-color: #FCE4EC;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #6B2145;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="bloque-principal">
        <h1>Grupo MOR</h1>
        <p>VeriLógica · Evaluador orientativo de confiabilidad para noticias e influencers</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "Esta herramienta no determina una verdad absoluta. "
    "Organiza criterios de evaluación y aplica un modelo lógico-matemático "
    "según las respuestas ingresadas."
)

with st.sidebar:
    st.header("Modelo matemático")

    st.latex(r"P = 3F + 3C + 2A - 3S - 3E - O")

    st.caption(
        "Regla crítica: si no hay fuentes verificables y tampoco "
        "corroboración independiente, se requiere verificación obligatoria."
    )

    st.divider()

    st.subheader("Integrantes")
    st.write(" Oscar Arturo Chavarría Hernández")
    st.write("Mariela Castro Corrales")
    st.write("Rachid Josue Angulo Rodriguez")

    st.caption("Curso: Lógica y Matemática Básica")

st.subheader("Datos de la publicación")

titulo = st.text_input(
    "Título o descripción breve de la publicación",
    placeholder="Ejemplo: Nuevo producto cura una enfermedad en 24 horas",
)

autor = st.text_input(
    "Autor, influencer o medio de publicación (opcional)",
    placeholder="Ejemplo: Nombre de la cuenta o medio",
)

enlace = st.text_input(
    "Enlace de la publicación (opcional)",
    placeholder="https://...",
)

opciones = ["Sí", "No", "No sé"]

preguntas = {
    "fuentes_verificables": "¿La publicación tiene fuentes verificables?",
    "corroboracion_independiente": (
        "¿Otras fuentes independientes confirman la información?"
    ),
    "autor_identificado": (
        "¿Se identifica claramente el autor, medio o responsable?"
    ),
    "titulo_sensacionalista": (
        "¿El título utiliza lenguaje exagerado, alarmista o urgente?"
    ),
    "afirmacion_sin_evidencia": (
        "¿Hay afirmaciones importantes sin evidencia verificable?"
    ),
    "informacion_desactualizada": (
        "¿La publicación utiliza información antigua como si fuera actual?"
    ),
}

st.subheader("Criterios de evaluación")

with st.form("formulario_verilogica"):
    datos = {}

    for variable, pregunta in preguntas.items():
        datos[variable] = st.radio(
            pregunta,
            opciones,
            horizontal=True,
            key=variable,
        )

    notas = st.text_area(
        "Fuentes revisadas u observaciones (opcional)",
        placeholder=(
            "Escriba enlaces, fuentes revisadas, fechas u observaciones "
            "sobre el contenido."
        ),
        height=120,
    )

    evaluar = st.form_submit_button(
        "Evaluar publicación",
        type="primary",
        use_container_width=True,
    )

if evaluar:
    if not titulo.strip():
        st.error("Debe escribir al menos un título o una descripción.")

    else:
        resultado = calcular_resultado(datos)

        st.divider()
        st.subheader("Resultado de la evaluación")

        col1, col2, col3 = st.columns(3)

        col1.metric("Puntaje total", resultado["puntaje"])
        col2.metric("Incertidumbre", f"{resultado['incertidumbre']:.0f}%")
        col3.metric(
            "Criterios sin verificar",
            resultado["sin_verificar"],
        )

        if resultado["clasificacion"] == "CONFIABILIDAD RELATIVAMENTE ALTA":
            st.success(resultado["clasificacion"])

        elif resultado["clasificacion"] == "CONFIABILIDAD MEDIA":
            st.info(resultado["clasificacion"])

        elif "RIESGO ALTO" in resultado["clasificacion"]:
            st.error(resultado["clasificacion"])

        else:
            st.warning(resultado["clasificacion"])

        st.write(resultado["mensaje"])

        if resultado["regla_critica"]:
            st.error(
                "Regla crítica activada: no hay fuentes verificables "
                "ni corroboración independiente."
            )

        izquierda, derecha = st.columns(2)

        with izquierda:
            st.markdown("#### Factores favorables")

            if resultado["positivos"]:
                for factor in resultado["positivos"]:
                    st.write(f"✅ {factor}")
            else:
                st.caption("No se registraron factores favorables.")

        with derecha:
            st.markdown("#### Alertas detectadas")

            if resultado["alertas"]:
                for alerta in resultado["alertas"]:
                    st.write(f"⚠️ {alerta}")
            else:
                st.caption("No se detectaron alertas directas.")

        with st.expander("Ver explicación lógica y matemática"):
            st.latex(r"P = 3F + 3C + 2A - 3S - 3E - O")

            st.latex(
                r"(\neg F \land \neg C) \Rightarrow "
                r"\text{Verificación obligatoria}"
            )

            st.write(
                "El resultado depende de las respuestas ingresadas y de la "
                "calidad de la evidencia revisada. No determina una verdad "
                "absoluta."
            )

        if notas.strip():
            st.caption(
                "Las observaciones fueron registradas temporalmente "
                "durante esta evaluación."
            )