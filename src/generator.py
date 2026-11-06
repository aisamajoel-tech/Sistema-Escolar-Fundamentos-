"""
generator.py
Generador de cohorte sintética para el Sistema de Alerta Temprana (SITA-IA).
Genera 120 estudiantes ficticios distribuidos en 3 comisiones y turnos,
con casos controlados para demostrar las reglas A1, A2, A3, F1 y F3.
"""

import csv
import os
import random

RANDOM_SEED = 42
TOTAL_ESTUDIANTES = 120

NOMBRES = [
    "Lucas", "Camila", "Mateo", "Sofía", "Brian", "Julieta", "Tomás", "Valentina",
    "Agustín", "Lucía", "Facundo", "Martina", "Joaquín", "Micaela", "Nicolás",
    "Florencia", "Ignacio", "Paula", "Santiago", "Abril", "Gonzalo", "Candela",
    "Mariano", "Belén", "Federico", "Delfina", "Rodrigo", "Rocío", "Lautaro", "Zoe"
]

APELLIDOS = [
    "González", "Martínez", "Fernández", "Gómez", "López", "Pérez", "Romero",
    "Díaz", "Álvarez", "Torres", "Ruiz", "Ramírez", "Flores", "Benítez", "Acosta",
    "Medina", "Herrera", "Suárez", "Aguirre", "Giménez", "Castro", "Molina",
    "Ortiz", "Silva", "Nuñez", "Luna", "Juárez", "Cabrera", "Ríos", "Morales"
]

COMISIONES = [
    {"comision": "Comisión 1 (Noche)", "turno": "Noche", "carrera": "Ing. en Sistemas de Información"},
    {"comision": "Comisión 2 (Mañana)", "turno": "Mañana", "carrera": "Ing. en Sistemas de Información"},
    {"comision": "Comisión 3 (Tarde)", "turno": "Tarde", "carrera": "Lic. en Informática"},
]


