from sentence_transformers import SentenceTransformer
import torch
import faiss
from tqdm import tqdm
import pandas as pd

ratings = pd.read_csv("ratings_reduzido.csv")

model_name = "sentence-transformers/distiluse-base-multilingual-cased-v2"

device = "cuda" if torch.cuda.is_available() else "cpu"

model = SentenceTransformer(model_name, device=device)

texts = ratings["text"].astype(str).tolist()

embedding_dim = model.get_sentence_embedding_dimension()

index = faiss.IndexFlatIP(embedding_dim)

batch_size = 32

for start in tqdm(range(0, len(texts), batch_size)):

    end = min(start + batch_size, len(texts))
    batch_texts = texts[start:end]

    embeddings = model.encode(
        batch_texts,
        batch_size=batch_size,
        show_progress_bar=False,
        normalize_embeddings=True,
        device=device
    )

    embeddings = embeddings.astype("float32")

    index.add(embeddings)

faiss.write_index(index, "opiniao_index_final.faiss")