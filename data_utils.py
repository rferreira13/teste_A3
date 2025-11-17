import ast
import pandas as pd


def load_books_and_lists(books_path: str):
    """Carrega books_data e extrai listas de autores e categorias."""
    books_data = pd.read_csv(books_path)

    authors_set = {
        author
        for author_list in books_data["authors"].tolist()
        if isinstance(author_list, str)
        for author in ast.literal_eval(author_list)
    }
    authors_list = sorted(list(authors_set))

    categories_set = {
        cat
        for cat_list in books_data["categories"].tolist()
        if isinstance(cat_list, str)
        for cat in ast.literal_eval(cat_list)
    }
    categories_list = sorted(list(categories_set))

    return books_data, authors_list, categories_list


def load_ratings(ratings_path: str):
    """Carrega ratings já reduzido."""
    ratings = pd.read_csv(ratings_path)
    return ratings
