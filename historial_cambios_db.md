# Informe de Cambios en la Base de Datos 'proyectomacro'
**Fecha del Informe:** 25 de mayo de 2026
**Periodo de Análisis:** 21 de mayo al 25 de mayo de 2026

Este documento resume los cambios realizados en la base de datos `proyectomacro` alojada en Turso durante los últimos 4 días. Los cambios fueron identificados comparando la versión actual descargada con el respaldo del 23 de mayo.

## 1. Actualización de Series de Tiempo (Nuevos Datos)
Se han actualizado varias tablas con datos correspondientes al año **2025**. A continuación se detallan los incrementos en el número de registros y el avance en la cobertura temporal:

| Tabla | Registros Anteriores | Registros Actuales | Incremento | Último Año (Ant.) | Último Año (Act.) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Reservas_oro_divisas | 75 | 76 | +1 | 2024 | 2025 |
| balanza_comercial | 76 | 77 | +1 | 2024 | 2025 |
| deuda_externa_total | 74 | 75 | +1 | 2024 | 2025 |
| exportaciones_totales | 44 | 46 | +2 | 2023 | 2025 |
| exportaciones_tradicionales | 33 | 34 | +1 | 2024 | 2025 |
| exportaciones_tradicionales_hidrocarburos | 33 | 34 | +1 | 2024 | 2025 |
| exportaciones_tradicionales_no_tradicionales | 45 | 46 | +1 | 2024 | 2025 |

## 2. Cambios en la Estructura de la Base de Datos
### Depuración de Tablas
Se han eliminado o consolidado las siguientes tablas que ya no son necesarias en la versión actual:
- `Participacion_PIB`
- `participacion_exp_trad_no_trad`
- `participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos`
- `participacion_hidrocarburos_minerales_exportaciones_tradicionales`

### Modificaciones de Esquema
- **exportaciones_tradicionales_hidrocarburos**:
  - Se añadió la columna: `total`
  - Se eliminó la columna: `hidrocarburos`

## 3. Resumen Ejecutivo para el Cliente
1. **Actualización de Datos:** La base de datos ahora cuenta con información proyectada o real hasta el año **2025** en indicadores clave como Reservas Internacionales, Balanza Comercial y Deuda Externa.
2. **Optimización:** Se eliminaron tablas de 'participación' redundantes, simplificando el esquema de la base de datos.
3. **Integridad:** Se ajustó la estructura de la tabla de exportaciones de hidrocarburos para incluir totales consolidados.