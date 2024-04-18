import json
import os.path
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

modelSBert = SentenceTransformer('neuralmind/bert-large-portuguese-cased')

qdrant_client = QdrantClient(
    url="https://ca13b100-6830-4a4f-a1c7-b363a3053ffb.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="nrS_ycptYQRrzG-PFPD5yNocfx97R4HOb9qA3P9Ku-e4sIjVT_trQQ",
)

vector = modelSBert.encode("carência médica na cobertura incluindo rol da ans").tolist()

search_result = qdrant_client.search(
    collection_name='jurisprudencias',
    query_vector=vector,
    query_filter=None,
    limit=10
)

score = [hit.score for hit in search_result]
payloads = [hit.payload for hit in search_result]