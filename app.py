from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_CANDIDATES = (ROOT / "Netflix", ROOT / "netflix.csv", ROOT / "Netflix.csv")
REQUIRED_COLUMNS = {"Region", "Monthly_Revenue", "Subscription_Plan", "Rating", "Category"}
RED = "#E50914"
PLOT_BACKGROUND = "#111111"
TEXT = "#F5F5F1"
MUTED = "#A6A6A6"
PIE_COLORS = ["#E50914", "#F25C66", "#FFFFFF", "#A6A6A6", "#851019", "#D9D9D9", "#C62832", "#666666"]

st.set_page_config(page_title="Netflix Viewing Report", page_icon="N", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

    :root {
        color-scheme: dark;
        --ink: #080808;
        --panel: #141414;
        --red: #E50914;
        --paper: #F5F5F1;
        --muted: #A6A6A6;
    }
    .stApp { background: var(--ink); color: var(--paper); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppViewContainer"] > .main { background: var(--ink); }
    .block-container { max-width: 1320px; padding-top: 2.2rem; padding-bottom: 3rem; }
    html, body, [class*="st-"], p, label { font-family: 'DM Sans', sans-serif; }
    .brand-row { display: flex; align-items: center; gap: 13px; margin-bottom: 1.2rem; }
    .brand-mark {
        display: grid; place-items: center; width: 42px; height: 48px;
        background: var(--red); color: white; font-family: 'Barlow Condensed', sans-serif;
        font-size: 35px; font-weight: 800; line-height: 1; border-radius: 3px;
    }
    .brand-name { color: var(--paper); font-size: 12px; font-weight: 700; letter-spacing: 2px; }
    .page-title {
        margin: 0; color: var(--paper); font-family: 'Barlow Condensed', sans-serif;
        font-size: 48px; font-weight: 700; line-height: 1.05;
    }
    .page-subtitle { color: var(--muted); font-size: 14px; margin: 8px 0 28px; }
    .section-label {
        color: var(--red); font-size: 11px; font-weight: 700;
        letter-spacing: 1.8px; text-transform: uppercase; margin: 0 0 5px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--panel); border: 1px solid #292929; border-radius: 4px;
        padding: 14px 16px 8px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] h3 { color: var(--paper); margin-bottom: 0; }
    [data-testid="stAlert"] { border-left-color: var(--red); }
    @media (max-width: 700px) {
        .block-container { padding: 1.3rem 1rem 2rem; }
        .page-title { font-size: 38px; }
        .brand-mark { width: 36px; height: 42px; font-size: 30px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data_path = next((path for path in DATA_CANDIDATES if path.is_file()), None)
    if data_path is None:
        raise FileNotFoundError("Could not find the Netflix CSV beside app.py.")

    data = pd.read_csv(data_path)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"The dataset is missing required columns: {', '.join(sorted(missing_columns))}")
    return data


def style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor(PLOT_BACKGROUND)
    axis.tick_params(colors=MUTED, labelsize=10)
    axis.xaxis.label.set_color(MUTED)
    axis.yaxis.label.set_color(MUTED)
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.grid(axis="y", color="#303030", linewidth=0.8)
    axis.set_axisbelow(True)


def make_bar_chart(values: pd.Series, ylabel: str) -> plt.Figure:
    figure, axis = plt.subplots(figsize=(8, 3.6), facecolor=PLOT_BACKGROUND)
    style_axis(axis)
    bars = axis.bar(values.index.astype(str), values.values, color=RED, width=0.58)
    axis.set_ylabel(ylabel, labelpad=10)
    axis.grid(axis="y", color="#303030", linewidth=0.8)
    axis.bar_label(bars, labels=[f"{value:,.0f}" for value in values.values], padding=4, color=TEXT, fontsize=9)
    axis.margins(y=0.18)
    figure.tight_layout(pad=1.2)
    return figure


def make_pie_chart(values: pd.Series) -> plt.Figure:
    figure, axis = plt.subplots(figsize=(8, 3.8), facecolor=PLOT_BACKGROUND)
    axis.set_facecolor(PLOT_BACKGROUND)
    wedges, _, percentage_labels = axis.pie(
        values.values,
        colors=PIE_COLORS[: len(values)],
        startangle=90,
        counterclock=False,
        autopct="%1.0f%%",
        pctdistance=0.72,
        textprops={"color": TEXT, "fontsize": 9, "weight": "bold"},
        wedgeprops={"linewidth": 1.5, "edgecolor": PLOT_BACKGROUND},
    )
    for wedge, label in zip(wedges, percentage_labels):
        red, green, blue, _ = wedge.get_facecolor()
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        label.set_color("#111111" if luminance > 0.55 else TEXT)
    legend_labels = [f"{label}  |  {value:,.0f}" for label, value in values.items()]
    axis.legend(
        wedges,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(0.92, 0.5),
        frameon=False,
        labelcolor=TEXT,
        fontsize=9,
    )
    axis.set_aspect("equal")
    figure.tight_layout(pad=1.2)
    return figure


def show_chart(title: str, description: str, figure: plt.Figure) -> None:
    with st.container(border=True):
        st.markdown(f'<p class="section-label">{description}</p>', unsafe_allow_html=True)
        st.subheader(title)
        st.pyplot(figure, width="stretch")
        plt.close(figure)


st.markdown(
    '<div class="brand-row"><div class="brand-mark">N</div><div class="brand-name">NETFLIX DATA ANALYSIS</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<h1 class="page-title">Viewing Report</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-subtitle">Revenue and rating breakdowns from the Netflix dataset.</p>',
    unsafe_allow_html=True,
)

try:
    netflix = load_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    st.error(str(error))
    st.stop()

left, right = st.columns(2, gap="large")
with left:
    show_chart(
        "Revenue by region",
        "Monthly revenue · grouped by region",
        make_bar_chart(netflix.groupby("Region")["Monthly_Revenue"].sum(), "Monthly revenue"),
    )
with right:
    show_chart(
        "Rating by subscription plan",
        "Rating total · grouped by plan",
        make_pie_chart(netflix.groupby("Subscription_Plan")["Rating"].sum()),
    )

left, right = st.columns(2, gap="large")
with left:
    show_chart(
        "Rating distribution",
        "Number of records · grouped by rating",
        make_bar_chart(netflix["Rating"].value_counts().sort_index(), "Number of ratings"),
    )
with right:
    show_chart(
        "Revenue by category",
        "Monthly revenue · grouped by category",
        make_pie_chart(netflix.groupby("Category")["Monthly_Revenue"].sum().sort_values(ascending=False)),
    )