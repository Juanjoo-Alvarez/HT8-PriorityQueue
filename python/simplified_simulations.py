#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Versión simplificada de la simulación de emergencias
Este script está diseñado para probar la generación de resultados
"""

import os
import random
import simpy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import json

# Crear directorio para resultados
OUTPUT_DIR = "resultados"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Se ha creado el directorio: {OUTPUT_DIR}")

# Datos simulados para prueba - estos datos son ficticios para probar la generación de resultados
def generate_test_data():
    patient_times = []
    for i in range(20):  # Generar datos para 20 pacientes ficticios
        severity = random.randint(1, 5)
        entry_time = random.uniform(0, 24)
        exit_time = entry_time + random.uniform(30, 180)
        patient_times.append({
            'patient_id': i+1,
            'severity': severity,
            'entry_time': entry_time,
            'exit_time': exit_time,
            'total_time': exit_time - entry_time
        })
    return patient_times

# Función para generar gráficos de prueba
def generate_test_charts(patient_times):
    try:
        # Convertir a DataFrame
        df = pd.DataFrame(patient_times)

        # 1. Gráfico simple de tiempo por severidad
        plt.figure(figsize=(10, 6))
        severity_stats = df.groupby('severity')['total_time'].mean().reset_index()
        plt.bar(severity_stats['severity'], severity_stats['total_time'])
        plt.title('Tiempo promedio por severidad')
        plt.xlabel('Severidad')
        plt.ylabel('Tiempo (minutos)')
        # Guardar gráfico
        output_path = os.path.join(OUTPUT_DIR, "test_severidad.png")
        plt.savefig(output_path)
        plt.close()
        print(f"Gráfico guardado en: {output_path}")

        # 2. Guardar datos en JSON
        output_json = os.path.join(OUTPUT_DIR, "test_results.json")
        with open(output_json, 'w') as f:
            json.dump({
                "patient_data": patient_times,
                "average_time": df['total_time'].mean(),
                "total_patients": len(df)
            }, f, indent=4)
        print(f"Datos JSON guardados en: {output_json}")

        return True
    except Exception as e:
        print(f"Error al generar gráficos: {str(e)}")
        return False

# Función principal
def main():
    print("=== PRUEBA DE GENERACIÓN DE RESULTADOS ===")

    # Generar datos de prueba
    print("Generando datos de prueba...")
    data = generate_test_data()

    # Generar gráficos y guardar resultados
    print("Generando gráficos y guardando resultados...")
    if generate_test_charts(data):
        print("¡La prueba ha sido exitosa! Verifica la carpeta 'resultados'")
    else:
        print("La prueba falló. Revisa los mensajes de error.")

if __name__ == "__main__":
    main()