# Script de Exportación de Tablas a Excel

## Descripción

Script automatizado que exporta todas las tablas de la base de datos SQLite (`proyectomacro.db`) a archivos Excel, organizándolos por sección según la configuración definida en `pages.yml`.

## Características

- ✅ **Exportación automática**: Procesa todas las tablas de la base de datos
- 📁 **Organización por sección**: Crea carpetas según la estructura de `pages.yml`
- 🔄 **Creación automática de directorios**: Las carpetas se crean si no existen
- 📊 **Formato Excel**: Exporta a `.xlsx` compatible con Microsoft Excel y LibreOffice
- 📈 **Reportes detallados**: Muestra progreso y resumen de la exportación

## Requisitos

- Python 3.7+
- Paquetes necesarios:
  - `pandas`
  - `openpyxl`
  - `pyyaml`

## Uso

### Desde el directorio `db/`:

```bash
cd db/
python exportar_tablas_excel.py
```

### Con entorno virtual activado:

```bash
source .venv/bin/activate
cd db/
python exportar_tablas_excel.py
```

## Estructura de salida

El script crea la siguiente estructura en `db/tablas_excel/`:

```
tablas_excel/
├── cuentas_nacionales/
│   ├── PIB_Real_Gasto.xlsx
│   ├── pib_ramas.xlsx
│   ├── tasa_crecimiento_pib.xlsx
│   └── ...
├── sector_externo/
│   ├── balanza_comercial.xlsx
│   ├── flujo_divisas.xlsx
│   └── ...
├── exportaciones/
│   ├── exportacion_gas_natural.xlsx
│   ├── exportaciones_tradicionales.xlsx
│   └── ...
├── importaciones/
│   └── ...
├── precios_y_produccion/
│   └── ...
├── sector_fiscal/
│   └── ...
├── deuda/
│   └── ...
├── empleo/
│   └── ...
├── pobreza/
│   └── ...
├── sector_monetario/
│   └── ...
└── sin_clasificar/
    └── ... (tablas no definidas en pages.yml)
```

## Configuración

El script lee la configuración de secciones desde:
```
../src/proyectomacro/config/pages.yml
```

### Mapeo de tablas a secciones

El archivo `pages.yml` define qué tabla pertenece a cada sección:

```yaml
secciones:
  cuentas_nacionales:
    name: "Cuentas Nacionales"
    tablas:
      pib_real_gasto:
        tabla: "PIB_Real_Gasto"
        label: "PIB real por componentes de gasto"
```

## Tablas sin clasificar

Las tablas que existen en la base de datos pero no están definidas en `pages.yml` se exportan a la carpeta `sin_clasificar/`.

## Ejemplo de salida

```
======================================================================
🔄 EXPORTACIÓN DE TABLAS A EXCEL
======================================================================

📋 Cargando configuración de secciones...
   ✓ Configuración cargada: 52 tablas mapeadas

🗄️  Consultando tablas en la base de datos...
   ✓ Encontradas 54 tablas en la base de datos

📤 Iniciando exportación de tablas...
----------------------------------------------------------------------
📊 PIB_Real_Gasto
   → Destino: tablas_excel/cuentas_nacionales/PIB_Real_Gasto.xlsx
   ✅ Exportada exitosamente

...

======================================================================
📊 RESUMEN DE EXPORTACIÓN
======================================================================
✅ Exitosas:        54
❌ Fallidas:        0
⚠️  Sin clasificar: 3
📁 Total:           54

📂 Directorio de salida: /path/to/db/tablas_excel
======================================================================
```

## Mantenimiento

### Agregar una nueva sección

1. Edita `pages.yml` y agrega la nueva sección:
```yaml
nueva_seccion:
  name: "Nueva Sección"
  tablas:
    nueva_tabla:
      tabla: "nombre_tabla_db"
      label: "Etiqueta descriptiva"
```

2. Ejecuta el script nuevamente

### Solución de problemas

**Error: "No module named 'pandas'"**
```bash
pip install pandas openpyxl pyyaml
```

**Error: "Base de datos no encontrada"**
- Verifica que estés ejecutando el script desde el directorio `db/`
- Confirma que existe `proyectomacro.db`

**Error: "No se encontró pages.yml"**
- Verifica la ruta relativa: `../src/proyectomacro/config/pages.yml`
- El script asume ejecución desde `db/`

## Notas técnicas

- **Formato de Excel**: Usa el motor `openpyxl` para compatibilidad
- **Índices**: No incluye el índice de pandas en la exportación (`index=False`)
- **Codificación**: UTF-8 para correcta lectura de caracteres especiales
- **Sobrescritura**: Si un archivo ya existe, será sobrescrito

## Autor

Script generado automáticamente
Fecha: 2025-10-16

## Licencia

Uso interno del proyecto `proyectomacro`
