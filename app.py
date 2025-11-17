import ast
from dash import dcc, html, Input, Output, dash_table
import dash
from figures_utils import build_time_series_figures, build_empty_figures
from data_utils import load_books_and_lists, load_ratings
from semantic_utils import load_model_and_index, semantic_search

books_data, authors_list, categories_list = load_books_and_lists(
    "books_data_reduzido.csv"
)
ratings = load_ratings("ratings_reduzido.csv")

index, model = load_model_and_index(
    "opiniao_index_final.faiss",
    "sentence-transformers/distiluse-base-multilingual-cased-v2",
)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Tabs(
            id="main-tabs",
            value="tab-author",
            children=[
                dcc.Tab(
                    label="Autor",
                    value="tab-author",
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                id="author-dropdown",
                                options=[{"label": a, "value": a} for a in authors_list],
                                value=authors_list[0] if authors_list else None,
                                clearable=False,
                            ),
                            style={
                                "width": "40%",
                                "margin": "10px auto 20px auto",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="author-graph-score",
                                    style={"width": "33%", "height": "350px"},
                                    config={"displayModeBar": False},
                                ),
                                dcc.Graph(
                                    id="author-graph-count",
                                    style={"width": "33%", "height": "350px"},
                                    config={"displayModeBar": False},
                                ),
                                dcc.Graph(
                                    id="author-graph-cummean",
                                    style={"width": "33%", "height": "350px"},
                                    config={"displayModeBar": False},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "space-between",
                            },
                        ),
                    ],
                ),

                dcc.Tab(
                    label="Categoria",
                    value="tab-category",
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                id="category-dropdown",
                                options=[
                                    {"label": c, "value": c} for c in categories_list
                                ],
                                value=categories_list[0] if categories_list else None,
                                clearable=False,
                            ),
                            style={
                                "width": "40%",
                                "margin": "10px auto 20px auto",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="category-graph-score",
                                    style={"width": "33%", "height": "350px"},
                                    config={"displayModeBar": False},
                                ),
                                dcc.Graph(
                                    id="category-graph-count",
                                    style={"width": "33%", "height": "350px"},
                                    config={"displayModeBar": False},
                                ),
                                dcc.Graph(
                                    id="category-graph-cummean",
                                    style={"width": "33%", "height": "350px"},
                                    config={"displayModeBar": False},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "justifyContent": "space-between",
                            },
                        ),
                    ],
                ),

                dcc.Tab(
                    label="Busca Semântica",
                    value="tab-semantic",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label("Texto da busca:"),
                                        dcc.Textarea(
                                            id="semantic-query",
                                            style={
                                                "width": "100%",
                                                "height": "80px",
                                            },
                                            placeholder=(
                                                "Digite aqui sua busca "
                                                "(ex: Interesting novels)..."
                                            ),
                                        ),
                                    ],
                                    style={"width": "70%", "display": "inline-block"},
                                ),
                                html.Div(
                                    [
                                        html.Label("k (número de resultados):"),
                                        dcc.Slider(
                                            id="semantic-k",
                                            min=1,
                                            max=10,
                                            step=1,
                                            value=5,
                                            marks={i: str(i) for i in range(1, 11)},
                                        ),
                                    ],
                                    style={
                                        "width": "25%",
                                        "display": "inline-block",
                                        "verticalAlign": "top",
                                        "marginLeft": "20px",
                                    },
                                ),
                            ],
                            style={
                                "width": "90%",
                                "margin": "20px auto",
                            },
                        ),
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="semantic-table",
                                    page_size=10,
                                    style_table={
                                        "overflowX": "auto",
                                        "maxHeight": "400px",
                                        "overflowY": "auto",
                                    },
                                    style_cell={
                                        "fontSize": 12,
                                        "padding": "5px",
                                        "whiteSpace": "normal",
                                        "height": "auto",
                                    },
                                )
                            ],
                            style={"width": "95%", "margin": "0 auto 20px auto"},
                        ),
                    ],
                ),
            ],
        )
    ]
)

@app.callback(
    Output("author-graph-score", "figure"),
    Output("author-graph-count", "figure"),
    Output("author-graph-cummean", "figure"),
    Input("author-dropdown", "value"),
)
def atualizar_graficos_autor(selected_author):
    if not selected_author:
        return build_empty_figures(f"o autor: {selected_author}")

    titles = books_data[
        books_data["authors"].apply(
            lambda x: selected_author in ast.literal_eval(x)
            if isinstance(x, str)
            else False
        )
    ]["Title"]

    titles = titles[~titles.isna()].tolist()

    author_ratings = ratings[ratings["Title"].isin(titles)][
        ["tempo_ajustado", "score"]
    ].copy()

    if author_ratings.empty:
        return build_empty_figures(f"o autor: {selected_author}")

    return build_time_series_figures(author_ratings, selected_author)

@app.callback(
    Output("category-graph-score", "figure"),
    Output("category-graph-count", "figure"),
    Output("category-graph-cummean", "figure"),
    Input("category-dropdown", "value"),
)
def atualizar_graficos_categoria(selected_category):
    if not selected_category:
        return build_empty_figures(f"a categoria: {selected_category}")

    titles = books_data[
        books_data["categories"].apply(
            lambda x: selected_category in ast.literal_eval(x)
            if isinstance(x, str)
            else False
        )
    ]["Title"]

    titles = titles[~titles.isna()].tolist()

    cat_ratings = ratings[ratings["Title"].isin(titles)][
        ["tempo_ajustado", "score"]
    ].copy()

    if cat_ratings.empty:
        return build_empty_figures(f"a categoria: {selected_category}")

    return build_time_series_figures(cat_ratings, selected_category)

@app.callback(
    Output("semantic-table", "data"),
    Output("semantic-table", "columns"),
    Input("semantic-query", "value"),
    Input("semantic-k", "value"),
)
def atualizar_busca_semantica(query, k):
    if not query or query.strip() == "":
        return [], []

    df_result = semantic_search(query, k, index, model, ratings)
    if df_result.empty:
        return [], []

    data = df_result.to_dict("records")
    columns = [{"name": c, "id": c} for c in df_result.columns]

    return data, columns


if __name__ == "__main__":
    app.run(debug=True)
