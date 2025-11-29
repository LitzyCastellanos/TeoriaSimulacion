import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)


# TABLA DE FLUJO DE CAJA

def tabla_flujo_caja_completa(parametros=None):

    ingresos = [0, 250000, 300000, 429000, 485000, 429000, 445000,
                429000, 485000, 429000, 429000]

    costos_var = [0, -100000, -120000, -157200, -157200, -157200,
                  -120000, -157200, -157200, -157200, -157200]

    costos_fijos = [0, -30000, -33000, -33000, -33000, -33000,
                    -33000, -33000, -33000, -33000, -33000]

    dep_const = [0] + [-10000]*10
    dep_A = [0] + [-14000]*9 + [0]
    dep_B = [0, -32000, -32000, -32000, -32000, -32000, 0, -32000, -32000, -32000, 0]

    utilidad = [0, 95800, 111750, 183960, 183960, 183960,
                230800, 183960, 183960, 183960, 183960]

    impuesto = [0, -19120, -22350, -36792, -36792, -36792,
                -46160, -36792, -36792, -36792, -36792]

    utilidad_neta = [0, 76680, 89400, 147168, 147168, 147168,
                     184640, 147168, 147168, 147168, 147168]

    cap_trabajo = [-32500, -5000, -10050] + [0]*8
    desecho = [0]*10 + [524000]

    flujo = [-812500, 95800, 111750, 183960, 183960, 183960,
             183960, 183960, 183960, 183960, 755510]

    encabezados = ["Concepto"] + [f"Año {i}" for i in range(11)]

    filas = [
        ["Ingresos"] + ingresos,
        ["Costo Variable"] + costos_var,
        ["Costo Fijo"] + costos_fijos,
        ["Depreciación Construcción"] + dep_const,
        ["Depreciación Máquina A"] + dep_A,
        ["Depreciación Máquina B"] + dep_B,
        ["Utilidad"] + utilidad,
        ["Impuesto"] + impuesto,
        ["Utilidad Neta"] + utilidad_neta,
        ["Capital de Trabajo"] + cap_trabajo,
        ["Valor de Desecho"] + desecho,
        ["FLUJO NETO"] + flujo,
    ]

    return [encabezados] + filas



# GENERAR REPORTE PDF

