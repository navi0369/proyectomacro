# Generador de Gráficas - Documentación

## Descripción

El **Generador de Gráficas** es una nueva página del dashboard que permite a los usuarios crear gráficas personalizadas de líneas usando matplotlib. Esta funcionalidad está enfocada en generar visualizaciones simples y rápidas de series económicas completas.

## Características Principales

### ✅ Implementado
- **Selección de tablas**: Dropdown con todas las tablas disponibles en la base de datos
- **Selección de columnas**: Hasta 5 columnas por gráfica
- **Título personalizable**: Los usuarios pueden agregar títulos personalizados
- **Gráficas de líneas simples**: Usando matplotlib con estilo corporativo
- **Exportación automática**: Las gráficas se generan como imágenes PNG de alta calidad
- **Colores predefinidos**: Paleta de colores corporativos automática
- **Validación de datos**: Verificación de datos válidos antes de graficar

### 🚫 NO Implementado (por diseño)
- Anotaciones de valores
- Cuadros de medias por ciclo
- Tasas de crecimiento por período
- Líneas verticales de hitos
- Elementos gráficos adicionales del sistema completo

## Acceso

- **URL**: `/plotter`
- **Menú**: "Generador de Gráficas" en el sidebar principal
- **Ubicación**: Entre "Calculadora" y "Cuentas Nacionales"

## Uso

### 1. Seleccionar Tabla
- Elige una tabla del dropdown "Seleccionar Tabla"
- Se cargan automáticamente las columnas disponibles

### 2. Seleccionar Columnas
- Elige hasta 5 columnas para graficar
- Las columnas se muestran como líneas separadas
- Se excluyen automáticamente las columnas de año/tiempo

### 3. Título (Opcional)
- Agrega un título personalizado
- Si no se especifica, se genera automáticamente

### 4. Generar Gráfica
- Presiona "Generar Gráfica"
- La gráfica se muestra directamente en la página
- Se puede hacer clic derecho para guardar la imagen

## Especificaciones Técnicas

### Backend
- **Framework**: Dash con matplotlib backend
- **Datos**: Conexión directa a SQLite (`proyectomacro.db`)
- **Estilo**: Aplicación del estilo corporativo unificado
- **Resolución**: 300 DPI para alta calidad

### Frontend
- **Componentes**: Dash Bootstrap Components
- **Validación**: Tiempo real de selecciones
- **Mensajes**: Estados de éxito/error informativos
- **Responsivo**: Adaptable a diferentes tamaños de pantalla

### Limitaciones
- **Máximo 5 columnas** por gráfica para mantener legibilidad
- **Solo líneas simples**: No se incluyen elementos del sistema completo de gráficas
- **Datos numéricos**: Conversión automática con manejo de NaN

## Estructura de Archivos

```
src/proyectomacro/pages/plotter_matplotlib.py  # Página principal
src/proyectomacro/app.py                        # Registro de la página
func_auxiliares/graficos_utils.py               # Funciones de estilo
func_auxiliares/config.py                       # Configuración global
```

## Integración con el Sistema

### Funciones Utilizadas
- `load_validated_tables()`: Carga de datos validados
- `set_style()`: Aplicación del estilo corporativo
- `DB_PATH`: Ruta a la base de datos

### Estilo Corporativo
- **Colores**: Paleta predefinida con 6 colores principales
- **Tipografía**: Serif para consistencia
- **Grid**: Líneas punteadas con transparencia
- **Fuente**: Texto de fuente estándar del proyecto

## Casos de Uso Típicos

1. **Exploración rápida de datos**
   - Seleccionar tabla de interés
   - Visualizar 2-3 columnas principales
   - Identificar tendencias generales

2. **Comparación de series**
   - Seleccionar series relacionadas
   - Comparar comportamiento temporal
   - Identificar correlaciones visuales

3. **Presentaciones simples**
   - Generar gráficas limpias
   - Títulos personalizados
   - Exportar imágenes de alta calidad

## Notas de Desarrollo

### Decisiones de Diseño
- **Simplicidad**: Solo funcionalidad esencial para reducir complejidad
- **Rapidez**: Generación inmediata sin procesamiento pesado
- **Consistencia**: Uso del mismo estilo que el resto del sistema

### Futuras Expansiones Posibles
- Selección de rango de años
- Más tipos de gráficos (barras, área)
- Personalización de colores
- Exportación en múltiples formatos
- Integración con metadata YAML
