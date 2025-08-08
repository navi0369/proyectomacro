# Sistema de Metadatos Centralizados

## Resumen

Este sistema permite centralizar los metadatos de todas las tablas en un archivo YAML (`pages.yml`) en lugar de definirlos manualmente en cada página. Esto hace el código más limpio, mantenible y consistente.

## Estructura del Sistema

### 1. Archivo de Configuración (`src/proyectomacro/config/pages.yml`)

```yaml
secciones:
  cuentas_nacionales:
    name: "Cuentas Nacionales"
    path: "/cuentas-nacionales"
    tablas:
      pib_ramas:
        tabla: "pib_ramas"                    # ID de la tabla en la BD
        label: "Desagregación del PIB..."     # Etiqueta para mostrar
        metadata:                             # Metadatos centralizados
          nombre_descriptivo: "Descripción de la tabla"
          periodo: "1950–2022"
          unidades:
            "PIB Total": "Miles de bolivianos constantes de 1990"
            "Agricultura": "Miles de bolivianos constantes de 1990"
          fuentes:
            - "Instituto Nacional de Estadística (INE)"
            - "Banco Central de Bolivia (BCB)"
          notas:
            - "Datos preliminares para 2019–2022"
            - "Base año 1990 = 100"
```

### 2. Cargador de Configuración (`src/proyectomacro/config_loader.py`)

**Clases y funciones principales:**

- `ConfigLoader`: Clase principal que maneja la carga del YAML
- `get_table_metadata(table_id)`: Obtiene metadatos de una tabla por ID
- `get_table_config(table_id)`: Obtiene toda la configuración de una tabla

### 3. Funciones de Utilidad (`src/proyectomacro/page_utils.py`)

- `load_metadata_from_config(table_id)`: Carga metadatos desde YAML y los convierte al formato esperado por `build_metadata_panel`
- `create_metadata_helper()`: Función original (ahora como fallback)

## Uso en las Páginas

### Antes (método manual):
```python
# Cada página tenía que definir manualmente todos los metadatos
metadata = create_metadata_helper(
    nombre_descriptivo="Desagregación del PIB por sectores económicos",
    periodo="1950–2022",
    unidades={...},
    fuentes=[...],
    notas=[...]
)
```

### Después (método centralizado):
```python
# Los metadatos se cargan automáticamente desde la configuración
metadata = load_metadata_from_config(TABLE_ID)

# Fallback si no están definidos en YAML
if metadata is None:
    metadata = create_metadata_helper(...)  # valores por defecto
```

## Ventajas del Sistema

1. **Centralización**: Todos los metadatos en un solo lugar
2. **Consistencia**: Formato uniforme para todas las tablas
3. **Mantenibilidad**: Cambios globales desde un archivo
4. **Escalabilidad**: Fácil agregar nuevas tablas
5. **Separación de responsabilidades**: Configuración separada del código

## Flujo de Trabajo para Agregar una Nueva Tabla

### 1. Definir en `pages.yml`:
```yaml
nueva_tabla:
  tabla: "nueva_tabla_bd"
  label: "Descripción de la nueva tabla"
  metadata:
    nombre_descriptivo: "..."
    periodo: "..."
    unidades: {...}
    fuentes: [...]
    notas: [...]
```

### 2. Crear la página:
```python
# src/proyectomacro/pages/seccion/nueva_tabla.py
TABLE_ID = "nueva_tabla_bd"

# Metadatos automáticos desde configuración
metadata = load_metadata_from_config(TABLE_ID)
if metadata is None:
    # Fallback manual si es necesario
    metadata = create_metadata_helper(...)
```

### 3. Resultado:
- Los metadatos se cargan automáticamente
- La página funciona inmediatamente
- Cambios futuros solo requieren editar el YAML

## Estructura de Metadatos Soportados

```yaml
metadata:
  nombre_descriptivo: str           # Descripción breve de la tabla
  periodo: str                      # Rango temporal (ej: "1950-2022")
  unidades:                         # Unidades de medida
    "Columna1": "Unidad1"          # Para columnas específicas
    "Columna2": "Unidad2"
  fuentes:                          # Lista de fuentes
    - "Fuente 1"
    - "Fuente 2" 
  notas:                           # Notas adicionales (opcional)
    - "Nota 1"
    - "Nota 2"
```

## Funciones de la API

### ConfigLoader
```python
config_loader = ConfigLoader()

# Obtener todas las secciones
sections = config_loader.get_sections()

# Obtener una sección específica
section = config_loader.get_section("cuentas_nacionales")

# Buscar tabla por ID
table_info = config_loader.find_table_by_id("pib_ramas")
```

### Funciones de Conveniencia
```python
# Obtener metadatos de una tabla
metadata = get_table_metadata("pib_ramas")

# Obtener configuración completa
config = get_table_config("pib_ramas")

# Cargar metadatos formateados para Dash
formatted_metadata = load_metadata_from_config("pib_ramas")
```

## Manejo de Errores

El sistema maneja graciosamente:
- Archivos YAML no encontrados o corruptos
- Tablas no definidas en la configuración
- Metadatos faltantes o incompletos

En todos estos casos, retorna `None` y permite usar el fallback manual.

## Extensiones Futuras

1. **Validación de esquemas**: Validar que los metadatos sigan un esquema específico
2. **Carga dinámica**: Recargar configuración sin reiniciar la aplicación
3. **Múltiples idiomas**: Soporte para metadatos en diferentes idiomas
4. **Herramientas de migración**: Scripts para migrar metadatos existentes al YAML

## Ejemplo Completo de Migración

### Página Actual (pib_ramas.py):
```python
# ✅ DESPUÉS: Código limpio y centralizado
TABLE_ID = "pib_ramas"

# Carga automática desde configuración
metadata = load_metadata_from_config(TABLE_ID)

# Fallback opcional para casos especiales
if metadata is None:
    metadata = create_metadata_helper(...)
```

### Resultado:
- **Líneas de código reducidas**: De ~25 líneas a ~5 líneas por página
- **Mantenimiento centralizado**: Un solo archivo para todos los metadatos
- **Consistencia garantizada**: Formato uniforme automático
- **Fácil escalabilidad**: Nuevas tablas requieren solo configuración YAML

Este sistema transforma la gestión de metadatos de un proceso manual y repetitivo a uno centralizado y automático, mejorando significativamente la mantenibilidad del proyecto.
