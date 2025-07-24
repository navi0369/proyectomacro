# src/proyectomacro/validation/check_rules.py

from rules import load_rules, TableRule

def main():
    # Carga las reglas desde rules.yml
    rules = load_rules()

    # 1. Comprueba una tabla configurada en el YAML
    tr = rules.get("PIB_Real_Gasto", None)
    assert isinstance(tr, TableRule), "PIB_Real_Gasto no devolvió un TableRule"
    print("PIB_Real_Gasto.rule =", tr)
    print(".............")

    # 2. Comprueba una tabla inexistente, debe devolver defaults
    tr2 = rules.get("TABLA_INEXISTENTE", TableRule())
    # Todos los checks por defecto son True
    assert tr2.check_gaps is True,    "check_gaps debería ser True por defecto"
    assert tr2.check_outliers is True, "check_outliers debería ser True por defecto"
    print("Default rule =", tr2)

if __name__ == "__main__":
    main()
