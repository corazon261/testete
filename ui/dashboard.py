"""
PR Insights Analyzer
Entry point for the Streamlit application for intelligent Pull Request analysis.
"""

import time

import pandas as pd
import streamlit as st

from components.charts import render_charts, render_metrics
from components.details import render_details_tab
from components.sidebar import render_sidebar
from utils.filters import apply_filters, clean_dataframe, clear_filters


def render_upload_section() -> None:
    """Render the CSV upload section and data preview.

    After file selection, displays a preview of the first 5 rows and a button
    to confirm processing. On confirmation, saves the DataFrame to
    ``st.session_state`` and triggers a rerun to show the dashboard.
    """
    file = st.file_uploader("Drag your CSV file here or select one", type=["csv"])

    if file is not None:
        df: pd.DataFrame = pd.read_csv(file)

        st.markdown("### Data Preview")
        st.dataframe(df.head(5), use_container_width=True, hide_index=True)

        if st.button(
            "Confirm and process with AI", type="primary", use_container_width=True
        ):
            with st.spinner("Processing data with AI..."):
                time.sleep(1.5)

            st.session_state.df_cache = df
            st.session_state.data_processed = True
            st.rerun()


def render_dashboard(df: pd.DataFrame) -> None:
    """Orchestrate the dashboard: normalize data, apply filters and render tabs.

    Args:
        df: Raw DataFrame stored in ``st.session_state.df_cache``.
    """
    df = clean_dataframe(df)

    language, pr_type, period = render_sidebar(df)
    df = apply_filters(df, language, pr_type, period)

    tab_dash, tab_details = st.tabs(["📊 Dashboard", "📋 Details"])

    with tab_dash:
        render_metrics(df)
        st.markdown("---")
        render_charts(df)

    with tab_details:
        render_details_tab(df)


def main() -> None:
    """Main entry point of the Streamlit application.

    Initializes session state, renders the header with navigation and decides
    which section to display: upload (initial state) or dashboard (after processing).
    """
    st.set_page_config(page_title="PR Insights Analyzer", layout="wide")

    if "data_processed" not in st.session_state:
        st.session_state.data_processed = False
    if "df_cache" not in st.session_state:
        st.session_state.df_cache = None

    col_title, col_nav = st.columns([4, 1])

    with col_title:
        st.title("PR Insights Analyzer")
        st.caption("Intelligent analysis powered by AI")

    with col_nav:
        st.write("")
        if st.session_state.data_processed:
            if st.button("New dataset", use_container_width=True):
                st.session_state.data_processed = False
                st.session_state.df_cache = None
                clear_filters()
                st.rerun()

    if not st.session_state.data_processed:
        render_upload_section()
    else:
        render_dashboard(st.session_state.df_cache)


if __name__ == "__main__":
    main()