"""Details tab and Pull Request modal components."""

import pandas as pd
import streamlit as st


@st.dialog("Pull Request Details", width="large")
def show_pr_details(row: pd.Series) -> None:
    """Display a modal with the full details of a selected Pull Request.

    Args:
        row: DataFrame row corresponding to the selected PR.
    """
    st.markdown(f"## {row.get('repo', 'N/A')}")
    st.caption(f"**Type:** {row.get('pr_type', 'N/A')}")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"**Language:** {row.get('language', 'N/A')}")
        st.markdown(f"**Author:** {row.get('author', 'N/A')}")

    with col_right:
        st.markdown(f"**Date:** {row.get('date', 'N/A')}")
        st.markdown(f"**Clarity (AI):** {row.get('clarity_score', 0)}/10")

    st.markdown("---")

    st.markdown("#### AI Analysis")
    st.markdown(f"**Classification:** {row.get('ai_classification', 'N/A')}")
    st.info(
        "This PR was automatically analyzed based on description clarity, "
        "provided context, and documentation quality. The clarity score considers "
        "the completeness of information and ease of understanding."
    )

    st.markdown("#### Description")
    st.write(
        row.get(
            "text",
            "Implementation of a new feature to improve the user experience.",
        )
    )

    st.markdown("---")

    col_github, col_analysis = st.columns(2)

    with col_github:
        st.button("View on GitHub", type="primary", use_container_width=True)
    with col_analysis:
        st.button("View full analysis", use_container_width=True)


def render_details_tab(df: pd.DataFrame) -> None:
    """Render the details tab with full-text search and an interactive table.

    Allows filtering data by free text and opening the PR details modal
    when a row is selected.

    Args:
        df: Filtered and normalized DataFrame used as the table source.
    """
    st.markdown("**Search by repository, type or language...**")
    search: str = st.text_input("Search", label_visibility="collapsed")

    df_display = df.copy()

    if search:
        mask = (
            df_display.astype(str)
            .apply(lambda col: col.str.contains(search, case=False, na=False))
            .any(axis=1)
        )
        df_display = df_display[mask]

    if df_display.empty:
        st.info("No results found for your search.")
        return

    if "date" in df_display.columns and pd.api.types.is_datetime64_any_dtype(
        df_display["date"]
    ):
        df_display["date"] = df_display["date"].dt.strftime("%d/%m/%Y")

    event = st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "clarity_score": st.column_config.ProgressColumn(
                "Clarity (AI)", format="%.1f", min_value=0, max_value=10
            ),
            "pr_type": st.column_config.TextColumn("Type"),
            "language": st.column_config.TextColumn("Language"),
            "repo": st.column_config.TextColumn("Repository"),
            "ai_classification": st.column_config.TextColumn("AI Classification"),
            "date": st.column_config.TextColumn("Date"),
            "author": st.column_config.TextColumn("Author"),
        },
    )

    if len(event.selection.rows) > 0:
        selected_idx: int = event.selection.rows[0]
        selected_row: pd.Series = df_display.iloc[selected_idx]
        show_pr_details(selected_row)