def generar_reporte_pdf(resumen_van, resultados_pruebas=None, ruta_grafica="grafica_van.png"):

    ruta = "reports/pdf_generados/reporte_simulacion.pdf"
    os.makedirs("reports/pdf_generados", exist_ok=True)

    doc = SimpleDocTemplate(
        ruta,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=40,
    )
    

    elementos = []
    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloUNAH", fontSize=16, alignment=1,
        textColor=colors.white, leading=20
    )

    estilo_sub = ParagraphStyle(
        "SubUNAH", fontSize=10, alignment=1,
        textColor=colors.white, leading=14
    )

    estilo_seccion = ParagraphStyle(
        "Seccion", fontSize=13, leading=16,
        textColor=colors.HexColor("#002B5B"), spaceAfter=8
    )

   
    # ENCABEZADO CON LOGO
   
    ruta_logo = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "assets", "logo_unah.png"
    )
    ruta_logo = os.path.normpath(ruta_logo)

    try:
        logo = Image(ruta_logo, width=70, height=70)
    except:
        logo = Paragraph("<b>LOGO NO ENCONTRADO</b>", estilo_sub)

    encabezado = [[logo, Paragraph(
        "<b>UNIVERSIDAD NACIONAL AUTÓNOMA DE HONDURAS</b>",
        estilo_titulo
    ), ""]]

    tabla_encabezado = Table(encabezado, colWidths=[80, 350, 10])
    tabla_encabezado.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#002B5B")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TEXTCOLOR", (1,0), (1,0), colors.white),
    ]))

    elementos.append(tabla_encabezado)
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph(
        "<b>Reporte de Simulación – Devimulator</b><br/>Evaluación financiera bajo riesgo",
        estilo_sub
    ))
    elementos.append(Spacer(1, 20))

   
    # 1. RESUMEN ESTADÍSTICO DEL VAN
   
    elementos.append(Paragraph("1. Resumen estadístico del VAN", estilo_seccion))

    data_van = [
        ["Indicador", "Valor (Lempiras)"],
        ["Media", f"L {resumen_van['media']:,.2f}"],
        ["Mediana", f"L {resumen_van['mediana']:,.2f}"],
        ["Desviación estándar", f"L {resumen_van['desviacion']:,.2f}"],
        ["Percentil 5%", f"L {resumen_van['percentil_5']:,.2f}"],
        ["Percentil 25%", f"L {resumen_van['percentil_25']:,.2f}"],
        ["Percentil 75%", f"L {resumen_van['percentil_75']:,.2f}"],
        ["Percentil 95%", f"L {resumen_van['percentil_95']:,.2f}"],
        ["Mínimo", f"L {resumen_van['minimo']:,.2f}"],
        ["Máximo", f"L {resumen_van['maximo']:,.2f}"],
    ]

    tabla_van = Table(data_van, colWidths=[230, 220])
    tabla_van.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#002B5B")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ]))

    elementos.append(tabla_van)
    elementos.append(Spacer(1, 20))

   
    # 2. VALIDACIÓN ESTADÍSTICA
   
    if resultados_pruebas:
        elementos.append(Paragraph("2. Validación estadística", estilo_seccion))

        data_pr = [["Variable", "Prueba", "Estadístico", "Valor crítico", "¿Acepta H₀?"]]

        for var, res in resultados_pruebas.items():
            data_pr.append([
                var,
                res["prueba"],
                f"{res['estadistico']:.4f}",
                f"{res['valor_critico']:.4f}",
                "Sí" if res["acepta"] else "No",
            ])

        tabla_est = Table(data_pr, colWidths=[120,130,80,90,80])
        tabla_est.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#002B5B")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ]))

        elementos.append(tabla_est)
        elementos.append(Spacer(1, 20))

        
        # 2.1 Parámetros teóricos de las variables
        
        elementos.append(Paragraph("2.1 Parámetros teóricos de las variables de entrada", estilo_seccion))
        data_param = [
            ["Variable", "Media (μ)", "Varianza (σ²)", "Observaciones"],
            ["Demanda", "≈ 10,500", "Alta (rango 9,061 – 11,915)", "Distribución uniforme"],
            ["Precio de venta", "26.48", "≈ 0.69", "Distribución normal"],
            ["Costos variables", "≈ 9.86", "≈ 0.30", "Distribución uniforme"],
            ["Costos fijos", "28,000; 30,000; 32,000", "Varianza moderada", "Distribución discreta"],
        ]
        tabla_param = Table(data_param, colWidths=[110, 90, 110, 150])
        tabla_param.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#002B5B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
        ]))
        elementos.append(tabla_param)
        elementos.append(Spacer(1, 16))

        
        # 2.2 Resumen del ajuste de distribuciones
        
        elementos.append(Paragraph("2.2 Resumen del ajuste de distribuciones", estilo_seccion))
        data_ajuste = [
            ["Variable", "Distribución probada", "Prueba aplicada", "Resultado"],
            ["Demanda", "Uniforme (9,061 – 11,915)", "Kolmogorov–Smirnov", "Se ajusta"],
            ["Precio de venta", "Normal (μ=26.48, σ=0.83)", "Chi-cuadrado", "Se ajusta"],
            ["Costos variables", "Uniforme (9.01 – 10.71)", "Kolmogorov–Smirnov", "Se ajusta"],
            ["Costos fijos", "Discreta (28k, 30k, 32k)", "Chi-cuadrado", "Se ajusta"],
        ]
        tabla_ajuste = Table(data_ajuste, colWidths=[90, 160, 110, 80])
        tabla_ajuste.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#002B5B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
        ]))
        elementos.append(tabla_ajuste)
        elementos.append(Spacer(1, 20))

   
    # 3. TABLA DE FLUJO DE CAJA COMPLETO
   
    elementos.append(Paragraph("3. Flujo de caja del proyecto (Escenario Base)", estilo_seccion))

    tabla_fc = tabla_flujo_caja_completa()
    tabla_fc_pdf = Table(tabla_fc, repeatRows=1)

    tabla_fc_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#002B5B")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTSIZE", (0,0), (-1,-1), 7),
    ]))

    elementos.append(tabla_fc_pdf)
    elementos.append(Spacer(1, 20))

   
    # 4. GRÁFICA DEL VAN
   
    elementos.append(Paragraph("4. Distribución del VAN", estilo_seccion))

    if os.path.exists(ruta_grafica):
        try:
            grafica = Image(ruta_grafica, width=450, height=250)
            elementos.append(grafica)
        except:
            elementos.append(Paragraph("Error al cargar la gráfica.", estilos["BodyText"]))
    else:
        elementos.append(Paragraph("No se encontró la gráfica generada.", estilos["BodyText"]))

    elementos.append(Spacer(1, 20))

   
    # 5. PROYECCIÓN FINANCIERA – TABLA 4
   
    elementos.append(Paragraph("5. Proyección Financiera del Proyecto", estilo_seccion))

    tabla_pf = [
        ["Concepto", "Año 0", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5", "Total"],
        ["Beneficios", "-", "400,000", "400,000", "400,000", "400,000", "400,000", "2,000,000"],
        ["Costos (Inversión + Operación)", "591,300", "128,300", "119,300", "110,300",
         "102,300", "105,300", "1,156,800"],
        ["Flujos Netos", "-591,300", "271,700", "280,700", "289,700",
         "297,700", "294,700", "843,200"],
    ]

    tabla_pf_pdf = Table(tabla_pf, colWidths=[120,60,60,60,60,60,60,70])
    tabla_pf_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#002B5B")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTSIZE", (0,0), (-1,-1), 7),
    ]))

    elementos.append(tabla_pf_pdf)
    elementos.append(Spacer(1, 20))

   
    # 5.1 PERÍODO DE RECUPERACIÓN
   
    elementos.append(Paragraph("5.1 Período de Recuperación Normal", estilo_seccion))

    tabla_pr = [
        ["Año", "Flujo", "Acumulado"],
        ["1", "271,700", "271,700"],
        ["2", "280,700", "552,400"],
        ["3", "289,700", "842,100 ✔"],
    ]

    tabla_pr_pdf = Table(tabla_pr, colWidths=[60,80,80])
    tabla_pr_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#002B5B")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))

    elementos.append(tabla_pr_pdf)
    elementos.append(Spacer(1, 20))

   
    # 5.2 PERÍODO DE RECUPERACIÓN DESCONTADO
   
     # 5.2 PERÍODO DE RECUPERACIÓN DESCONTADO (SEGÚN TU EXCEL)
    elementos.append(Paragraph("5.2 Período de Recuperación Descontado", estilo_seccion))

    tabla_prd = [
    ["Año", "Flujo", "Acumulado"],
    ["1", "271,700", "271,700"],
    ["2", "280,700", "552,400"],
    ["3", "289,700", "842,100"],
    ["4", "297,700", "1,139,800"],
    ["5", "294,700", "1,434,500"],
]

    tabla_prd_pdf = Table(tabla_prd, colWidths=[60, 80, 100])
    tabla_prd_pdf.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#002B5B")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
]))
    elementos.append(tabla_prd_pdf)
    elementos.append(Spacer(1, 20))


   
    # 5.3 INDICADORES FINANCIEROS
   
    elementos.append(Paragraph("5.3 Indicadores Financieros Clave", estilo_seccion))

    tabla_ind = [
        ["Indicador", "Valor"],
        ["Valor Presente Total", "L 955,722"],
        ["Valor Presente Neto (VAN)", "L 364,422"],
    ]

    tabla_ind_pdf = Table(tabla_ind, colWidths=[200,150])
    tabla_ind_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#002B5B")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    elementos.append(tabla_ind_pdf)
    elementos.append(Spacer(1, 20))

   
    # 5.4 ROI
   
    elementos.append(Paragraph("5.4 Tasa Contable de Rendimiento (ROI)", estilo_seccion))

    tabla_roi = [
        ["Indicador", "Resultado"],
        ["ROI anual", "-9.14%"],
        ["ROI del proyecto", "-45.68%"],
        ["Índice de Rentabilidad", "1.6163 (61.63%)"],
    ]

    tabla_roi_pdf = Table(tabla_roi, colWidths=[200,150])
    tabla_roi_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#002B5B")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    elementos.append(tabla_roi_pdf)
    elementos.append(Spacer(1, 30))


    
    # 6. Histogramas de las variables simuladas (opcional)
    
    elementos.append(Paragraph("6. Histogramas de las variables de entrada", estilo_seccion))
    elementos.append(Spacer(1, 10))

    ruta_hist_vars = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "hist_variables.png"))
    if os.path.exists(ruta_hist_vars):
        try:
            img_hist = Image(ruta_hist_vars, width=450, height=160)
            elementos.append(img_hist)
        except Exception:
            elementos.append(Paragraph("No se pudo cargar la imagen de histogramas.", estilos["BodyText"]))
    else:
        elementos.append(Paragraph("No se encontró la imagen de histogramas (hist_variables.png).", estilos["BodyText"]))

    elementos.append(Spacer(1, 16))

  
    # TEXTO FINAL
   
    elementos.append(Paragraph(
        "Este informe muestra el comportamiento financiero del proyecto bajo incertidumbre "
        "y valida estadísticamente los generadores utilizados.",
        estilos["BodyText"]
    ))

    doc.build(elementos)
    return ruta
