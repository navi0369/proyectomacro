# Dashboard Macroeconómico de Bolivia

## 🚀 Inicio Rápido para Usuarios

### Para usuarios de Windows:
1. **Doble clic** en `run_dashboard.bat`
2. El navegador se abrirá automáticamente en http://127.0.0.1:8050

### Para usuarios de Linux/Mac:
1. **Doble clic** en `run_dashboard.sh` 
2. O ejecutar desde terminal: `./run_dashboard.sh`
3. El navegador se abrirá automáticamente en http://127.0.0.1:8050

### Opción multiplataforma:
1. **Doble clic** en `launch_dashboard.py`
2. Se abrirá automáticamente el navegador

---

## 🛠️ Primera Instalación

Si es la primera vez que usa el sistema:

### Linux/Mac:
```bash
chmod +x install.sh
./install.sh
```

### Windows:
```cmd
python install.py
```

---

## 📊 Características del Dashboard

- **Cuentas Nacionales**: PIB por ramas de actividad, componentes del gasto
- **Sector Externo**: Balanza comercial, exportaciones, importaciones
- **Precios y Producción**: Índices de precios, producción sectorial
- **Sector Fiscal**: Ingresos, gastos, déficit/superávit
- **Deuda**: Deuda externa e interna
- **Empleo**: Tasas de empleo, desempleo, participación laboral
- **Pobreza**: Indicadores de pobreza y distribución del ingreso
- **Sector Monetario**: Agregados monetarios, tasas de interés

---

## 🔧 Para Desarrolladores

### Estructura del proyecto:
```
├── src/proyectomacro/           # Código principal
│   ├── app.py                   # Aplicación principal Dash
│   └── pages/                   # Páginas del dashboard
├── func_auxiliares/             # Funciones auxiliares
├── db/                         # Base de datos SQLite
├── assets/                     # Imágenes y archivos estáticos
├── run_dashboard.sh            # Launcher Linux/Mac
├── run_dashboard.bat           # Launcher Windows
└── launch_dashboard.py         # Launcher multiplataforma
```

### Ejecutar en modo desarrollo:
```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src:$PYTHONPATH"
python src/proyectomacro/app.py
```

---

## 📋 Requisitos del Sistema

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10+, Linux, macOS
- **RAM**: Mínimo 4GB recomendado
- **Navegador**: Chrome, Firefox, Safari, Edge (versiones recientes)

---

## 🆘 Solución de Problemas

### Error: "No se encontró el entorno virtual"
- Ejecute primero `install.sh` (Linux/Mac) o `install.py` (Windows)

### Error: "Módulo no encontrado"
- Verifique que todas las dependencias estén instaladas
- Ejecute nuevamente el script de instalación

### El navegador no se abre automáticamente
- Abra manualmente: http://127.0.0.1:8050

### Puerto ocupado
- Si el puerto 8050 está en uso, modifique `app.py` línea final:
  ```python
  app.run(debug=True, port=8051)  # Cambiar puerto
  ```

---

## 📞 Soporte

Para reportar problemas o sugerir mejoras, contacte al equipo de desarrollo.

---

**Dashboard Macroeconómico de Bolivia**  
*Análisis económico integral para la toma de decisiones*
