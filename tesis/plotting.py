import matplotlib.pyplot as plt

def apply_mpl_style():
    """Apply consistent Matplotlib style across thesis charts."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 14,
        "grid.linestyle": "--",
        "lines.linewidth": 2,
        "figure.dpi": 150,
        "savefig.bbox": "tight",
    })

