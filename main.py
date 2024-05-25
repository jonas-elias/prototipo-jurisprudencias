from qdrant_client import QdrantClient
import numpy as np
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, HTTPException, Request
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random
import uuid
from fastapi.responses import JSONResponse
import json
from openai import OpenAI

client = OpenAI(
    api_key="",
)

qdrant_client = QdrantClient(
    url="https://65899fc3-6f4d-4fed-9a62-02e307b35f13.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="",
)

model = SentenceTransformer('juridics/bertlaw-base-portuguese-sts-scale')
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
    id_aleatorio = str(uuid.uuid1())
    id_aleatorio = id_aleatorio[:5]

    for jurisprudencia in jurisprudencias:
        if jurisprudencia["texto"] != '':
            resultados.append(jurisprudencia)
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhuma jurisprudência encontrada.")
    with open(f"./busca-jurisprudencias/database/{id_aleatorio}_aplicacao.json", "w", encoding="utf-8") as file:
        resultados_json = json.dumps(resultados)
        file.write(resultados_json)

    random.shuffle(resultados)
    return JSONResponse(resultados, 200, {'id': id_aleatorio, 'Access-Control-Expose-Headers': '*'})


@app.post("/salvar_jurisprudencias")
async def salvar_jurisprudencias(request: Request):
    body = await request.json()
    jurisprudencias_html = body.get('html', '')
    file_name = body.get('id', '')
    if jurisprudencias_html:
        with open(f"./busca-jurisprudencias/database/{file_name}_advogado.html", "w", encoding="utf-8") as file:
            file.write(jurisprudencias_html)


@app.post("/gerar_defesa/")
async def gerar_defesa(request: Request):
    body = await request.json()
    prompt = body.get('prompt', '')

    try:
        result = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente legal que sempre elabora defesas com base em jurisprudências."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )

        if len(result.choices) == 0:
            raise HTTPException(status_code=404, detail="Nenhuma defesa foi gerada.")

        response_text = result.choices[0].message.content
        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)