"""Utility functions for cleaning and filtering the PR DataFrame."""

import pandas as pd
import streamlit as st

FILTER_DEFAULTS: dict[str, list | str] = {
    "lang_filter": [],
    "type_filter": [],
    "period_filter": "All",
}


def clear_filters() -> None:
    """Reset all sidebar filters to their default values.

    Sets each filter key in ``st.session_state`` back to its default — an
    empty list for multiselects and ``"All"`` for the period selectbox.

    Deleting the keys is not enough: Streamlit keeps the widget's internal
    value alive across reruns even when the key is absent. Explicitly writing
    the default is the only reliable way to reset the UI.
    """
    for key, default in FILTER_DEFAULTS.items():
        st.session_state[key] = default


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize text columns in the DataFrame to prevent filter inconsistencies.

    Operations applied:
    - ``pr_type``: strips whitespace and converts to Title Case (e.g. ``bugfix`` → ``Bugfix``).
    - ``language``: strips leading and trailing whitespace.

    Args:
        df: Raw DataFrame read from the user-uploaded CSV.

    Returns:
        A copy of the DataFrame with normalized columns.
    """
    df = df.copy()

    if "pr_type" in df.columns:
        df["pr_type"] = df["pr_type"].astype(str).str.strip().str.title()

    if "language" in df.columns:
        df["language"] = df["language"].astype(str).str.strip()

    return df


def apply_filters(
    df: pd.DataFrame,
    language: list[str],
    pr_type: list[str],
    period: str,
) -> pd.DataFrame:
    """Apply sidebar filters to the DataFrame.

    Each filter is only applied when the user has made an explicit selection:
    - ``language`` and ``pr_type``: inclusion filters via ``isin``.
    - ``period``: filters by a time window relative to the dataset's latest date.

    Args:
        df: Normalized DataFrame.
        language: Selected languages (empty list = no filter).
        pr_type: Selected PR types (empty list = no filter).
        period: Selected period — ``"All"``, ``"Last 7 days"`` or ``"Last month"``.

    Returns:
        Filtered DataFrame according to the provided parameters.
    """
    if language and "language" in df.columns:
        df = df[df["language"].isin(language)]

    if pr_type and "pr_type" in df.columns:
        df = df[df["pr_type"].isin(pr_type)]

    if period != "All" and "date" in df.columns:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
        reference_date = df["date"].max()

        if pd.notna(reference_date):
            if period == "Last 7 days":
                df = df[df["date"] >= reference_date - pd.Timedelta(days=7)]
            elif period == "Last month":
                df = df[df["date"] >= reference_date - pd.Timedelta(days=30)]

    return df