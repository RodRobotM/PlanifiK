import unittest

from planifik_agent import generar_plan_semanal


class PlanifikAgentTests(unittest.TestCase):
    def test_genera_siete_dias(self):
        plan = generar_plan_semanal(["Tarea difícil A"], ["Micro 1", "Micro 2"])
        self.assertEqual(len(plan["plan_semanal"]), 7)

    def test_incluye_salud_y_ducha(self):
        plan = generar_plan_semanal(["Tarea difícil A"], ["Micro 1"])
        primer_dia = plan["plan_semanal"][0]

        self.assertIn("salud", primer_dia)
        self.assertIn("vitaminas", primer_dia["salud"])
        self.assertIn("agua_objetivo_litros", primer_dia["salud"])
        self.assertIn("calorias_objetivo_kcal", primer_dia["salud"])
        self.assertTrue(any(b["actividad"] == "Ducha" for b in primer_dia["bloques"]))

    def test_no_olvida_microtareas_ni_tareas_dificiles(self):
        tareas = ["Proyecto Alpha", "Proyecto Beta"]
        microtareas = ["Micro 1", "Micro 2", "Micro 3"]
        plan = generar_plan_semanal(tareas, microtareas)

        objetivos = {dia["objetivo_principal"] for dia in plan["plan_semanal"]}
        self.assertTrue(objetivos.issubset(set(tareas)))

        for dia in plan["plan_semanal"]:
            bloque_micro = next(b for b in dia["bloques"] if b["tipo"] == "microtareas")
            self.assertIn("Micro", bloque_micro["actividad"])


if __name__ == "__main__":
    unittest.main()
