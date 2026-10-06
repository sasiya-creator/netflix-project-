from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_CANDIDATES = (ROOT / "Netflix.csv", ROOT / "netflix.csv", ROOT / "Netflix")
REQUIRED_COLUMNS = {"Region", "Monthly_Revenue", "Subscription_Plan", "Rating", "Category"}

RED = "#E50914"
INK = "#090909"
PANEL = "#151515"
WHITE = "#F5F5F1"
MUTED = "#A6A6A6"
GRID = "#303030"

st.set_page_config(page_title="Netflix Data Analysis", page_icon="N", layout="wide")

st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: dark;
        --ink: {INK};
        --panel: {PANEL};
        --red: {RED};
        --white: {WHITE};
        --muted: {MUTED};
    }}
    .stApp, [data-testid="stAppViewContainer"] > .main {{
        background: var(--ink);
        color: var(--white);
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ max-width: 1320px; padding-top: 2rem; padding-bottom: 3rem; }}
    .brand-row {{ display: flex; align-items: center; gap: 12px; margin-bottom: 1.2rem; }}
    .brand-mark {{
        display: grid; place-items: center; width: 42px; height: 48px;
        background: var(--red); color: white; font-size: 34px; font-weight: 800;
        line-height: 1; border-radius: 3px;
    }}
    .brand-name {{ color: var(--white); font-size: 12px; font-weight: 700; letter-spacing: 2px; }}
    .page-title {{ color: var(--white); font-size: clamp(2.4rem, 5vw, 3.5rem); font-weight: 800; line-height: 1; }}
    .page-subtitle {{ color: var(--muted); font-size: 14px; margin: 8px 0 26px; }}
    .section-label {{
        color: var(--red); font-size: 11px; font-weight: 700;
        letter-spacing: 1.7px; text-transform: uppercase; margin: 0 0 5px;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: var(--panel); border: 1px solid #292929; border-radius: 5px;
        padding: 14px 16px 8px;
    }}
    [data-testid="stMetric"] {{
        background: var(--panel); border: 1px solid #292929; border-left: 3px solid var(--red);
        border-radius: 4px; padding: 14px 18px;
    }}
    [data-testid="stMetricLabel"] {{ color: var(--muted); }}
    [data-testid="stMetricValue"] {{ color: var(--white); }}
    @media (max-width: 700px) {{
        .block-container {{ padding: 1.2rem 1rem 2rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data_path = next((path for path in DATA_CANDIDATES if path.is_file()), None)
    if data_path is None:
        raise FileNotFoundError("Could not find Netflix.csv beside app.py.")

    data = pd.read_csv(data_path)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(
            f"The dataset is missing required columns: {', '.join(sorted(missing_columns))}"
        )

    for column in ("Monthly_Revenue", "Rating"):
        data[column] = pd.to_numeric(data[column], errors="raise")
    if "Watch_Date" in data.columns:
        data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
    return data


def style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor(INK)
    axis.tick_params(colors=MUTED, labelsize=10)
    axis.xaxis.label.set_color(MUTED)
    axis.yaxis.label.set_color(MUTED)
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.grid(axis="y", color=GRID, linewidth=0.8)
    axis.set_axisbelow(True)


def make_bar_chart(values: pd.Series, ylabel: str, *, color: str = RED) -> plt.Figure:
    figure, axis = plt.subplots(figsize=(7.2, 3.5), facecolor=INK)
    style_axis(axis)
    bars = axis.bar(values.index.astype(str), values.values, color=color, width=0.58)
    axis.set_ylabel(ylabel, labelpad=10)
    axis.bar_label(
        bars,
        labels=[f"{value:,.0f}" for value in values.values],
        padding=4,
        color=WHITE,
        fontsize=9,
    )
    axis.margins(y=0.18)
    figure.tight_layout(pad=1.2)
    return figure


def make_line_chart(values: pd.Series) -> plt.Figure:
    figure, axis = plt.subplots(figsize=(7.2, 3.5), facecolor=INK)
    style_axis(axis)
    x_values = range(len(values))
    axis.plot(
        x_values,
        values.values,
        color=RED,
        marker="o",
        markersize=8,
        markerfacecolor=RED,
        markeredgecolor=WHITE,
        linewidth=2.5,
    )
    axis.set_xticks(list(x_values), values.index.astype(str))
    axis.set_ylabel("Total rating", labelpad=10)
    for x_value, y_value in zip(x_values, values.values):
        axis.annotate(
            f"{y_value:,.0f}",
            (x_value, y_value),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            color=WHITE,
            fontsize=9,
        )
    axis.margins(y=0.2)
    figure.tight_layout(pad=1.2)
    return figure


def make_pie_chart(values: pd.Series) -> plt.Figure:
    colors = [RED, "#F25C66", WHITE, "#A6A6A6", "#851019", "#D9D9D9", "#C62832", "#666666"]
    if len(values) > len(colors):
        colors = (colors * ((len(values) + len(colors) - 1) // len(colors)))[: len(values)]

    figure, axis = plt.subplots(figsize=(7.2, 3.7), facecolor=INK)
    axis.set_facecolor(INK)
    wedges, _, percentage_labels = axis.pie(
        values.values,
        colors=colors[: len(values)],
        startangle=90,
        counterclock=False,
        autopct="%1.0f%%",
        pctdistance=0.72,
        textprops={"color": WHITE, "fontsize": 9, "weight": "bold"},
        wedgeprops={"linewidth": 1.5, "edgecolor": INK},
    )
    for wedge, label in zip(wedges, percentage_labels):
        red, green, blue, _ = wedge.get_facecolor()
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        label.set_color("#111111" if luminance > 0.55 else WHITE)

    legend_labels = [f"{name}  |  {amount:,.0f}" for name, amount in values.items()]
    axis.legend(
        wedges,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(0.92, 0.5),
        frameon=False,
        labelcolor=WHITE,
        fontsize=8,
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
    '<div class="brand-row"><div class="brand-mark">N</div>'
    '<div class="brand-name">NETFLIX DATA ANALYSIS</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<h1 class="page-title">Viewing Report</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-subtitle">A closer look at revenue and ratings across the Netflix dataset.</p>',
    unsafe_allow_html=True,
)

try:
    netflix = load_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    st.error(str(error))
    st.stop()

with st.sidebar:
    st.markdown("## Report filters")
    st.caption("Choose the records included in all four charts.")

    selected_filters: dict[str, list[str]] = {}
    for column, label in (
        ("Region", "Region"),
        ("Subscription_Plan", "Subscription plan"),
        ("Category", "Category"),
    ):
        options = sorted(netflix[column].dropna().astype(str).unique().tolist())
        selected_filters[column] = st.multiselect(label, options, default=options)

    filtered_netflix = netflix.copy()
    for column, selected_values in selected_filters.items():
        filtered_netflix = filtered_netflix[
            filtered_netflix[column].astype("string").isin(selected_values)
        ]

    if "Watch_Date" in netflix.columns:
        valid_dates = netflix["Watch_Date"].dropna()
        if not valid_dates.empty:
            minimum_date = valid_dates.min().date()
            maximum_date = valid_dates.max().date()
            selected_date_range = st.date_input(
                "Watch date range",
                value=(minimum_date, maximum_date),
                min_value=minimum_date,
                max_value=maximum_date,
            )
            if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
                start_date, end_date = selected_date_range
                filtered_netflix = filtered_netflix[
                    filtered_netflix["Watch_Date"].dt.date.between(start_date, end_date)
                ]

    with st.expander("About these charts"):
        st.caption(
            "This report keeps to the four visualizations in Untitled(1).py: "
            "regional revenue, plan ratings, rating counts, and category revenue."
        )

if filtered_netflix.empty:
    st.warning("No records match the selected filters. Adjust the filters in the sidebar.")
    st.stop()

metric_columns = st.columns(3)
metric_columns[0].metric("Records in view", f"{len(filtered_netflix):,}")
metric_columns[1].metric(
    "Monthly revenue total", f"{filtered_netflix['Monthly_Revenue'].sum():,.0f}"
)
average_rating = filtered_netflix["Rating"].mean()
metric_columns[2].metric(
    "Average rating", f"{average_rating:.2f}" if pd.notna(average_rating) else "—"
)
st.caption(
    f"Showing {len(filtered_netflix):,} of {len(netflix):,} records. "
    "Revenue and rating totals below update with the selected filters."
)

st.write("")
left, right = st.columns(2, gap="large")
with left:
    show_chart(
        "Revenue by region",
        "Sum of monthly revenue · grouped by region",
        make_bar_chart(
            filtered_netflix.groupby("Region")["Monthly_Revenue"].sum(),
            "Monthly revenue",
        ),
    )
with right:
    show_chart(
        "Rating total by subscription plan",
        "Sum of record ratings · grouped by plan (not the average)",
        make_line_chart(
            filtered_netflix.groupby("Subscription_Plan")["Rating"].sum()
        ),
    )

left, right = st.columns(2, gap="large")
with left:
    show_chart(
        "Rating distribution",
        "Record count · grouped by rating value",
        make_bar_chart(
            filtered_netflix["Rating"].value_counts().sort_index(),
            "Number of ratings",
            color=WHITE,
        ),
    )
with right:
    show_chart(
        "Revenue by category",
        "Share of summed monthly revenue · grouped by category",
        make_pie_chart(
            filtered_netflix.groupby("Category")["Monthly_Revenue"]
            .sum()
            .sort_values(ascending=False)
        ),
    )

with st.expander("Dataset details and filtered records"):
    quality_columns = st.columns(3)
    quality_columns[0].metric("Dataset rows", f"{len(netflix):,}")
    quality_columns[1].metric("Missing cells", f"{int(netflix.isna().sum().sum()):,}")
    quality_columns[2].metric("Duplicate rows", f"{int(netflix.duplicated().sum()):,}")
    st.caption(
        f"Dataset dimensions: {netflix.shape[0]:,} rows × {netflix.shape[1]:,} columns."
    )
    st.dataframe(filtered_netflix, width="stretch", hide_index=True)
    st.download_button(
        "Download filtered records",
        data=filtered_netflix.to_csv(index=False),
        file_name="netflix_filtered.csv",
        mime="text/csv",
    )
