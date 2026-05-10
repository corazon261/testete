"""Sidebar component with dynamic filters."""

import pandas as pd
import streamlit as st

from utils.filters import clear_filters


def render_sidebar(df: pd.DataFrame) -> tuple[list[str], list[str], str]:
    """Render the sidebar with dynamic filters based on the DataFrame.

    Language and PR type filters are automatically populated with the unique
    values present in the CSV.

    Args:
        df: Normalized DataFrame used to extract filter options.

    Returns:
        Tuple ``(language, pr_type, period)`` with the currently selected values.
    """
    with st.sidebar:
        st.title("Filters")
        st.button("Clear", on_click=clear_filters, use_container_width=True)

        language_options: list[str] = (
            sorted(df["language"].dropna().unique().tolist())
            if "language" in df.columns
            else []
        )
        language: list[str] = st.multiselect(
            "Language", language_options, key="lang_filter"
        )

        pr_type_options: list[str] = (
            sorted(df["pr_type"].dropna().unique().tolist())
            if "pr_type" in df.columns
            else []
        )
        pr_type: list[str] = st.multiselect(
            "PR Type", pr_type_options, key="type_filter"
        )

        period: str = st.selectbox(
            "Period",
            ["All", "Last 7 days", "Last month"],
            key="period_filter",
        )

    return language, pr_type, period