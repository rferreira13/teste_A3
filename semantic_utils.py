import faiss
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer


def load_model_and_index(index_path: str, model_name: str):
    index = faiss.read_index(index_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer(model_name, device=device)
    return index, model


def semantic_search(query: str, k: int, index, model, ratings: pd.DataFrame):
    """
    Faz busca semântica e retorna um DataFrame pronto para exibição:
    - sem colunas 'Unnamed: 0' e 'time'
    - 'tempo_ajustado' formatado como 'Data da resposta' em dd/mm/yyyy.
    """
    query = query.strip()
    if not query:
        return pd.DataFrame()

    query_emb = model.encode(
        query,
        normalize_embeddings=True,
        convert_to_numpy=True
    ).astype("float32")

    scores, idxs = index.search(query_emb.reshape(1, -1), int(k))
    idxs_list = idxs[0].tolist()

    df_result = ratings.iloc[idxs_list].copy()
    df_result = df_result.reset_index(drop=True)

    df_result["similaridade"] = scores[0]

    colunas_para_excluir = ["Unnamed: 0", "time"]
    for col in colunas_para_excluir:
        if col in df_result.columns:
            df_result = df_result.drop(columns=[col])

    if "tempo_ajustado" in df_result.columns:
        df_result["tempo_ajustado"] = pd.to_datetime(
            df_result["tempo_ajustado"], format="%Y-%m-%d"
        ).dt.strftime("%d/%m/%Y")
        df_result = df_result.rename(columns={"tempo_ajustado": "Data da resposta"})

        cols = ["Data da resposta"] + [
            c for c in df_result.columns if c != "Data da resposta"
        ]
        df_result = df_result[cols]

    return df_result
