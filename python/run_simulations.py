#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para ejecutar múltiples simulaciones de la sala de emergencias
con diferentes configuraciones y generar un informe comparativo.
"""

import os
import json
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_simulation_with_config(config_name, config):
    """Ejecuta la simulación con una configuración específica"""
    # Guardar configuración en un archivo temporal
    with open(f"config_{config_name}.json", 'w') as f:
        json.dump(config, f)

    # Ejecutar la simulación con esta configuración
    print(f"Ejecutando simulación con configuración: {config_name}")
    subprocess.run(["python", "emergency_simulation.py", f"config_{config_name}.json"])

    # Cargar resultados
    try:
        with open(f"resultados/emergency_simulation_results.json", 'r') as f:
            results = json.load(f)

        # Renombrar archivos para no sobreescribirlos
        for file in os.listdir("resultados"):
            if file.startswith("emergency_simulation"):
                os.rename(f"resultados/{file}", f"resultados/{config_name}_{file}")

        return results
    except Exception as e:
        print(f"Error al cargar resultados: {e}")
        return {}

def generate_comparison_report(results_dict):
    """Genera un informe comparativo de las diferentes configuraciones"""
    # Crear DataFrame con resultados
    comparison_data = []

    for config_name, results in results_dict.items():
        if not results:
            continue

        comparison_data.append({
            'Configuración': config_name,
            'Tiempo Promedio (min)': results.get('average_time_in_system', 0),
            'Pacientes Atendidos': results.get('total_patients', 0),
            'Doctores': results.get('simulation_parameters', {}).get('num_doctors', 0),
            'Enfermeras': results.get('simulation_parameters', {}).get('num_nurses', 0),
            'Enfermeras de Triage': results.get('simulation_parameters', {}).get('num_triage_nurses', 0),
            'Equipos de Rayos X': results.get('simulation_parameters', {}).get('num_xray', 0),
            'Laboratorios': results.get('simulation_parameters', {}).get('num_labs', 0)
        })

    if not comparison_data:
        print("No hay datos suficientes para generar el informe comparativo")
        return

    df = pd.DataFrame(comparison_data)

    # Guardar como CSV
    df.to_csv("resultados/comparacion_configuraciones.csv", index=False)

    # Generar gráfica comparativa
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Configuración', y='Tiempo Promedio (min)', data=df)
    plt.title('Comparación de Tiempo Promedio por Configuración')
    plt.xlabel('Configuración')
    plt.ylabel('Tiempo Promedio (minutos)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("resultados/comparacion_tiempos.png")

    # Generar informe de texto
    with open("resultados/informe_comparativo.txt", 'w') as f:
        f.write("INFORME COMPARATIVO DE CONFIGURACIONES\n")
        f.write("=====================================\n\n")

        f.write("Resumen de tiempos de atención:\n")
        for _, row in df.iterrows():
            f.write(f"- {row['Configuración']}: {row['Tiempo Promedio (min)']:.2f} minutos con {row['Pacientes Atendidos']} pacientes\n")

        f.write("\nDetalle de recursos por configuración:\n")
        for _, row in df.iterrows():
            f.write(f"\n{row['Configuración']}:\n")
            f.write(f"  - Doctores: {row['Doctores']}\n")
            f.write(f"  - Enfermeras: {row['Enfermeras']}\n")
            f.write(f"  - Enfermeras de Triage: {row['Enfermeras de Triage']}\n")
            f.write(f"  - Equipos de Rayos X: {row['Equipos de Rayos X']}\n")
            f.write(f"  - Laboratorios: {row['Laboratorios']}\n")

        # Encontrar configuración óptima (menor tiempo promedio)
        best_config = df.loc[df['Tiempo Promedio (min)'].idxmin()]
        f.write("\nCONFIGURACIÓN ÓPTIMA RECOMENDADA:\n")
        f.write(f"- {best_config['Configuración']} con {best_config['Tiempo Promedio (min)']:.2f} minutos de tiempo promedio\n")
        f.write(f"- Recursos: {best_config['Doctores']} doctores, {best_config['Enfermeras']} enfermeras, {best_config['Enfermeras de Triage']} enfermeras de triage, {best_config['Equipos de Rayos X']} equipos de rayos X, {best_config['Laboratorios']} laboratorios\n")

if __name__ == "__main__":
    # Asegurar que existe el directorio de resultados
    if not os.path.exists("resultados"):
        os.makedirs("resultados")

    # Configuración base
    base_config = {
        'num_triage_nurses': 2,
        'num_doctors': 3,
        'num_nurses': 5,
        'num_xray': 2,
        'num_labs': 2,
        'arrival_interval': 10,
        'day_factors': [0.8, 0.8, 0.9, 0.9, 1.0, 1.5, 1.2],
        'hour_factors': [0.5, 0.3, 0.7, 1.3, 1.5, 1.0],
        'severity_weights': [0.1, 0.25, 0.35, 0.2, 0.1],
        'nurse_salary_monthly': 1500,
        'doctor_salary_monthly': 4500,
        'xray_machine_cost': 120000,
        'lab_equipment_cost': 75000,
        'random_seed': 42,
        'sim_time': 24  # Simulación corta para pruebas
    }

    # Definir diferentes configuraciones para probar
    configurations = {
        "base": base_config,
        "mas_doctores": {**base_config, "num_doctors": 5},
        "mas_enfermeras": {**base_config, "num_nurses": 8},
        "mas_recursos_diagnóstico": {**base_config, "num_xray": 3, "num_labs": 3}
    }

    # Ejecutar simulaciones
    results = {}

    for name, config in configurations.items():
        result = run_simulation_with_config(name, config)
        results[name] = result

    # Generar informe comparativo
    generate_comparison_report(results)

    print("\nSimulaciones completadas. Informe comparativo generado en 'resultados/informe_comparativo.txt'")