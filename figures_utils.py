import pandas as pd
import plotly.graph_objects as go


def _prepare_time_series(df: pd.DataFrame):
    """
    Recebe um DataFrame com colunas 'tempo_ajustado' (string yyyy-mm-dd)
    e 'score', e devolve ts_step, counts_cum, cum_mean, full_idx.
    """
    df = df.copy()

    df["tempo_ajustado"] = pd.to_datetime(df["tempo_ajustado"], format="%Y-%m-%d")

    ts = (
        df.groupby("tempo_ajustado")["score"]
        .mean()
        .sort_index()
    )

    daily_counts = (
        df.groupby("tempo_ajustado")["score"]
        .count()
        .sort_index()
    )

    daily_sum = (
        df.groupby("tempo_ajustado")["score"]
        .sum()
        .sort_index()
    )

    end_date = pd.Timestamp("2015-01-01")
    start_date = ts.index.min()

    for idx in [ts.index, daily_counts.index, daily_sum.index]:
        if end_date < idx.max():
            end_date = idx.max()

    full_idx = pd.date_range(start=start_date, end=end_date, freq="D")

    ts_step = ts.reindex(full_idx, method="ffill")

    counts_full = daily_counts.reindex(full_idx, fill_value=0)
    sum_full = daily_sum.reindex(full_idx, fill_value=0)

    counts_cum = counts_full.cumsum()
    sum_cum = sum_full.cumsum()

    cum_mean = sum_cum / counts_cum

    return ts_step, counts_cum, cum_mean, full_idx


def build_time_series_figures(df: pd.DataFrame, label: str):
    """
    A partir de um subconjunto de ratings (colunas 'tempo_ajustado' e 'score'),
    cria os três gráficos: score médio diário, contagem acumulada e média acumulada.
    """
    ts_step, counts_cum, cum_mean, full_idx = _prepare_time_series(df)

    fig_score = go.Figure()
    fig_score.add_trace(
        go.Scatter(
            x=ts_step.index,
            y=ts_step.values,
            mode="lines",
            line_shape="hv",
            name="Score médio diário",
        )
    )
    fig_score.update_layout(
        title=f"Evolução do score (média diária) – {label}",
        xaxis_title="Data",
        yaxis_title="Score médio diário",
        yaxis=dict(range=[0, 6]),
        margin=dict(l=40, r=10, t=40, b=40),
    )

    fig_count = go.Figure()
    fig_count.add_trace(
        go.Scatter(
            x=counts_cum.index,
            y=counts_cum.values,
            mode="lines",
            name="Avaliações acumuladas",
        )
    )
    fig_count.update_layout(
        title=f"Avaliações acumuladas – {label}",
        xaxis_title="Data",
        yaxis_title="Quantidade acumulada de avaliações",
        margin=dict(l=40, r=10, t=40, b=40),
    )

    fig_cummean = go.Figure()
    fig_cummean.add_trace(
        go.Scatter(
            x=cum_mean.index,
            y=cum_mean.values,
            mode="lines",
            name="Score médio acumulado",
        )
    )
    fig_cummean.update_layout(
        title=f"Score médio acumulado – {label}",
        xaxis_title="Data",
        yaxis_title="Score médio acumulado",
        yaxis=dict(range=[0, 6]),
        margin=dict(l=40, r=10, t=40, b=40),
    )

    return fig_score, fig_count, fig_cummean


def build_empty_figures(label: str):
    """Figuras vazias quando não há dados para autor/categoria."""
    fig1 = go.Figure()
    fig1.update_layout(
        title=f"Nenhum score encontrado para {label}",
        xaxis_title="Data",
        yaxis_title="Score",
        yaxis=dict(range=[0, 6]),
        margin=dict(l=40, r=10, t=40, b=40),
    )

    fig2 = go.Figure()
    fig2.update_layout(
        title=f"Nenhuma avaliação encontrada para {label}",
        xaxis_title="Data",
        yaxis_title="Avaliações acumuladas",
        margin=dict(l=40, r=10, t=40, b=40),
    )

    fig3 = go.Figure()
    fig3.update_layout(
        title=f"Score médio acumulado – {label}",
        xaxis_title="Data",
        yaxis_title="Score médio acumulado",
        yaxis=dict(range=[0, 6]),
        margin=dict(l=40, r=10, t=40, b=40),
    )

    return fig1, fig2, fig3
