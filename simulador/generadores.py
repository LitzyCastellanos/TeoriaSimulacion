import random
import numpy as np


# DISTRIBUCIONES BÁSICAS


def generar_uniforme(a, b):
    """Distribución uniforme: igual que Excel =a+R*(b-a)"""
    R = random.random()
    return a + R * (b - a)

def generar_normal(mu, sigma):
    """Distribución normal: NORM.INV(R; mu; sigma)"""
    return np.random.normal(mu, sigma)

def generar_discreta(valores, probabilidades):
    """Distribución discreta para costos fijos"""
    R = random.random()
    acumulada = 0
    for valor, prob in zip(valores, probabilidades):
        acumulada += prob
        if R <= acumulada:
            return valor
    return valores[-1]  # fallback



# FUNCIONES DE ALTO NIVEL PARA EL PROYECTO


def generar_demanda(a, b):
    """Genera demanda usando distribución uniforme"""
    return generar_uniforme(a, b)

def generar_precio(mu, sigma):
    """Genera precio con distribución normal"""
    return generar_normal(mu, sigma)

def generar_costo_variable(a, b):
    """Costo variable por unidad: uniforme"""
    return generar_uniforme(a, b)

def generar_costo_fijo(valores, probabilidades):
    """Costo fijo anual elegido por probabilidad"""
    return generar_discreta(valores, probabilidades)
