#!/usr/bin/env python3
"""Agente local preprogramado para planificación semanal."""

from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import cycle, islice
from typing import Iterable

DIAS_SEMANA = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]


@dataclass(frozen=True)
class SaludBase:
    vitaminas_sugeridas: tuple[str, ...] = ("Vitamina D", "Complejo B", "Magnesio")
    objetivo_calorias_kcal: int = 2100
    objetivo_agua_litros: float = 2.2
    preparaciones: tuple[str, ...] = (
        "Meal prep de proteína y verduras",
        "Fruta + yogur natural para snack",
    )


def _distribuir_microtareas(microtareas: Iterable[str], por_dia: int = 2) -> list[list[str]]:
    microtareas_limpias = [m.strip() for m in microtareas if m.strip()]
    if not microtareas_limpias:
        microtareas_limpias = ["Revisión de pendientes rápidos", "Ordenar escritorio"]

    rotacion = cycle(microtareas_limpias)
    return [list(islice(rotacion, por_dia)) for _ in DIAS_SEMANA]


def _bloques_dia(dia: str, tarea_dificil: str, microtareas_dia: list[str], ducha_tarde: bool) -> list[dict[str, str]]:
    hora_ducha = "21:30" if ducha_tarde else "06:30"
    return [
        {"hora": "06:00", "actividad": "Hidratación inicial (500 ml agua)", "tipo": "cuidado"},
        {"hora": hora_ducha, "actividad": "Ducha", "tipo": "cuidado"},
        {"hora": "07:00", "actividad": "Desayuno + vitaminas", "tipo": "salud"},
        {"hora": "08:00", "actividad": f"Bloque profundo: {tarea_dificil}", "tipo": "tarea_dificil"},
        {"hora": "11:00", "actividad": "Microtareas: " + ", ".join(microtareas_dia), "tipo": "microtareas"},
        {"hora": "13:30", "actividad": "Almuerzo planificado (calorías controladas)", "tipo": "salud"},
        {"hora": "18:30", "actividad": f"Preparación saludable: {dia}", "tipo": "preparacion"},
        {"hora": "22:00", "actividad": "Cierre diario y planificación del siguiente día", "tipo": "organizacion"},
    ]


def generar_plan_semanal(tareas_dificiles: Iterable[str], microtareas: Iterable[str]) -> dict:
    tareas = [t.strip() for t in tareas_dificiles if t.strip()]
    if not tareas:
        tareas = ["Avanzar proyecto principal", "Resolver tarea técnica compleja"]

    salud = SaludBase()
    tareas_rotacion = cycle(tareas)
    micro_por_dia = _distribuir_microtareas(microtareas)

    dias = []
    for idx, dia in enumerate(DIAS_SEMANA):
        tarea_dificil = next(tareas_rotacion)
        micro_dia = micro_por_dia[idx]
        dias.append(
            {
                "dia": dia,
                "objetivo_principal": tarea_dificil,
                "bloques": _bloques_dia(dia, tarea_dificil, micro_dia, ducha_tarde=idx % 2 == 1),
                "salud": {
                    "vitaminas": list(salud.vitaminas_sugeridas),
                    "calorias_objetivo_kcal": salud.objetivo_calorias_kcal,
                    "agua_objetivo_litros": salud.objetivo_agua_litros,
                    "preparaciones": list(salud.preparaciones),
                },
            }
        )

    return {
        "agente": "PlanifiK Local Weekly Agent",
        "objetivo": "Avanzar tareas difíciles sin olvidar microtareas ni autocuidado",
        "plan_semanal": dias,
    }


def main() -> None:
    tareas_dificiles = [
        "Diseñar entregable estratégico",
        "Implementar módulo complejo",
        "Preparar presentación clave",
    ]
    microtareas = [
        "Responder correos críticos",
        "Actualizar tablero de tareas",
        "Revisar gastos semanales",
        "Confirmar citas pendientes",
    ]

    plan = generar_plan_semanal(tareas_dificiles, microtareas)
    print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
