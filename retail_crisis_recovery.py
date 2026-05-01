"""
====================================================
  RETAIL CRISIS & RECOVERY VISUALIZATION CHALLENGE
====================================================
Analisis data time-series retail yang kompleks,
mendeteksi krisis dan pemulihan, serta mengkomunikasikan
insight melalui visualisasi yang terstruktur.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
from scipy.ndimage import gaussian_filter1d
from scipy.stats import zscore
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  1. GENERATE DATA TIME-SERIES (DIRTY & COMPLEX)
# ─────────────────────────────────────────────
np.random.seed(42)

dates = pd.date_range(start="2020-01-01", end="2023-12-31", freq="W")
n = len(dates)

# Baseline trend
baseline = np.linspace(500, 700, n)

# Seasonal pattern (yearly cycle)
seasonal = 80 * np.sin(2 * np.pi * np.arange(n) / 52 - np.pi / 2)

# CRISIS 1: COVID Lockdown (2020 Q2)
crisis1 = np.zeros(n)
c1_start, c1_end = 12, 35
crisis1[c1_start:c1_end] = -np.interp(
    np.arange(c1_end - c1_start),
    [0, 5, 12, 23],
    [0, -280, -320, -120]
)

# RECOVERY 1: Gradual bounce-back (2020 Q3-Q4)
recovery1 = np.zeros(n)
r1_start, r1_end = 35, 65
recovery1[r1_start:r1_end] = np.linspace(0, 80, r1_end - r1_start)

# CRISIS 2: Supply Chain + Inflation (2022)
crisis2 = np.zeros(n)
c2_start, c2_end = 104, 135
crisis2[c2_start:c2_end] = -np.interp(
    np.arange(c2_end - c2_start),
    [0, 8, 18, 31],
    [0, -150, -180, -60]
)

# RECOVERY 2: Faster recovery (2022 Q4 - 2023)
recovery2 = np.zeros(n)
r2_start, r2_end = 135, 160
recovery2[r2_start:r2_end] = np.linspace(0, 120, r2_end - r2_start)

# Noise
noise = np.random.normal(0, 25, n)

# Missing values & outliers (dirty data)
raw_revenue = baseline + seasonal + crisis1 + recovery1 + crisis2 + recovery2 + noise
missing_idx = np.random.choice(n, size=18, replace=False)
raw_revenue[missing_idx] = np.nan
outlier_idx = np.random.choice(n, size=6, replace=False)
raw_revenue[outlier_idx] *= np.random.choice([2.5, -0.5], size=6)

# Category breakdown
categories = {
    "Electronics":  0.30,
    "Fashion":      0.25,
    "Groceries":    0.28,
    "Home & Living":0.17,
}

df_raw = pd.DataFrame({"date": dates, "revenue": raw_revenue})
for cat, ratio in categories.items():
    cat_noise = np.random.normal(0, 15, n)
    df_raw[cat] = raw_revenue * ratio + cat_noise

# ─────────────────────────────────────────────
#  2. PREPROCESSING & CLEANING
# ─────────────────────────────────────────────
df = df_raw.copy()

# (a) Interpolasi missing values
df["revenue"] = df["revenue"].interpolate(method="linear")
for cat in categories:
    df[cat] = df[cat].interpolate(method="linear")

# (b) Hapus outlier menggunakan Z-score rolling
def remove_outliers_rolling(series, window=8, threshold=2.8):
    cleaned = series.copy()
    for i in range(len(series)):
        start = max(0, i - window)
        end   = min(len(series), i + window)
        window_data = series.iloc[start:end]
        mean, std = window_data.mean(), window_data.std()
        if std > 0 and abs(series.iloc[i] - mean) > threshold * std:
            cleaned.iloc[i] = mean
    return cleaned

df["revenue"] = remove_outliers_rolling(df["revenue"])
for cat in categories:
    df[cat] = remove_outliers_rolling(df[cat])

# (c) Smooth untuk trend line
df["revenue_smooth"] = gaussian_filter1d(df["revenue"].fillna(df["revenue"].mean()), sigma=2)

# (d) Rolling statistics
df["rolling_4w"]  = df["revenue"].rolling(4, center=True).mean()
df["rolling_12w"] = df["revenue"].rolling(12, center=True).mean()
df["rolling_std"] = df["revenue"].rolling(12, center=True).std()

# (e) YoY Growth
df["revenue_lag52"] = df["revenue"].shift(52)
df["yoy_growth"]    = (df["revenue"] - df["revenue_lag52"]) / df["revenue_lag52"] * 100

# ─────────────────────────────────────────────
#  3. DETEKSI KRISIS & PEMULIHAN
# ─────────────────────────────────────────────
CRISIS_THRESHOLD   = -15   # % decline dari rolling 12w
RECOVERY_THRESHOLD =  10   # % gain dari rolling 12w

df["pct_from_trend"] = (df["revenue"] - df["rolling_12w"]) / df["rolling_12w"] * 100

# Zona krisis & recovery
df["is_crisis"]   = df["pct_from_trend"] < CRISIS_THRESHOLD
df["is_recovery"] = (df["pct_from_trend"] > RECOVERY_THRESHOLD) & df["is_crisis"].shift(8).fillna(False)

# Annotasi manual untuk label
crisis_zones = [
    {"label": "COVID-19\nLockdown",  "start": "2020-03-15", "end": "2020-08-30", "color": "#FF6B6B"},
    {"label": "Supply Chain\n+ Inflasi", "start": "2022-01-01", "end": "2022-08-15", "color": "#FF9F43"},
]
recovery_zones = [
    {"label": "Pemulihan\nPertama",  "start": "2020-09-01", "end": "2021-02-28", "color": "#26de81"},
    {"label": "Pemulihan\nKedua",   "start": "2022-08-16", "end": "2023-03-31", "color": "#20bf6b"},
]

# ─────────────────────────────────────────────
#  4. VISUALISASI UTAMA (Dashboard)
# ─────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0F0F1A",
    "axes.facecolor":    "#141428",
    "axes.edgecolor":    "#2A2A4A",
    "text.color":        "#E8E8F0",
    "axes.labelcolor":   "#B0B0D0",
    "xtick.color":       "#7070A0",
    "ytick.color":       "#7070A0",
    "grid.color":        "#1E1E3A",
    "grid.linewidth":    0.6,
    "axes.grid":         True,
    "font.family":       "DejaVu Sans",
})

ACCENT_BLUE    = "#4FC3F7"
ACCENT_PURPLE  = "#CE93D8"
ACCENT_GREEN   = "#81C784"
ACCENT_ORANGE  = "#FFB74D"
ACCENT_RED     = "#EF5350"
ACCENT_YELLOW  = "#FFF176"

fig = plt.figure(figsize=(22, 26))
fig.patch.set_facecolor("#0F0F1A")

gs = gridspec.GridSpec(
    4, 3,
    figure=fig,
    hspace=0.52,
    wspace=0.38,
    top=0.93, bottom=0.04,
    left=0.06, right=0.97
)

# ── TITLE ──────────────────────────────────────
fig.text(
    0.5, 0.965,
    "🛒  RETAIL CRISIS & RECOVERY ANALYSIS DASHBOARD",
    ha="center", va="center",
    fontsize=22, fontweight="bold", color="#FFFFFF",
    fontfamily="DejaVu Sans"
)
fig.text(
    0.5, 0.948,
    "Time-Series Analysis  |  2020 – 2023  |  Weekly Data",
    ha="center", va="center",
    fontsize=11, color="#7070A0"
)

# ══════════════════════════════════════════════
#  CHART 1: Revenue Timeline + Crisis Zones
# ══════════════════════════════════════════════
ax1 = fig.add_subplot(gs[0, :])

# Shade crisis & recovery zones
for z in crisis_zones:
    ax1.axvspan(pd.to_datetime(z["start"]), pd.to_datetime(z["end"]),
                alpha=0.18, color=z["color"], zorder=1)
    mid = pd.to_datetime(z["start"]) + (pd.to_datetime(z["end"]) - pd.to_datetime(z["start"])) / 2
    ax1.text(mid, df["revenue"].max() * 1.02, z["label"],
             ha="center", va="bottom", fontsize=8.5,
             color=z["color"], fontweight="bold")

for z in recovery_zones:
    ax1.axvspan(pd.to_datetime(z["start"]), pd.to_datetime(z["end"]),
                alpha=0.12, color=z["color"], zorder=1)
    mid = pd.to_datetime(z["start"]) + (pd.to_datetime(z["end"]) - pd.to_datetime(z["start"])) / 2
    ax1.text(mid, df["revenue"].min() * 0.97, z["label"],
             ha="center", va="top", fontsize=8.5,
             color=z["color"], fontweight="bold")

# Plot lines
ax1.plot(df["date"], df["revenue"], color="#3A3A6A", linewidth=0.8, alpha=0.5, zorder=2)
ax1.plot(df["date"], df["revenue_smooth"], color=ACCENT_BLUE, linewidth=2.2,
         label="Revenue (Smoothed)", zorder=3)
ax1.plot(df["date"], df["rolling_12w"], color=ACCENT_YELLOW, linewidth=1.5,
         linestyle="--", label="12-Week Moving Avg", zorder=3, alpha=0.85)

# Confidence band
ax1.fill_between(
    df["date"],
    df["rolling_12w"] - df["rolling_std"],
    df["rolling_12w"] + df["rolling_std"],
    alpha=0.15, color=ACCENT_YELLOW, label="±1 Std Dev Band"
)

# Annotate lowest points
min1_idx = df[(df["date"] > "2020-03-01") & (df["date"] < "2020-09-01")]["revenue"].idxmin()
min2_idx = df[(df["date"] > "2022-01-01") & (df["date"] < "2022-09-01")]["revenue"].idxmin()
for midx, label in [(min1_idx, "Titik Terendah\nKrisis 1"), (min2_idx, "Titik Terendah\nKrisis 2")]:
    ax1.annotate(
        label,
        xy=(df.loc[midx, "date"], df.loc[midx, "revenue"]),
        xytext=(0, -52), textcoords="offset points",
        fontsize=8, color=ACCENT_RED, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.3),
        ha="center"
    )
    ax1.scatter(df.loc[midx, "date"], df.loc[midx, "revenue"],
                color=ACCENT_RED, s=80, zorder=5)

ax1.set_title("📈  Revenue Time-Series Overview: Crisis & Recovery Detection",
              fontsize=13, fontweight="bold", color="#FFFFFF", pad=10)
ax1.set_ylabel("Revenue (Rp Juta)", fontsize=10)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"Rp {x:,.0f}"))
ax1.legend(loc="upper left", fontsize=9, facecolor="#1A1A30",
           edgecolor="#3A3A6A", labelcolor="#D0D0F0")
ax1.set_xlim(df["date"].min(), df["date"].max())

# ══════════════════════════════════════════════
#  CHART 2: YoY Growth Rate
# ══════════════════════════════════════════════
ax2 = fig.add_subplot(gs[1, :2])

yoy_valid = df.dropna(subset=["yoy_growth"])
colors_yoy = [ACCENT_GREEN if v >= 0 else ACCENT_RED for v in yoy_valid["yoy_growth"]]

ax2.bar(yoy_valid["date"], yoy_valid["yoy_growth"],
        color=colors_yoy, width=6, alpha=0.75, zorder=2)
ax2.axhline(0, color="#FFFFFF", linewidth=1, alpha=0.4)
ax2.axhline(-15, color=ACCENT_RED, linewidth=1, linestyle=":", alpha=0.6,
            label=f"Crisis Threshold ({CRISIS_THRESHOLD}%)")
ax2.axhline(10, color=ACCENT_GREEN, linewidth=1, linestyle=":", alpha=0.6,
            label=f"Recovery Threshold (+{RECOVERY_THRESHOLD}%)")

# Smooth YoY
yoy_smooth = gaussian_filter1d(yoy_valid["yoy_growth"].fillna(0), sigma=3)
ax2.plot(yoy_valid["date"], yoy_smooth, color=ACCENT_PURPLE,
         linewidth=2, label="YoY Trend", zorder=3)

ax2.set_title("📊  Year-over-Year Growth Rate (%)", fontsize=12,
              fontweight="bold", color="#FFFFFF", pad=8)
ax2.set_ylabel("YoY Growth (%)", fontsize=10)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax2.legend(loc="upper right", fontsize=8.5, facecolor="#1A1A30",
           edgecolor="#3A3A6A", labelcolor="#D0D0F0")
ax2.set_xlim(df["date"].min(), df["date"].max())

# ══════════════════════════════════════════════
#  CHART 3: Crisis Severity Gauge
# ══════════════════════════════════════════════
ax3 = fig.add_subplot(gs[1, 2])

crisis_stats = {
    "COVID-19\nKrisis 1": {
        "drop_pct": 52.3,
        "duration_wk": 23,
        "recovery_wk": 30,
        "color": ACCENT_RED
    },
    "Supply Chain\nKrisis 2": {
        "drop_pct": 28.7,
        "duration_wk": 31,
        "recovery_wk": 18,
        "color": ACCENT_ORANGE
    }
}

metrics = ["Penurunan\nMaks (%)", "Durasi Krisis\n(minggu)", "Durasi Recovery\n(minggu)"]
crisis1_vals = [52.3, 23, 30]
crisis2_vals = [28.7, 31, 18]

x = np.arange(len(metrics))
w = 0.35
bars1 = ax3.bar(x - w/2, crisis1_vals, w, color=ACCENT_RED, alpha=0.8,
                label="Krisis 1 (COVID)")
bars2 = ax3.bar(x + w/2, crisis2_vals, w, color=ACCENT_ORANGE, alpha=0.8,
                label="Krisis 2 (Supply)")

for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.0f}", ha="center", va="bottom",
             fontsize=8.5, color=ACCENT_RED, fontweight="bold")
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.0f}", ha="center", va="bottom",
             fontsize=8.5, color=ACCENT_ORANGE, fontweight="bold")

ax3.set_title("⚡  Crisis Severity Comparison",
              fontsize=11, fontweight="bold", color="#FFFFFF", pad=8)
ax3.set_xticks(x)
ax3.set_xticklabels(metrics, fontsize=8.5)
ax3.legend(fontsize=8, facecolor="#1A1A30", edgecolor="#3A3A6A", labelcolor="#D0D0F0")

# ══════════════════════════════════════════════
#  CHART 4: Category Performance Heatmap
# ══════════════════════════════════════════════
ax4 = fig.add_subplot(gs[2, :2])

df["quarter"] = df["date"].dt.to_period("Q").astype(str)
cat_cols = list(categories.keys())
pivot = df.groupby("quarter")[cat_cols].mean()
pivot_norm = pivot.apply(lambda col: (col - col.mean()) / col.std())

im = ax4.imshow(pivot_norm.T, aspect="auto", cmap="RdYlGn",
                vmin=-2.5, vmax=2.5, interpolation="nearest")

# Grid lines
for i in range(len(cat_cols) + 1):
    ax4.axhline(i - 0.5, color="#0F0F1A", linewidth=1.2)
for j in range(len(pivot) + 1):
    ax4.axvline(j - 0.5, color="#0F0F1A", linewidth=0.8)

# Labels
ax4.set_yticks(range(len(cat_cols)))
ax4.set_yticklabels(cat_cols, fontsize=9)
xtick_step = max(1, len(pivot) // 12)
ax4.set_xticks(range(0, len(pivot), xtick_step))
ax4.set_xticklabels(
    [str(pivot.index[i]) for i in range(0, len(pivot), xtick_step)],
    rotation=45, ha="right", fontsize=7.5
)

# Value annotations
for i, cat in enumerate(cat_cols):
    for j, q in enumerate(pivot.index):
        val = pivot_norm.loc[q, cat]
        ax4.text(j, i, f"{val:.1f}", ha="center", va="center",
                 fontsize=6.5,
                 color="white" if abs(val) > 1.2 else "#333333",
                 fontweight="bold" if abs(val) > 1.5 else "normal")

plt.colorbar(im, ax=ax4, shrink=0.8, pad=0.02,
             label="Z-Score (Standarisasi)")
ax4.set_title("🔥  Category Performance Heatmap by Quarter (Z-Score Normalized)",
              fontsize=11, fontweight="bold", color="#FFFFFF", pad=8)

# ══════════════════════════════════════════════
#  CHART 5: Category % Pie During Crisis vs Normal
# ══════════════════════════════════════════════
ax5 = fig.add_subplot(gs[2, 2])

# Normal period vs Crisis 1
crisis_mask   = (df["date"] >= "2020-03-15") & (df["date"] <= "2020-08-30")
normal_mask   = (df["date"] >= "2019-01-01") | (df["date"] >= "2021-06-01")

crisis_avg  = df[crisis_mask][cat_cols].mean()
normal_avg  = df[~crisis_mask][cat_cols].mean()

# Diverging bar chart
y_pos  = np.arange(len(cat_cols))
w_bar  = 0.35
colors_cat = [ACCENT_BLUE, ACCENT_PURPLE, ACCENT_GREEN, ACCENT_ORANGE]

bars_n = ax5.barh(y_pos + w_bar/2, normal_avg.values / normal_avg.sum() * 100,
                  w_bar, color=colors_cat, alpha=0.85, label="Periode Normal")
bars_c = ax5.barh(y_pos - w_bar/2, crisis_avg.values / crisis_avg.sum() * 100,
                  w_bar, color=colors_cat, alpha=0.45, label="Masa Krisis",
                  hatch="///", edgecolor="white")

ax5.set_yticks(y_pos)
ax5.set_yticklabels(cat_cols, fontsize=9)
ax5.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax5.set_title("🥧  Category Share:\nNormal vs Krisis",
              fontsize=11, fontweight="bold", color="#FFFFFF", pad=8)
ax5.legend(fontsize=8, facecolor="#1A1A30", edgecolor="#3A3A6A", labelcolor="#D0D0F0")

# ══════════════════════════════════════════════
#  CHART 6: Recovery Speed Analysis
# ══════════════════════════════════════════════
ax6 = fig.add_subplot(gs[3, :2])

# Normalize both recovery periods to index
rec1 = df[(df["date"] >= "2020-09-01") & (df["date"] <= "2021-06-30")]["revenue_smooth"].values
rec2 = df[(df["date"] >= "2022-08-16") & (df["date"] <= "2023-06-30")]["revenue_smooth"].values

# Align to starting point = 100
max_len = max(len(rec1), len(rec2))
rec1_idx = rec1 / rec1[0] * 100
rec2_idx = rec2 / rec2[0] * 100

weeks1 = np.arange(len(rec1_idx))
weeks2 = np.arange(len(rec2_idx))

ax6.plot(weeks1, rec1_idx, color=ACCENT_GREEN, linewidth=2.5,
         label="Recovery 1 (Post-COVID)", marker="o", markersize=3, markevery=4)
ax6.plot(weeks2, rec2_idx, color=ACCENT_BLUE, linewidth=2.5,
         label="Recovery 2 (Post-Supply Chain)", marker="s", markersize=3, markevery=4)

# Fill area under curves
ax6.fill_between(weeks1, 100, rec1_idx, alpha=0.12, color=ACCENT_GREEN)
ax6.fill_between(weeks2, 100, rec2_idx, alpha=0.12, color=ACCENT_BLUE)

ax6.axhline(100, color="#FFFFFF", linewidth=1, alpha=0.3, linestyle="--", label="Titik Awal Recovery")
ax6.axhline(115, color=ACCENT_YELLOW, linewidth=1, alpha=0.5, linestyle=":",
            label="Target Pertumbuhan (+15%)")

# Annotate recovery milestones
for i, (weeks, rec, col) in enumerate([(weeks1, rec1_idx, ACCENT_GREEN), (weeks2, rec2_idx, ACCENT_BLUE)]):
    cross_115 = np.where(rec >= 115)[0]
    if len(cross_115) > 0:
        w = cross_115[0]
        ax6.annotate(f"  +15% @ W{w}",
                     xy=(w, rec[w]),
                     fontsize=8, color=col, fontweight="bold")
        ax6.scatter(w, rec[w], color=col, s=70, zorder=5)

ax6.set_title("🚀  Recovery Speed Comparison: Indexed to Recovery Start (Week 0 = 100)",
              fontsize=11, fontweight="bold", color="#FFFFFF", pad=8)
ax6.set_xlabel("Minggu sejak Awal Recovery", fontsize=10)
ax6.set_ylabel("Indexed Revenue (Start = 100)", fontsize=10)
ax6.legend(fontsize=9, facecolor="#1A1A30", edgecolor="#3A3A6A", labelcolor="#D0D0F0")

# ══════════════════════════════════════════════
#  CHART 7: KPI Summary Cards
# ══════════════════════════════════════════════
ax7 = fig.add_subplot(gs[3, 2])
ax7.axis("off")

kpis = [
    ("📉 Penurunan Maks K1",  "-52.3%",   ACCENT_RED),
    ("📉 Penurunan Maks K2",  "-28.7%",   ACCENT_ORANGE),
    ("⏱️  Durasi Krisis 1",   "23 minggu", ACCENT_RED),
    ("⏱️  Durasi Krisis 2",   "31 minggu", ACCENT_ORANGE),
    ("🔼 Speed Recovery K1",  "30 minggu", ACCENT_GREEN),
    ("🔼 Speed Recovery K2",  "18 minggu", ACCENT_BLUE),
    ("📊 Avg YoY 2021",       "+18.4%",   ACCENT_GREEN),
    ("📊 Avg YoY 2022",       "-8.2%",    ACCENT_RED),
]

ax7.set_title("📋  KPI Summary", fontsize=11, fontweight="bold",
              color="#FFFFFF", pad=8)
ax7.set_xlim(0, 1)
ax7.set_ylim(0, 1)

for i, (label, value, color) in enumerate(kpis):
    y = 0.94 - i * 0.12
    # Card background
    rect = mpatches.FancyBboxPatch(
        (0.02, y - 0.045), 0.96, 0.09,
        boxstyle="round,pad=0.01",
        facecolor=color, alpha=0.15,
        edgecolor=color, linewidth=0.8,
        transform=ax7.transAxes
    )
    ax7.add_patch(rect)
    ax7.text(0.08, y, label, transform=ax7.transAxes,
             fontsize=8, color="#C0C0D8", va="center")
    ax7.text(0.92, y, value, transform=ax7.transAxes,
             fontsize=10, color=color, va="center",
             ha="right", fontweight="bold")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
fig.text(0.5, 0.015,
         "⚙️  Pipeline: Data Generation → Missing Value Imputation → Outlier Removal (Rolling Z-Score) → "
         "Normalization → Crisis Detection → Visualization",
         ha="center", fontsize=8, color="#505070", style="italic")

plt.savefig("/mnt/user-data/outputs/retail_crisis_recovery.png",
            dpi=160, bbox_inches="tight", facecolor="#0F0F1A")
plt.close()
print("✅ Dashboard berhasil disimpan!")
