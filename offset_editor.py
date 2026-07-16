#!/usr/bin/env python3
"""
Editor Interactivo de Offsets para Gráficas de Tesis
═══════════════════════════════════════════════════════
Ejecutar con:
    cd /home/navi/projects/proyectomacro
    ./venv/bin/streamlit run offset_editor.py
"""

import json
import os
import re
import sys
import traceback

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

# ══════════════════════════════════════════════════════════════════════
# Configuración del proyecto
# ══════════════════════════════════════════════════════════════════════
PROJECT_ROOT = "/home/navi/projects/proyectomacro"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

st.set_page_config(
    page_title="Editor de Offsets — Tesis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════
# Estilos CSS y Atajos de Teclado
# ══════════════════════════════════════════════════════════════════════
st.markdown(
    """
    <style>
    /* Fuente monoespaciada para los text areas de código */
    .stTextArea textarea {
        font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', monospace;
        font-size: 12.5px;
        line-height: 1.5;
    }
    /* Maximizar ancho de la app y sacrificar márgenes */
    .block-container {
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    /* Botón de copiar */
    .copy-block { background: #1e1e2e; border-radius: 8px; padding: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inyectar Script JS para capturar Ctrl + Q en la ventana padre
st.components.v1.html(
    """
    <script>
        const parentDoc = window.parent.document;
        
        // Evitar registrar múltiples listeners al recargar la app
        if (!window.parent.__shortcut_registered) {
            window.parent.__shortcut_registered = true;
            
            parentDoc.addEventListener('keydown', function(e) {
                // Verificar si se presiona Ctrl + Q
                if (e.ctrlKey && (e.key === 'q' || e.key === 'Q')) {
                    e.preventDefault();
                    
                    // Buscar todos los botones en el documento padre
                    const buttons = parentDoc.querySelectorAll('button');
                    for (const btn of buttons) {
                        if (btn.innerText && btn.innerText.includes('Ejecutar Gráfica')) {
                            btn.click();
                            break;
                        }
                    }
                }
            });
        }
    </script>
    """,
    height=0,
    width=0,
)


# ══════════════════════════════════════════════════════════════════════
# Funciones de parseo
# ══════════════════════════════════════════════════════════════════════

def extract_dict_block(code: str, var_name: str):
    """
    Extrae un bloque de asignación 'var_name = {...}' del código fuente.
    Retorna: (bloque_completo, indice_inicio, indice_fin) o (None, -1, -1).
    """
    pattern = re.compile(rf"(?:^|\n)({re.escape(var_name)}\s*=\s*\{{)")
    match = pattern.search(code)
    if not match:
        return None, -1, -1

    assign_start = match.start(1)
    brace_start = code.index("{", assign_start)

    depth = 0
    i = brace_start
    while i < len(code):
        ch = code[i]
        if ch == "#":
            # Saltar comentarios de línea
            nl = code.find("\n", i)
            i = nl if nl != -1 else len(code)
            continue
        if ch in ("'", '"'):
            # Saltar cadenas
            quote = ch
            triple = code[i:i+3] in ('"""', "'''")
            if triple:
                end_q = code.find(code[i:i+3], i + 3)
                i = end_q + 3 if end_q != -1 else len(code)
            else:
                end_q = code.find(quote, i + 1)
                i = end_q + 1 if end_q != -1 else len(code)
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return code[assign_start:i + 1], assign_start, i + 1
        i += 1
    return None, -1, -1


def find_offset_dicts(code: str) -> dict:
    """
    Encuentra todos los dicts cuyo nombre de variable contiene 'offset'.
    Filtra dict comprehensions (e.g., {x: 0.8 for x in lista}).
    Retorna: {var_name: value_string, ...}
    """
    results = {}
    seen = set()
    for match in re.finditer(
        r"(?:^|\n)(\w*offset\w*)\s*=\s*\{", code, re.IGNORECASE
    ):
        var = match.group(1)
        if var in seen:
            continue
        seen.add(var)
        block, _, _ = extract_dict_block(code, var)
        if block is None:
            continue
        eq_pos = block.index("=")
        value_str = block[eq_pos + 1:].strip()
        # Filtrar dict comprehensions
        if re.search(r"\bfor\b.*\bin\b", value_str):
            continue
        results[var] = value_str
    return results


def replace_dict_in_code(code: str, var_name: str, new_value: str) -> str:
    """Reemplaza la asignación del dict en el código."""
    _, start, end = extract_dict_block(code, var_name)
    if start >= 0:
        return code[:start] + f"{var_name} = {new_value}" + code[end:]
    return code


def find_plotting_cells(notebook: dict) -> list:
    """
    Encuentra todas las celdas de código que contienen funciones de graficación.
    Retorna lista de tuplas (indice, primeras_lineas_resumen).
    """
    results = []
    for i, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"])
        if "init_base_plot" in src or "init_dual_axis_plot" in src:
            # Obtener un resumen: primera línea no vacía
            for line in src.split("\n"):
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    break
            summary = stripped[:80] if stripped else f"Celda {i}"
            results.append((i, src, summary))
    return results


# ══════════════════════════════════════════════════════════════════════
# Interfaz principal
# ══════════════════════════════════════════════════════════════════════
st.title("📊 Editor Interactivo de Offsets")
st.caption(
    "Carga un notebook, edita los offsets de posicionamiento y "
    "previsualiza la gráfica en tiempo real."
)

# ─── Input: ruta del notebook ──────────────────────────────────────
nb_path = st.text_input(
    "📂 Ruta del notebook (.ipynb):",
    value=st.session_state.get("last_path", ""),
    placeholder="/home/navi/projects/proyectomacro/notebooks/tesis/serie_completa/...",
    key="nb_path_input",
)

if nb_path:
    st.session_state["last_path"] = nb_path

if not nb_path:
    st.info("👆 Pega la ruta absoluta de un notebook `.ipynb` para comenzar.")
    st.stop()

if not os.path.exists(nb_path):
    st.error(f"❌ Archivo no encontrado: `{nb_path}`")
    st.stop()

if not nb_path.endswith(".ipynb"):
    st.error("❌ El archivo debe ser un notebook `.ipynb`")
    st.stop()

# ─── Cargar notebook ──────────────────────────────────────────────
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Buscar celdas de graficación
plotting_cells = find_plotting_cells(nb)

if not plotting_cells:
    st.warning(
        "⚠️ No se encontró ninguna celda con `init_base_plot` o "
        "`init_dual_axis_plot` en este notebook."
    )
    st.stop()

# Si hay múltiples celdas de graficación, permitir seleccionar
if len(plotting_cells) > 1:
    cell_options = {
        f"Celda {idx} — {summary}": (idx, src)
        for idx, src, summary in plotting_cells
    }
    selected_label = st.selectbox(
        "📋 Selecciona la celda de graficación:",
        options=list(cell_options.keys()),
    )
    cell_idx, cell_code = cell_options[selected_label]
else:
    cell_idx, cell_code, _ = plotting_cells[0]

# Extraer dicts de offsets
offset_dicts = find_offset_dicts(cell_code)

if not offset_dicts:
    st.warning(
        "⚠️ No se encontraron diccionarios de offsets en la celda seleccionada."
    )
    st.stop()

st.success(
    f"✅ Notebook cargado — celda **{cell_idx}** — "
    f"**{len(offset_dicts)}** diccionarios encontrados: "
    + ", ".join(f"`{k}`" for k in offset_dicts)
)

# ─── Layout: Editores | Gráfica ─────────────────────────────────
col_edit, col_plot = st.columns([1, 3.2], gap="medium")

with col_edit:
    st.subheader("✏️ Editar Offsets")

    edited = {}
    for var_name, value_str in offset_dicts.items():
        with st.expander(f"📝 `{var_name}`", expanded=True):
            edited[var_name] = st.text_area(
                label=var_name,
                value=value_str,
                height=180,
                label_visibility="collapsed",
                key=f"ta_{var_name}",
            )

    st.divider()

    col_run, col_save = st.columns(2)
    with col_run:
        run_btn = st.button(
            "▶ Ejecutar Gráfica (Ctrl+Q)",
            type="primary",
            use_container_width=True,
            help="También puedes presionar Ctrl+Q desde cualquier campo de texto",
        )
    with col_save:
        save_btn = st.button(
            "💾 Guardar en notebook",
            use_container_width=True,
        )

with col_plot:
    st.subheader("📈 Vista Previa")
    plot_placeholder = st.empty()
    status_placeholder = st.empty()
    copy_placeholder = st.container()

# ─── Guardar offsets de vuelta al notebook ──────────────────────
if save_btn:
    try:
        # Reconstruir el código de la celda con los offsets editados
        modified_src = cell_code
        for var_name, new_val in edited.items():
            modified_src = replace_dict_in_code(modified_src, var_name, new_val)

        # Actualizar la celda en el notebook
        code_cell_counter = -1
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                code_cell_counter += 1
                # Necesitamos encontrar la celda correcta por índice original
        
        # Encontrar la celda original por su contenido
        for cell in nb["cells"]:
            if cell["cell_type"] != "code":
                continue
            src = "".join(cell["source"])
            if src == cell_code:
                cell["source"] = modified_src.split("\n")
                # Reconstruct con newlines (cada línea excepto la última necesita \n)
                lines = modified_src.split("\n")
                cell["source"] = [
                    line + "\n" if i < len(lines) - 1 else line
                    for i, line in enumerate(lines)
                ]
                break

        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)

        status_placeholder.success(
            f"✅ Offsets guardados en `{os.path.basename(nb_path)}`"
        )
    except Exception as e:
        status_placeholder.error(f"❌ Error al guardar: {e}")

# ─── Ejecutar gráfica ────────────────────────────────────────────
if run_btn:
    # Construir código modificado
    mod_code = cell_code
    for var_name, new_val in edited.items():
        mod_code = replace_dict_in_code(mod_code, var_name, new_val)

    # Desactivar plt.close() para capturar la figura
    mod_code = mod_code.replace("plt.close()", "# plt.close() [desactivado]")

    with plot_placeholder.container():
        with st.spinner("Generando gráfica..."):
            _orig_savefig = plt.Figure.savefig
            saved_paths = []
            
            def custom_savefig(self, fname, *args, **kwargs):
                import pathlib
                # Resolver la ruta completa
                full_path = os.path.abspath(str(fname))
                saved_paths.append(full_path)
                # Ejecutar el guardado real en assets
                return _orig_savefig(self, fname, *args, **kwargs)

            try:
                plt.close("all")
                # Interceptamos la llamada a savefig
                plt.Figure.savefig = custom_savefig

                namespace = {"__builtins__": __builtins__}
                
                # Ejecutar todas las celdas de código de forma secuencial
                for i, cell in enumerate(nb["cells"]):
                    if cell["cell_type"] != "code":
                        continue
                    
                    cell_src = "".join(cell["source"])
                    if not cell_src.strip():
                        continue
                    
                    # Si es la celda de graficación seleccionada, usamos el código modificado
                    if i == cell_idx:
                        exec_code = mod_code
                    else:
                        # Para las demás celdas, removemos plt.show() o plt.close() si causan problemas, o simplemente las ejecutamos
                        exec_code = cell_src
                    
                    try:
                        exec(exec_code, namespace)
                    except Exception as cell_ex:
                        st.error(f"❌ Error al ejecutar la celda {i}:")
                        st.code(cell_src[:500] + ("..." if len(cell_src) > 500 else ""), language="python")
                        raise cell_ex

                # Verificar si se guardó alguna imagen
                if saved_paths:
                    target_img = saved_paths[-1]
                    if os.path.exists(target_img):
                        st.image(target_img, use_container_width=True)
                        status_placeholder.success(f"✅ Gráfica cargada de assets: `{os.path.basename(target_img)}`")
                    else:
                        st.warning(f"⚠️ Se llamó a savefig con `{target_img}` pero el archivo no existe.")
                        # Fallback a st.pyplot si no existe
                        fig = plt.gcf()
                        if fig.get_axes():
                            st.pyplot(fig, use_container_width=True)
                else:
                    fig = plt.gcf()
                    if not fig.get_axes():
                        st.warning("⚠️ La ejecución no generó ninguna gráfica ni llamó a savefig.")
                    else:
                        st.pyplot(fig, use_container_width=True)
                        status_placeholder.success("✅ Gráfica renderizada (no se detectó llamada a savefig)")

                plt.close("all")

            except Exception:
                st.error("❌ Error al ejecutar la celda")
                st.code(traceback.format_exc(), language="python")
            finally:
                plt.Figure.savefig = _orig_savefig

    # Mostrar sección para copiar los dicts finales
    with copy_placeholder:
        with st.expander("📋 Copiar offsets finales al notebook", expanded=False):
            st.caption(
                "Copia estos valores y pégalos directamente en tu notebook, "
                "o usa el botón **💾 Guardar en notebook**."
            )
            copy_code = "\n\n".join(
                f"{var_name} = {val}" for var_name, val in edited.items()
            )
            st.code(copy_code, language="python")

elif not save_btn:
    with plot_placeholder:
        st.caption(
            "Modifica los offsets en el panel izquierdo y haz clic en "
            "**▶ Ejecutar Gráfica** para ver la vista previa."
        )