def generar_datos(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    random.seed(RANDOM_SEED)

    estudiantes = []

    # 1. Caso X (Lucas González - Alto Riesgo controlado)
    estudiantes.append({
        "legajo": "24901",
        "nombre": "González, Lucas (Caso X)",
        "comision": "Comisión 1 (Noche)",
        "turno": "Noche",
        "carrera": "Ing. en Sistemas de Información",
        "asistencia_pct": 40.0,
        "faltas_ult_2sem": 4,
        "dias_inactivo_campus": 12,
        "tps_entregados": 1,
        "tps_totales": 3,
        "nota_parcial_1": 3.5,
        "descargas_material": 2,
        "consentimiento_datos": True
    })

    # 2. Caso F3 (Mateo Fernández - Conflicto: alta asistencia presencial pero campus inactivo)
    estudiantes.append({
        "legajo": "24945",
        "nombre": "Fernández, Mateo",
        "comision": "Comisión 1 (Tarde)",
        "turno": "Tarde",
        "carrera": "Ing. en Sistemas de Información",
        "asistencia_pct": 92.0,
        "faltas_ult_2sem": 0,
        "dias_inactivo_campus": 14,
        "tps_entregados": 3,
        "tps_totales": 3,
        "nota_parcial_1": 7.0,
        "descargas_material": 0,
        "consentimiento_datos": True
    })

    # 3. Caso Camila Martínez (Riesgo alto - problemas de rendimiento)
    estudiantes.append({
        "legajo": "24883",
        "nombre": "Martínez, Camila",
        "comision": "Comisión 2 (Mañana)",
        "turno": "Mañana",
        "carrera": "Ing. en Sistemas de Información",
        "asistencia_pct": 52.0,
        "faltas_ult_2sem": 3,
        "dias_inactivo_campus": 9,
        "tps_entregados": 1,
        "tps_totales": 3,
        "nota_parcial_1": 4.0,
        "descargas_material": 3,
        "consentimiento_datos": True
    })

    # 4. Caso Sofía Gómez (Riesgo medio-alto)
    estudiantes.append({
        "legajo": "25012",
        "nombre": "Gómez, Sofía",
        "comision": "Comisión 3 (Noche)",
        "turno": "Noche",
        "carrera": "Lic. en Informática",
        "asistencia_pct": 64.0,
        "faltas_ult_2sem": 2,
        "dias_inactivo_campus": 4,
        "tps_entregados": 2,
        "tps_totales": 3,
        "nota_parcial_1": 4.5,
        "descargas_material": 8,
        "consentimiento_datos": True
    })

    # Generar el resto de los 116 alumnos ficticios
    legajo_base = 25020
    for i in range(TOTAL_ESTUDIANTES - len(estudiantes)):
        legajo = str(legajo_base + i)
        nom = f"{random.choice(APELLIDOS)}, {random.choice(NOMBRES)}"
        com_info = random.choice(COMISIONES)
        
        # Perfiles mayoritariamente sanos o regulares
        rand_profile = random.random()
        if rand_profile < 0.15:
            # Riesgo moderado / vulnerable
            asistencia = round(random.uniform(55.0, 72.0), 1)
            faltas = random.randint(1, 3)
            inactivo_campus = random.randint(4, 9)
            tps = random.randint(1, 2)
            nota = round(random.uniform(4.0, 6.0), 1)
            descargas = random.randint(3, 10)
        elif rand_profile < 0.20:
            # Riesgo alto puntual
            asistencia = round(random.uniform(35.0, 50.0), 1)
            faltas = random.randint(3, 5)
            inactivo_campus = random.randint(8, 16)
            tps = random.randint(0, 1)
            nota = round(random.uniform(2.0, 4.0), 1)
            descargas = random.randint(0, 4)
        else:
            # Estudiante regular / buen rendimiento
            asistencia = round(random.uniform(75.0, 98.0), 1)
            faltas = random.randint(0, 1)
            inactivo_campus = random.randint(0, 3)
            tps = random.choice([2, 3])
            nota = round(random.uniform(6.5, 9.5), 1)
            descargas = random.randint(12, 35)

        estudiantes.append({
            "legajo": legajo,
            "nombre": nom,
            "comision": com_info["comision"],
            "turno": com_info["turno"],
            "carrera": com_info["carrera"],
            "asistencia_pct": asistencia,
            "faltas_ult_2sem": faltas,
            "dias_inactivo_campus": inactivo_campus,
            "tps_entregados": tps,
            "tps_totales": 3,
            "nota_parcial_1": nota,
            "descargas_material": descargas,
            "consentimiento_datos": True
        })

    # Escribir los 3 CSVs
    # 1. Asistencia
    path_asistencia = os.path.join(output_dir, "asistencia.csv")
    with open(path_asistencia, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["legajo", "nombre", "comision", "turno", "carrera", "asistencia_acumulada_pct", "faltas_ultimas_2_semanas"])
        for e in estudiantes:
            writer.writerow([e["legajo"], e["nombre"], e["comision"], e["turno"], e["carrera"], e["asistencia_pct"], e["faltas_ult_2sem"]])

    # 2. Campus
    path_campus = os.path.join(output_dir, "campus.csv")
    with open(path_campus, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["legajo", "dias_inactividad_campus", "recursos_descargados", "sesiones_semana"])
        for e in estudiantes:
            sesiones = max(0, 7 - (e["dias_inactivo_campus"] // 2))
            writer.writerow([e["legajo"], e["dias_inactivo_campus"], e["descargas_material"], sesiones])

    # 3. Notas
    path_notas = os.path.join(output_dir, "notas.csv")
    with open(path_notas, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["legajo", "tps_entregados", "tps_exigidos", "calificacion_parcial_1"])
        for e in estudiantes:
            writer.writerow([e["legajo"], e["tps_entregados"], e["tps_totales"], e["nota_parcial_1"]])

    print(f"[generator] Generados {len(estudiantes)} registros en '{output_dir}'.")
    return estudiantes


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    generar_datos(base)
