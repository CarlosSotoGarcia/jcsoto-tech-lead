# Cobertura de criterios de aceptación (PI1)

Cálculo del 2026-09-29 sobre las seis HUs de las corridas E1c y E3c, leídas de Mongo (`hus`): un criterio, explícito o inferido,
cuenta como cubierto si al menos un caso de prueba lo referencia en `criterio_ref`.

- `calcular_cobertura.py`: el cálculo (emparejamiento exacto, por contención o por similitud ≥ 0.85; en estas HUs todo emparejó exacto).
- `cobertura-pi1.json`: resumen por proyecto, fila por HU y detalle (casos por criterio, criterios sin cubrir, casos sin criterio).
- `cobertura-pi1.md`: la tabla por HU.

Resultado: 110 de 110 criterios cubiertos (33 explícitos y 77 inferidos), 145 casos, ninguno sin criterio. Se reporta en el
apartado 5.2.15 de la tesis con sus límites: mide que hay un caso por criterio, no que el caso sea suficiente; el 70 % de los
criterios los infirió la skill 1; los 50 supuestos no cuentan; y Loom no valida la cobertura en código.
