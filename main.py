from simulador.main_engine import ejecutar_simulacion
from simulador.pdf_report import generar_pdf

if __name__ == "__main__":

    parametros_prueba = {
        "demanda_min": 9061,
        "demanda_max": 11915,

        "precio_mu": 26.48,
        "precio_sigma": 0.83,

        "cv_min": 9.01,
        "cv_max": 10.71,

        # Costo fijo discreto
        "cf_valores": [28000, 30000, 32000],
        "cf_probs": [0.30, 0.3667, 0.3333],

        "depreciacion": 50000,
        "tasa_impuesto": 0.30,

        "valor_desecho": 20000,

        "inversion_inicial": -812500,
        "tasa_descuento": 0.20,

        "vida": 10
    }

    # --- Ejecutar simulación ---
    vans, resumen = ejecutar_simulacion(parametros_prueba, iteraciones=100)

    print("\n========== RESULTADOS DE LA SIMULACIÓN ==========\n")
    print("Primeros 10 VANs generados:")
    print(vans[:10])

    print("\nResumen estadístico del VAN:")
    print(resumen)

    # --- Generar PDF ---
    ruta = "reports/pdf_generados/reporte_simulacion.pdf"
    generar_pdf(resumen, ruta)

    print("\nPDF generado correctamente en:", ruta)
