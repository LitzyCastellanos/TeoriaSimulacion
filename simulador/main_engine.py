# simulador/main_engine.py

from simulador.simulacion import correr_simulacion
from simulador.validacion import validar_aleatorios
from simulador.pdf_report import generar_reporte_pdf

def ejecutar_simulacion(parametros, iteraciones=1000):
    """
    Correr la simulación COMPLETA y devolver:
    - vans: lista de VAN por iteración
    - tirs: lista de TIR por iteración
    - flujos: flujos de caja año por año
    - resumen: estadísticas del VAN y TIR
    """
    vans, tirs, flujos, resumen = correr_simulacion(parametros, iteraciones)
    return vans, tirs, flujos, resumen


def generar_reporte(parametros, iteraciones=1000):
    """
    Generar el PDF completo usando:
    - simulación del VAN
    - validación estadística
    - gráfica del VAN
    """
    vans, tirs, flujos, resumen = ejecutar_simulacion(parametros, iteraciones)

    resultados_pruebas = validar_aleatorios(parametros)

    ruta_pdf = generar_reporte_pdf(
        resumen=resumen,
        resultados_pruebas=resultados_pruebas,
        ruta_grafica="grafica_van.png"
    )
    
    return ruta_pdf
