PESOS = {
    "fuentes_verificables": 3,
    "corroboracion_independiente": 3,
    "autor_identificado": 2,
    "titulo_sensacionalista": -3,
    "afirmacion_sin_evidencia": -3,
    "informacion_desactualizada": -1,
}


NOMBRES_CRITERIOS = {
    "fuentes_verificables": "Fuentes verificables",
    "corroboracion_independiente": "Corroboración independiente",
    "autor_identificado": "Autor o medio identificado",
    "titulo_sensacionalista": "Título sensacionalista",
    "afirmacion_sin_evidencia": "Afirmación sin evidencia",
    "informacion_desactualizada": "Información desactualizada",
}


def calcular_resultado(datos):
    puntaje = 0
    positivos = []
    alertas = []
    sin_verificar = 0

    for variable, peso in PESOS.items():
        respuesta = datos[variable]
        nombre = NOMBRES_CRITERIOS[variable]

        if respuesta == "No sé":
            sin_verificar += 1
            continue

        if respuesta == "Sí":
            puntaje += peso

            if peso > 0:
                positivos.append(f"{nombre} ({peso:+d} puntos)")
            else:
                alertas.append(f"{nombre} ({peso:+d} puntos)")

    incertidumbre = (sin_verificar / len(PESOS)) * 100

    sin_fuentes = datos["fuentes_verificables"] == "No"
    sin_corroboracion = datos["corroboracion_independiente"] == "No"

    regla_critica = sin_fuentes and sin_corroboracion

    if incertidumbre >= 50:
        clasificacion = "INFORMACIÓN INSUFICIENTE"
        mensaje = (
            "Hay demasiados criterios sin verificar. "
            "No es responsable generar una conclusión definitiva."
        )

    elif regla_critica:
        clasificacion = "REQUIERE VERIFICACIÓN OBLIGATORIA"
        mensaje = (
            "No se identificaron fuentes verificables ni corroboración "
            "independiente. El contenido no puede clasificarse como confiable."
        )

    elif puntaje >= 6:
        clasificacion = "CONFIABILIDAD RELATIVAMENTE ALTA"
        mensaje = (
            "El contenido presenta varias señales favorables. "
            "Esto no demuestra una verdad absoluta."
        )

    elif puntaje >= 2:
        clasificacion = "CONFIABILIDAD MEDIA"
        mensaje = (
            "Existen elementos favorables, pero todavía conviene revisar "
            "las fuentes y el contexto."
        )

    elif puntaje >= -2:
        clasificacion = "REQUIERE VERIFICACIÓN"
        mensaje = (
            "La evidencia disponible es limitada, contradictoria "
            "o requiere revisión adicional."
        )

    else:
        clasificacion = "RIESGO ALTO DE DESINFORMACIÓN"
        mensaje = (
            "Se identificaron varias señales de riesgo. "
            "No comparta el contenido antes de verificarlo."
        )

    return {
        "puntaje": puntaje,
        "incertidumbre": incertidumbre,
        "clasificacion": clasificacion,
        "mensaje": mensaje,
        "positivos": positivos,
        "alertas": alertas,
        "sin_verificar": sin_verificar,
        "regla_critica": regla_critica,
    }