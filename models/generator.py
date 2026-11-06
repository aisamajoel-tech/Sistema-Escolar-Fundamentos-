"""
models/generator.py
Generador de la cohorte sintética de evaluación (120 estudiantes de 1.er año).

Escribe en data/:
- asistencia.csv  (Bedelía)
- campus.csv      (campus virtual / Moodle)
- notas.csv       (cátedras)
- historial.csv   (puntajes de las 3 corridas semanales anteriores)

Incluye casos ancla para la demostración:
- 24901 Lucas González   -> riesgo alto (~82)
- 24883 Camila Martínez  -> riesgo alto (~76)
- 25012 Sofía Gómez      -> riesgo alto (~73)
- 24945 Mateo Fernández  -> señales contradictorias (regla F3)
"""

import csv
import os
import random

RANDOM_SEED = 42
TOTAL_ESTUDIANTES = 120

NOMBRES = ["Lucas", "Camila", "Mateo", "Sofía", "Brian", "Julieta", "Tomás", "Valentina", "Agustín", "Lucía",
           "Facundo", "Martina", "Joaquín", "Micaela", "Nicolás", "Florencia", "Ignacio", "Paula", "Santiago",
           "Abril", "Gonzalo", "Candela", "Mariano", "Belén", "Federico", "Delfina", "Rodrigo", "Rocío",
           "Lautaro", "Zoe"]
APELLIDOS = ["González", "Martínez", "Fernández", "Gómez", "López", "Pérez", "Romero", "Díaz", "Álvarez",
             "Torres", "Ruiz", "Ramírez", "Flores", "Benítez", "Acosta", "Medina", "Herrera", "Suárez",
             "Aguirre", "Giménez", "Castro", "Molina", "Ortiz", "Silva", "Núñez", "Luna", "Juárez", "Cabrera",
             "Ríos", "Morales"]

COMISIONES = [
    {"comision": "Comisión 1 (Noche)", "turno": "Noche", "carrera": "Ing. en Sistemas de Información"},
    {"comision": "Comisión 2 (Mañana)", "turno": "Mañana", "carrera": "Ing. en Sistemas de Información"},
    {"comision": "Comisión 3 (Tarde)", "turno": "Tarde", "carrera": "Lic. en Informática"},
]

ANCLAS = [
    dict(legajo="24901", nombre="González, Lucas", **COMISIONES[0], asistencia=40.0, faltas=4, dias=12,
         tps=1, nota=3.5, descargas=2, hist=[14, 38, 62]),
    dict(legajo="24883", nombre="Martínez, Camila", **COMISIONES[1], asistencia=45.0, faltas=4, dias=10,
         tps=1, nota=4.0, descargas=3, hist=[20, 45, 58]),
    dict(legajo="25012", nombre="Gómez, Sofía", **COMISIONES[2], asistencia=50.0, faltas=3, dias=11,
         tps=1, nota=3.5, descargas=4, hist=[18, 32, 54]),
    dict(legajo="24945", nombre="Fernández, Mateo", **COMISIONES[1], asistencia=92.0, faltas=0, dias=14,
         tps=3, nota=7.0, descargas=0, hist=[10, 12, 15]),
]


def _perfil_aleatorio(rng: random.Random) -> dict:
    r = rng.random()
    if r < 0.15:   # vulnerable
        return dict(asistencia=round(rng.uniform(55, 72), 1), faltas=rng.randint(1, 3), dias=rng.randint(4, 9),
                    tps=rng.randint(1, 2), nota=round(rng.uniform(4.0, 6.0), 1), descargas=rng.randint(3, 10),
                    hist=sorted([rng.randint(10, 25), rng.randint(18, 35), rng.randint(25, 45)]))
    if r < 0.20:   # riesgo alto
        return dict(asistencia=round(rng.uniform(35, 50), 1), faltas=rng.randint(3, 5), dias=rng.randint(8, 16),
                    tps=rng.randint(0, 1), nota=round(rng.uniform(2.0, 4.0), 1), descargas=rng.randint(0, 4),
                    hist=sorted([rng.randint(15, 30), rng.randint(30, 50), rng.randint(45, 65)]))
    return dict(asistencia=round(rng.uniform(75, 98), 1), faltas=rng.randint(0, 1), dias=rng.randint(0, 3),
                tps=rng.choice([2, 3]), nota=round(rng.uniform(6.5, 9.5), 1), descargas=rng.randint(12, 35),
                hist=[rng.randint(5, 15), rng.randint(5, 18), rng.randint(5, 20)])


def generar_datos(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    rng = random.Random(RANDOM_SEED)

    estudiantes = [dict(a) for a in ANCLAS]
    usados = {a["nombre"] for a in ANCLAS}
    legajo = 25020
    while len(estudiantes) < TOTAL_ESTUDIANTES:
        nombre = f"{rng.choice(APELLIDOS)}, {rng.choice(NOMBRES)}"
        if nombre in usados:
            continue
        usados.add(nombre)
        estudiantes.append(dict(legajo=str(legajo), nombre=nombre, **rng.choice(COMISIONES), **_perfil_aleatorio(rng)))
        legajo += 1

    def escribir(nombre_archivo, encabezado, filas):
        with open(os.path.join(output_dir, nombre_archivo), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(encabezado)
            w.writerows(filas)

    escribir("asistencia.csv",
             ["legajo", "nombre", "comision", "turno", "carrera", "asistencia_acumulada_pct", "faltas_ultimas_2_semanas"],
             [[e["legajo"], e["nombre"], e["comision"], e["turno"], e["carrera"], e["asistencia"], e["faltas"]] for e in estudiantes])
    escribir("campus.csv",
             ["legajo", "dias_inactividad_campus", "recursos_descargados", "sesiones_semana"],
             [[e["legajo"], e["dias"], e["descargas"], max(0, 7 - e["dias"] // 2)] for e in estudiantes])
    escribir("notas.csv",
             ["legajo", "tps_entregados", "tps_exigidos", "calificacion_parcial_1"],
             [[e["legajo"], e["tps"], 3, e["nota"]] for e in estudiantes])
    escribir("historial.csv",
             ["legajo", "semana_1", "semana_2", "semana_3"],
             [[e["legajo"], *e["hist"]] for e in estudiantes])

    print(f"[generator] {len(estudiantes)} estudiantes generados en '{output_dir}'.")
    return estudiantes


if __name__ == "__main__":
    generar_datos(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
