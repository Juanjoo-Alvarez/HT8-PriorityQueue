#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Simulación de Sala de Emergencias
Universidad del Valle de Guatemala
Algoritmos y Estructura de Datos - 2025

Simulación de una sala de emergencias utilizando SimPy para modelar
colas de prioridad y recursos con tiempo limitado.
"""

import simpy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import json

# Configuración de estilo para las gráficas
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

# Clase para reunir estadísticas
class EmergencyStats:
    def __init__(self):
        self.patient_times = []  # Tiempo total de cada paciente
        self.patient_wait_times = defaultdict(list)  # Tiempos de espera en cada etapa
        self.patient_severity = []  # Distribución de severidad
        self.daily_patients = defaultdict(int)  # Pacientes por día de la semana
        self.hourly_patients = defaultdict(int)  # Pacientes por hora del día
        self.resource_usage = defaultdict(list)  # Uso de recursos

    def add_patient_time(self, patient_id, severity, entry_time, exit_time, wait_times):
        """Registra el tiempo total de un paciente en el sistema"""
        total_time = exit_time - entry_time
        self.patient_times.append({
            'patient_id': patient_id,
            'severity': severity,
            'entry_time': entry_time,
            'exit_time': exit_time,
            'total_time': total_time
        })

        # Registrar tiempos de espera en cada etapa
        for stage, time in wait_times.items():
            self.patient_wait_times[stage].append({
                'patient_id': patient_id,
                'severity': severity,
                'wait_time': time
            })

        # Registrar severidad
        self.patient_severity.append(severity)

        # Registrar día y hora (simulados)
        day = int((entry_time // 24) % 7)  # 0-6 (lun-dom)
        hour = int(entry_time % 24)  # 0-23
        self.daily_patients[day] += 1
        self.hourly_patients[hour] += 1

    def log_resource_usage(self, resource_name, capacity, in_use, time):
        """Registra el uso de recursos a lo largo del tiempo"""
        self.resource_usage[resource_name].append({
            'time': time,
            'capacity': capacity,
            'in_use': in_use,
            'utilization': in_use / capacity if capacity > 0 else 0
        })

    def generate_report(self, simulation_params, file_prefix="emergency_simulation"):
        """Genera un informe con gráficas y estadísticas"""
        # Convertir a DataFrames para facilitar el análisis
        df_times = pd.DataFrame(self.patient_times)

        # Calcular estadísticas por severidad
        severity_stats = df_times.groupby('severity')['total_time'].agg(['mean', 'median', 'std', 'count']).reset_index()
        severity_stats.columns = ['Severidad', 'Tiempo Promedio (min)', 'Tiempo Mediano (min)', 'Desviación Estándar', 'Cantidad Pacientes']

        # Gráfica 1: Tiempo promedio por severidad
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x='Severidad', y='Tiempo Promedio (min)', data=severity_stats)
        plt.title('Tiempo Promedio de Atención por Nivel de Severidad')
        plt.xlabel('Nivel de Severidad (1: más urgente, 5: menos urgente)')
        plt.ylabel('Tiempo Promedio (minutos)')
        plt.tight_layout()
        plt.savefig(f"{file_prefix}_tiempo_por_severidad.png")

        # Gráfica 2: Distribución de pacientes por día de la semana
        days = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
                4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
        daily_df = pd.DataFrame([
            {'Día': days[day], 'Pacientes': count}
            for day, count in self.daily_patients.items()
        ])

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x='Día', y='Pacientes', data=daily_df)
        plt.title('Distribución de Pacientes por Día de la Semana')
        plt.xlabel('Día')
        plt.ylabel('Número de Pacientes')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{file_prefix}_pacientes_por_dia.png")

        # Gráfica 3: Distribución de pacientes por hora
        hourly_df = pd.DataFrame([
            {'Hora': hour, 'Pacientes': count}
            for hour, count in self.hourly_patients.items()
        ]).sort_values('Hora')

        plt.figure(figsize=(12, 6))
        ax = sns.barplot(x='Hora', y='Pacientes', data=hourly_df)
        plt.title('Distribución de Pacientes por Hora del Día')
        plt.xlabel('Hora (24h)')
        plt.ylabel('Número de Pacientes')
        plt.xticks(range(0, 24, 2))
        plt.tight_layout()
        plt.savefig(f"{file_prefix}_pacientes_por_hora.png")

        # Gráfica 4: Utilización de recursos a lo largo del tiempo
        for resource, usage_data in self.resource_usage.items():
            if not usage_data:
                continue

            resource_df = pd.DataFrame(usage_data)

            plt.figure(figsize=(14, 6))
            ax = sns.lineplot(x='time', y='utilization', data=resource_df)
            plt.title(f'Utilización de {resource} a lo largo del tiempo')
            plt.xlabel('Tiempo de Simulación (horas)')
            plt.ylabel('Tasa de Utilización')
            plt.ylim(0, 1.05)
            plt.tight_layout()
            plt.savefig(f"{file_prefix}_{resource}_utilizacion.png")

        # Gráfica 5: Comparativa de tiempos de espera por etapa
        wait_times_by_stage = {}
        for stage, times in self.patient_wait_times.items():
            df = pd.DataFrame(times)
            wait_times_by_stage[stage] = df.groupby('severity')['wait_time'].mean().reset_index()
            wait_times_by_stage[stage]['stage'] = stage

        wait_times_df = pd.concat(wait_times_by_stage.values())

        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='severity', y='wait_time', hue='stage', data=wait_times_df)
        plt.title('Tiempo Promedio de Espera por Etapa y Severidad')
        plt.xlabel('Severidad')
        plt.ylabel('Tiempo de Espera Promedio (minutos)')
        plt.legend(title='Etapa')
        plt.tight_layout()
        plt.savefig(f"{file_prefix}_tiempos_espera_por_etapa.png")

        # Guardar datos de simulación y resultados
        results = {
            "simulation_parameters": simulation_params,
            "severity_statistics": severity_stats.to_dict(orient='records'),
            "average_time_in_system": df_times['total_time'].mean(),
            "median_time_in_system": df_times['total_time'].median(),
            "total_patients": len(df_times),
            "daily_distribution": {days[day]: count for day, count in self.daily_patients.items()},
            "hourly_distribution": {str(hour): count for hour, count in self.hourly_patients.items()}
        }

        with open(f"{file_prefix}_results.json", 'w') as f:
            json.dump(results, f, indent=4)

        # Generar análisis económico
        self._generate_economic_analysis(simulation_params, file_prefix)

        return results

    def _generate_economic_analysis(self, params, file_prefix):
        """Genera un análisis económico basado en los recursos utilizados"""
        # Costos mensuales por tipo de recurso (valores ejemplo, ajustar según investigación)
        costs = {
            'nurses': params['nurse_salary_monthly'] * params['num_nurses'],
            'doctors': params['doctor_salary_monthly'] * params['num_doctors'],
            'triage_nurses': params['nurse_salary_monthly'] * params['num_triage_nurses'],
            'xray_machines': (params['xray_machine_cost'] / (5*12)) * params['num_xray'],  # Depreciar en 5 años
            'lab_equipment': (params['lab_equipment_cost'] / (3*12)) * params['num_labs']  # Depreciar en 3 años
        }

        # Calcular costo total mensual
        total_monthly_cost = sum(costs.values())

        # Estimar pacientes mensuales basado en la simulación
        total_sim_hours = params['sim_time']
        patients_per_hour = len(self.patient_times) / total_sim_hours
        estimated_monthly_patients = patients_per_hour * 24 * 30  # Pacientes estimados por mes

        # Calcular costo por paciente
        cost_per_patient = total_monthly_cost / estimated_monthly_patients if estimated_monthly_patients > 0 else 0

        # Calcular utilización promedio de recursos
        avg_utilization = {}
        for resource, usage_data in self.resource_usage.items():
            if usage_data:
                df = pd.DataFrame(usage_data)
                avg_utilization[resource] = df['utilization'].mean()

        # Crear gráfico de costos
        cost_df = pd.DataFrame([
            {'Recurso': resource, 'Costo Mensual ($)': cost}
            for resource, cost in costs.items()
        ])

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x='Recurso', y='Costo Mensual ($)', data=cost_df)
        plt.title('Distribución de Costos Mensuales por Tipo de Recurso')
        plt.xlabel('Tipo de Recurso')
        plt.ylabel('Costo Mensual ($)')
        plt.xticks(rotation=45)
        for i, v in enumerate(cost_df['Costo Mensual ($)']):
            ax.text(i, v + 100, f"${v:,.0f}", ha='center')
        plt.tight_layout()
        plt.savefig(f"{file_prefix}_distribucion_costos.png")

        # Crear gráfico comparativo de utilización vs costo
        if avg_utilization:
            util_cost_df = pd.DataFrame([
                {'Recurso': resource, 'Utilización Promedio': avg_utilization.get(resource, 0),
                 'Costo Relativo': costs.get(resource, 0) / total_monthly_cost if total_monthly_cost > 0 else 0}
                for resource in set(list(costs.keys()) + list(avg_utilization.keys()))
            ])

            plt.figure(figsize=(10, 6))
            ax1 = plt.gca()
            ax2 = ax1.twinx()

            sns.barplot(x='Recurso', y='Utilización Promedio', data=util_cost_df, ax=ax1, alpha=0.7, color='blue')
            sns.barplot(x='Recurso', y='Costo Relativo', data=util_cost_df, ax=ax2, alpha=0.4, color='red')

            ax1.set_ylabel('Utilización Promedio', color='blue')
            ax2.set_ylabel('Proporción del Costo Total', color='red')

            plt.title('Comparativa de Utilización vs Costo por Recurso')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{file_prefix}_utilizacion_vs_costo.png")

        # Guardar informe económico
        economic_results = {
            "costs": costs,
            "total_monthly_cost": total_monthly_cost,
            "estimated_monthly_patients": estimated_monthly_patients,
            "cost_per_patient": cost_per_patient,
            "average_resource_utilization": avg_utilization
        }

        with open(f"{file_prefix}_economic_analysis.json", 'w') as f:
            json.dump(economic_results, f, indent=4)


# Modelo de la sala de emergencias
class EmergencyRoom:
    def __init__(self, env, config):
        self.env = env
        self.config = config
        self.stats = EmergencyStats()

        # Crear recursos con prioridad
        self.triage_nurses = simpy.PriorityResource(env, capacity=config['num_triage_nurses'])
        self.doctors = simpy.PriorityResource(env, capacity=config['num_doctors'])
        self.nurses = simpy.PriorityResource(env, capacity=config['num_nurses'])
        self.xray = simpy.PriorityResource(env, capacity=config['num_xray'])
        self.lab = simpy.PriorityResource(env, capacity=config['num_labs'])

        # Contadores
        self.patient_counter = 0

        # Iniciar el registro periódico de uso de recursos
        env.process(self.monitor_resources())

    def monitor_resources(self):
        """Monitorea el uso de recursos a lo largo del tiempo"""
        while True:
            # Registrar el uso de cada recurso
            self.stats.log_resource_usage('triage_nurses',
                                           self.triage_nurses.capacity,
                                           len(self.triage_nurses.users),
                                           self.env.now)

            self.stats.log_resource_usage('doctors',
                                           self.doctors.capacity,
                                           len(self.doctors.users),
                                           self.env.now)

            self.stats.log_resource_usage('nurses',
                                           self.nurses.capacity,
                                           len(self.nurses.users),
                                           self.env.now)

            self.stats.log_resource_usage('xray',
                                           self.xray.capacity,
                                           len(self.xray.users),
                                           self.env.now)

            self.stats.log_resource_usage('lab',
                                           self.lab.capacity,
                                           len(self.lab.users),
                                           self.env.now)

            # Esperar antes de la próxima lectura
            yield self.env.timeout(1)  # Monitoreo cada hora simulada

    def get_severity(self):
        """Determina la severidad de un paciente (1-5, donde 1 es lo más grave)"""
        # Distribuir severidad con más probabilidad en valores intermedios
        weights = self.config['severity_weights']
        return random.choices([1, 2, 3, 4, 5], weights=weights)[0]

    def needs_xray(self, severity):
        """Determina si un paciente necesita rayos X basado en severidad"""
        # Pacientes más graves tienen mayor probabilidad de necesitar rayos X
        probabilities = {
            1: 0.8,  # 80% probabilidad para severidad 1
            2: 0.7,
            3: 0.5,
            4: 0.3,
            5: 0.2   # 20% probabilidad para severidad 5
        }
        return random.random() < probabilities[severity]

    def needs_lab(self, severity):
        """Determina si un paciente necesita pruebas de laboratorio basado en severidad"""
        # Pacientes más graves tienen mayor probabilidad de necesitar laboratorio
        probabilities = {
            1: 0.9,  # 90% probabilidad para severidad 1
            2: 0.8,
            3: 0.6,
            4: 0.4,
            5: 0.3   # 30% probabilidad para severidad 5
        }
        return random.random() < probabilities[severity]

    def patient_process(self, patient_id, arrival_time, day_of_week):
        """Proceso que simula el recorrido de un paciente por la sala de emergencias"""
        # Registrar tiempos de inicio
        entry_time = self.env.now
        wait_times = defaultdict(float)

        # Asignar severidad (en triage)
        severity = self.get_severity()

        # Ajustar tiempos según día de la semana
        weekend_factor = 1.2 if day_of_week >= 5 else 1.0  # Fines de semana más lentos

        print(f"Paciente {patient_id} llega a las {arrival_time:.2f}h con severidad {severity}")

        # 1. Registro y espera inicial
        initial_wait = max(0, random.expovariate(1.0 / (5 * weekend_factor * (severity / 3))))
        yield self.env.timeout(initial_wait)
        wait_times['registro'] = initial_wait

        # 2. Triage (evaluación inicial por enfermera)
        triage_start = self.env.now
        with self.triage_nurses.request(priority=severity) as req:
            yield req
            triage_wait = self.env.now - triage_start
            wait_times['triage'] = triage_wait

            # El proceso de triage toma tiempo
            triage_time = random.uniform(5, 15) * weekend_factor
            yield self.env.timeout(triage_time)

            print(f"Paciente {patient_id} (Severidad {severity}) completa triage a las {self.env.now:.2f}h")

        # 3. Espera para ver al doctor
        doctor_wait_start = self.env.now
        with self.doctors.request(priority=severity) as req:
            yield req
            doctor_wait = self.env.now - doctor_wait_start
            wait_times['doctor'] = doctor_wait

            # La consulta con el doctor toma tiempo
            # Pacientes más graves requieren más tiempo
            doctor_time = random.uniform(10, 30) * (1 + (6-severity)/10) * weekend_factor
            yield self.env.timeout(doctor_time)

            print(f"Paciente {patient_id} (Severidad {severity}) visto por doctor a las {self.env.now:.2f}h")

        # 4. Pruebas diagnósticas (si son necesarias)
        if self.needs_xray(severity):
            xray_wait_start = self.env.now
            with self.xray.request(priority=severity) as req:
                yield req
                xray_wait = self.env.now - xray_wait_start
                wait_times['rayos_x'] = xray_wait

                # El proceso de rayos X toma tiempo
                xray_time = random.uniform(15, 45) * weekend_factor
                yield self.env.timeout(xray_time)

                print(f"Paciente {patient_id} (Severidad {severity}) completa rayos X a las {self.env.now:.2f}h")

        if self.needs_lab(severity):
            lab_wait_start = self.env.now
            with self.lab.request(priority=severity) as req:
                yield req
                lab_wait = self.env.now - lab_wait_start
                wait_times['laboratorio'] = lab_wait

                # El proceso de laboratorio toma tiempo
                lab_time = random.uniform(20, 60) * weekend_factor
                yield self.env.timeout(lab_time)

                print(f"Paciente {patient_id} (Severidad {severity}) completa pruebas de laboratorio a las {self.env.now:.2f}h")

        # 5. Segunda consulta con el doctor (si fue a pruebas)
        if self.needs_xray(severity) or self.needs_lab(severity):
            follow_up_wait_start = self.env.now
            with self.doctors.request(priority=severity) as req:
                yield req
                follow_up_wait = self.env.now - follow_up_wait_start
                wait_times['segunda_consulta'] = follow_up_wait

                # La segunda consulta toma menos tiempo
                follow_up_time = random.uniform(5, 15) * weekend_factor
                yield self.env.timeout(follow_up_time)

                print(f"Paciente {patient_id} (Severidad {severity}) completa segunda consulta a las {self.env.now:.2f}h")

        # 6. Tratamiento por enfermera
        treatment_wait_start = self.env.now
        with self.nurses.request(priority=severity) as req:
            yield req
            treatment_wait = self.env.now - treatment_wait_start
            wait_times['enfermera'] = treatment_wait

            # El tratamiento toma tiempo según la severidad
            treatment_time = random.uniform(10, 40) * (1 + (6-severity)/10) * weekend_factor
            yield self.env.timeout(treatment_time)

            print(f"Paciente {patient_id} (Severidad {severity}) completa tratamiento a las {self.env.now:.2f}h")

        # 7. Paciente dado de alta
        exit_time = self.env.now
        total_time = exit_time - entry_time

        print(f"Paciente {patient_id} (Severidad {severity}) sale a las {exit_time:.2f}h, tiempo total: {total_time:.2f} minutos")

        # Registrar estadísticas del paciente
        self.stats.add_patient_time(patient_id, severity, entry_time, exit_time, wait_times)

    def generate_arrivals(self):
        """Genera la llegada de pacientes a la sala de emergencias"""
        while True:
            # El día de la semana afecta la tasa de llegada
            day_of_week = int((self.env.now // 24) % 7)  # 0-6 (lun-dom)
            hour_of_day = int(self.env.now % 24)  # 0-23

            # Factores para ajustar la tasa de llegada
            day_factor = self.config['day_factors'][day_of_week]
            hour_factor = self.config['hour_factors'][hour_of_day // 4]  # Dividir en bloques de 4 horas

            # Calcular intervalo entre llegadas
            adjusted_interval = self.config['arrival_interval'] / (day_factor * hour_factor)

            # Generar tiempo hasta la próxima llegada
            t = random.expovariate(1.0 / adjusted_interval)
            yield self.env.timeout(t)

            # Crear nuevo paciente
            self.patient_counter += 1
            self.env.process(self.patient_process(self.patient_counter, self.env.now, day_of_week))


def run_simulation(config, sim_time=168):  # 168 horas = 1 semana
    """Ejecuta la simulación de la sala de emergencias"""
    # Establecer semilla para reproducibilidad
    random.seed(config['random_seed'])

    # Crear entorno de simulación
    env = simpy.Environment()

    # Crear sala de emergencias
    er = EmergencyRoom(env, config)

    # Iniciar proceso de generación de pacientes
    env.process(er.generate_arrivals())

    # Ejecutar simulación
    env.run(until=sim_time)

    # Generar informe
    config['sim_time'] = sim_time
    results = er.stats.generate_report(config)

    return results


if __name__ == "__main__":
    # Configuración de la simulación
    config = {
        # Parámetros de recursos
        'num_triage_nurses': 2,
        'num_doctors': 3,
        'num_nurses': 5,
        'num_xray': 2,
        'num_labs': 2,

        # Parámetros de llegada de pacientes
        'arrival_interval': 30,  # Minutos promedio entre llegadas

        # Factores de día de semana (lunes a domingo)
        'day_factors': [0.8, 0.8, 0.9, 0.9, 1.0, 1.5, 1.2],  # Fin de semana más ocupado

        # Factores por hora del día (6 bloques de 4 horas)
        'hour_factors': [0.5, 0.3, 0.7, 1.3, 1.5, 1.0],  # Tarde/noche más ocupado

        # Distribución de severidad (1-5)
        'severity_weights': [0.1, 0.25, 0.35, 0.2, 0.1],  # Más casos de severidad media

        # Costos mensuales (en USD)
        'nurse_salary_monthly': 1500,
        'doctor_salary_monthly': 4500,
        'xray_machine_cost': 120000,  # Costo total del equipo
        'lab_equipment_cost': 75000,  # Costo total del equipamiento

        # Semilla para aleatoriedad
        'random_seed': 42
    }

    # Ejecutar simulación de una semana
    results = run_simulation(config, sim_time=168)

    print("\n=== RESULTADOS DE LA SIMULACIÓN ===")
    print(f"Tiempo promedio en el sistema: {results['average_time_in_system']:.2f} minutos")
    print(f"Pacientes atendidos: {results['total_patients']}")

    # Ejecutar simulaciones con diferentes configuraciones
    print("\n=== ANÁLISIS DE SENSIBILIDAD ===")

    # Variando el número de doctores
    doctor_configs = []
    for num_doctors in range(2, 7):
        config_variant = config.copy()
        config_variant['num_doctors'] = num_doctors
        result = run_simulation(
            config_variant,
            sim_time=168
        )
        doctor_configs.append({
            'num_doctors': num_doctors,
            'avg_time': result['average_time_in_system'],
            'total_cost': num_doctors * config['doctor_salary_monthly'] +
                        config['num_nurses'] * config['nurse_salary_monthly'] +
                        config['num_triage_nurses'] * config['nurse_salary_monthly']
        })
        print(f"Con {num_doctors} doctores: {result['average_time_in_system']:.2f} minutos de espera promedio")

    # Encontrar configuración óptima
    best_config = min(doctor_configs, key=lambda x: x['avg_time'])
    print(f"\nConfiguración óptima recomendada: {best_config['num_doctors']} doctores")
    print(f"Tiempo promedio de espera: {best_config['avg_time']:.2f} minutos")
    print(f"Costo mensual total estimado: ${best_config['total_cost']:,.2f}")

    print("\nReporte completo generado en los archivos emergency_simulation_*.png y emergency_simulation_results.json")