# Simulación de Sala de Emergencias Hospitalarias

Este módulo contiene la implementación en Python de una simulación para la sala de emergencias de un hospital, utilizando SimPy para modelar colas con prioridad y el flujo de pacientes.

## Archivos Incluidos

- `emergency_simulation.py`: Script principal de simulación
- `run_simulations.py`: Script auxiliar para ejecutar múltiples simulaciones con diferentes configuraciones
- `resources/config.json`: Archivo de configuración para la simulación

## Requisitos

- Python 3.8 o superior
- Bibliotecas: simpy, numpy, pandas, matplotlib, seaborn

## Instalación de Dependencias

```bash
pip install simpy numpy pandas matplotlib seaborn
```

## Cómo Ejecutar

### Simulación Básica

Para ejecutar una simulación simple con la configuración por defecto:

```bash
python emergency_simulation.py
```

Este comando generará gráficas y archivos de resultados en la carpeta `resultados/`.

### Comparación de Múltiples Configuraciones

Para ejecutar múltiples simulaciones con diferentes configuraciones y generar un informe comparativo:

```bash
python run_simulations.py
```

Este script probará varias configuraciones y generará un informe comparativo.

## Resultados Generados

Los resultados se guardan en la carpeta `resultados/` e incluyen:

1. **Gráficas**:
    - Tiempo promedio por nivel de severidad
    - Distribución de pacientes por día de la semana
    - Distribución de pacientes por hora del día
    - Utilización de recursos a lo largo del tiempo
    - Tiempo de espera por etapa y severidad
    - Distribución de costos mensuales
    - Comparativa de utilización vs costo

2. **Archivos de datos**:
    - `emergency_simulation_results.json`: Resultados detallados de la simulación
    - `emergency_simulation_economic_analysis.json`: Análisis económico
    - `comparacion_configuraciones.csv`: Tabla comparativa (solo con run_simulations.py)
    - `informe_comparativo.txt`: Informe de texto con recomendaciones (solo con run_simulations.py)

## Parámetros de Simulación

La simulación considera los siguientes parámetros:

1. **Recursos**:
    - Enfermeras de triage
    - Médicos
    - Enfermeras regulares
    - Equipos de rayos X
    - Equipamiento de laboratorio

2. **Patrones de Llegada**:
    - Variación por día de la semana
    - Variación por hora del día

3. **Severidad de Pacientes**:
    - Escala de 1 a 5 (1 = más urgente, 5 = menos urgente)
    - Distribución personalizable

4. **Costos**:
    - Salarios mensuales de personal
    - Costo de equipos médicos (depreciados)

## Personalización

Puedes modificar los parámetros de simulación editando el archivo `config.json` o directamente en el código.

### Parámetros Principales:

```python
config = {
    'num_triage_nurses': 2,  # Número de enfermeras de triage
    'num_doctors': 3,         # Número de médicos
    'num_nurses': 5,          # Número de enfermeras regulares
    'num_xray': 2,            # Equipos de rayos X
    'num_labs': 2,            # Unidades de laboratorio
    'arrival_interval': 10,   # Intervalo medio entre llegadas (minutos)
    'sim_time': 24            # Tiempo de simulación (horas)
}
```

## Notas Importantes

1. La simulación usa una semilla aleatoria fija para permitir comparaciones justas entre diferentes configuraciones.

2. Se han acelerado los tiempos para generar más pacientes en menos tiempo de simulación.

3. Si deseas una simulación más larga y realista, aumenta el parámetro `sim_time` a 168 (una semana completa).

4. Los tiempos de atención y probabilidades están basados en literatura sobre gestión hospitalaria, pero pueden ajustarse para reflejar situaciones específicas.

## Licencia

Este proyecto es parte de un trabajo académico para la Universidad del Valle de Guatemala, curso CC2003 - Algoritmos y Estructura de Datos.