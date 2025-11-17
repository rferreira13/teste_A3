import pandas as pd
import datetime
import ast


ratings = pd.read_csv("Books_rating.csv")

ratings = ratings.drop_duplicates(keep='first')

ratings["tempo_ajustado"] = ratings["time"].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d"))

ratings = ratings[ratings["tempo_ajustado"]>="1998-01-01"].reset_index(drop=True)

ratings = ratings[~ratings["Title"].isna()].reset_index(drop=True)

ratings_reduzido = ratings.sample(n=250_000, random_state=42)

ratings_reduzido.to_csv("ratings_reduzido.csv")

books_data = pd.read_csv("books_data.csv")
books_data["authors"] = books_data["authors"].apply(lambda x:ast.literal_eval(x) if isinstance(x, str) else x)
books_data["authors"] = books_data["authors"].apply(lambda x: [y.strip() for y in x] if isinstance(x, list) else x)
books_data["authors"] = books_data["authors"].apply(lambda x: [
    y[
        y.index(([w for w in y if w.isalpha()][0]))
        :y.rindex(([w for w in y if w.isalpha()][-1]))] for y in x if len([w for w in y if w.isalpha()])>0] if isinstance(x, list) else x
    )


books_data["categories"] = books_data["categories"].apply(lambda x:ast.literal_eval(x) if isinstance(x, str) else x)
books_data["categories"] = books_data["categories"].apply(lambda x: [y.strip() for y in x] if isinstance(x, list) else x)
books_data["categories"] = books_data["categories"].apply(lambda x: [
    y[
        y.index(([w for w in y if w.isalpha()][0]))
        :y.rindex(([w for w in y if w.isalpha()][-1]))] for y in x if len([w for w in y if w.isalpha()])>0] if isinstance(x, list) else x
    )


books_data_reduzido = books_data[books_data["Title"].isin(ratings_reduzido["Title"].tolist())]

books_data_reduzido.to_csv("books_data_reduzido.csv")