"""Chart and metrics rendering components for the dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.metrics import compute_metrics


def render_metrics(df: pd.DataFrame) -> None:
    """Render the summary metric cards at the top of the dashboard.

    Displays three metrics: total PRs, Bugfix/Feature ratio,
    and average AI clarity score.

    Args:
        df: Filtered DataFrame used to compute the metrics.
    """
    metrics = compute_metrics(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total PRs", metrics["total"])
    with col2:
        st.metric(
            "Bugfix vs Feature",
            f"{metrics['bugfix_pct']:.1f}% / {metrics['feature_pct']:.1f}%",
        )
    with col3:
        st.metric("Avg Clarity (AI)", f"{metrics['clarity']:.1f}/10")


def render_charts(df: pd.DataFrame) -> None:
    """Render the bar and pie charts in the dashboard.

    - Bar chart: distribution of PRs by programming language.
    - Donut chart: distribution by PR type with a fixed color map.

    Displays a warning if the DataFrame is empty after filtering.

    Args:
        df: Filtered and normalized DataFrame.
    """
    if df.empty:
        st.warning("No data found for the selected filters.")
        return

    col_bar, col_pie = st.columns(2)

    with col_bar:
        st.markdown("**PRs by Language**")
        if "language" in df.columns:
            lang_counts = df["language"].value_counts().reset_index()
            lang_counts.columns = ["Language", "Count"]
            fig_bar = px.bar(
                lang_counts,
                x="Language",
                y="Count",
                color_discrete_sequence=["#4A90E2"],
            )
            fig_bar.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_pie:
        st.markdown("**PR Type**")
        if "pr_type" in df.columns:
            type_counts = df["pr_type"].value_counts().reset_index()
            type_counts.columns = ["Type", "Count"]
            color_map: dict[str, str] = {
                "Bugfix": "#6C5CE7",
                "Feature": "#00B894",
                "Refactor": "#0984E3",
            }
            fig_pie = px.pie(
                type_counts,
                values="Count",
                names="Type",
                hole=0.4,
                color="Type",
                color_discrete_map=color_map,
            )
            fig_pie.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)