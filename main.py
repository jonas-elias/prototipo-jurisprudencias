from qdrant_client import QdrantClient
import numpy as np
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware

qdrant_client = QdrantClient(
    url="https://ca13b100-6830-4a4f-a1c7-b363a3053ffb.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="nrS_ycptYQRrzG-PFPD5yNocfx97R4HOb9qA3P9Ku-e4sIjVT_trQQ",
)

model = SentenceTransformer('neuralmind/bert-large-portuguese-cased')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/buscar_jurisprudencias/")
async def buscar_jurisprudencias(texto: str) -> List[dict]:
    resultados = []
    vector = model.encode(texto).tolist()

    search_result = qdrant_client.search(
        collection_name='jurisprudencias',
        query_vector=vector,
        query_filter=None,
        limit=10
    )

    jurisprudencias = [hit.payload for hit in search_result]
    for jurisprudencia in jurisprudencias:
        if jurisprudencia["texto"] != '':
            resultados.append(jurisprudencia)
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhuma jurisprudência encontrada.")
    return resultados
