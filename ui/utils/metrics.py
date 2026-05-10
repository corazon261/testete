"""Metric computation functions for the PR Insights dashboard."""

import pandas as pd


def compute_metrics(df: pd.DataFrame) -> dict[str, float]:
    """Calculate summary metrics displayed in the dashboard cards.

    Args:
        df: Filtered and normalized DataFrame.

    Returns:
        Dictionary with the following keys:

        - ``total`` (int): total number of PRs in the filtered dataset.
        - ``bugfix_pct`` (float): percentage of PRs of type ``Bugfix``.
        - ``feature_pct`` (float): percentage of PRs of type ``Feature``.
        - ``clarity`` (float): mean value of the ``clarity_score`` column.
    """
    total: int = len(df)

    if total == 0:
        return {"total": 0, "bugfix_pct": 0.0, "feature_pct": 0.0, "clarity": 0.0}

    bugfix_count: int = (
        len(df[df["pr_type"] == "Bugfix"]) if "pr_type" in df.columns else 0
    )
    feature_count: int = (
        len(df[df["pr_type"] == "Feature"]) if "pr_type" in df.columns else 0
    )
    clarity_mean: float = (
        float(df["clarity_score"].mean()) if "clarity_score" in df.columns else 0.0
    )

    return {
        "total": total,
        "bugfix_pct": (bugfix_count / total) * 100,
        "feature_pct": (feature_count / total) * 100,
        "clarity": clarity_mean,
    }