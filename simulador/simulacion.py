import numpy as np
from .generadores import generar_uniforme, generar_normal, generar_discreta
from .flujo_caja import calcular_flujo_proyecto
from .finanzas import calcular_van


def calcular_tir(flujos):
    try:
        tir = np.irr(flujos)
        return tir if tir is not None else 0
    except:
        return 0


def correr_simulacion(param, iteraciones=1000):

    lista_van = []
    lista_tir = []
    flujos_registrados = []

    for _ in range(iteraciones):

        demanda = generar_uniforme(param["demanda_min"], param["demanda_max"])
        precio = generar_normal(param["precio_mu"], param["precio_sigma"])
        costo_variable = generar_uniforme(param["cv_min"], param["cv_max"])
        costo_fijo = generar_discreta(param["cf_valores"], param["cf_probs"])

        flujo_anual = []
        for anio in range(1, param["vida"] + 1):

            es_ultimo = (anio == param["vida"])

            flujo, _ = calcular_flujo_proyecto({
                "demanda": demanda,
                "precio": precio,
                "costo_variable": costo_variable,
                "costo_fijo": costo_fijo,
                "depreciacion": param["depreciacion"],
                "tasa_impuesto": param["tasa_impuesto"],
                "valor_desecho": param["valor_desecho"],
            }, ultimo_anio=es_ultimo)

            flujo_anual.append(flujo)

        flujos_registrados.append(flujo_anual)

        van = calcular_van(
            inversion_inicial=param["inversion_inicial"],
            tasa_descuento=param["tasa_descuento"],
            flujo=flujo_anual
        )
        lista_van.append(van)

        flujos_completos = [param["inversion_inicial"]] + flujo_anual
        tir = calcular_tir(flujos_completos)
        lista_tir.append(tir)

    # REEMPLAZADO: claves correctas para app.py
    resumen = {
        "media": float(np.mean(lista_van)),
        "mediana": float(np.median(lista_van)),
        "desviacion": float(np.std(lista_van)),
        "minimo": float(np.min(lista_van)),
        "maximo": float(np.max(lista_van)),

        "media_tir": float(np.mean(lista_tir)),
        "minimo_tir": float(np.min(lista_tir)),
        "maximo_tir": float(np.max(lista_tir)),
    }

    return lista_van, lista_tir, flujos_registrados, resumen
