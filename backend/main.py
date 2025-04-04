from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("Relatorio_cadop.csv", sep=';', encoding='latin1')
df.fillna('', inplace=True)

@app.get("/operadoras")
def listar_todas_operadoras():
    return {
        "quantidade_total": len(df),
        "operadoras": df.to_dict(orient="records")
    }

@app.get("/buscar")
def buscar_operadora(query: str = Query(..., min_length=1)):
    query_lower = query.lower()

    def relevancia(linha):
        texto = ' '.join(str(valor).lower() for valor in linha)
        return query_lower in texto

    resultados = df[df.apply(relevancia, axis=1)]

    return {
        "quantidade_resultados": len(resultados),
        "resultados": resultados.to_dict(orient="records")
    }

@app.get("/buscar-razao")
def buscar_razao_social(query: str = Query(..., min_length=1)):
    resultados = df[df["Razao_Social"].str.lower().str.contains(query.lower())]
    return {
        "quantidade_resultados": len(resultados),
        "resultados": resultados.to_dict(orient="records")
    }

@app.get("/buscar-cnpj")
def buscar_cnpj(query: str = Query(..., min_length=14, max_length=14)):
    if not query.isdigit():
        raise HTTPException(status_code=400, detail="O CNPJ deve conter apenas números (14 dígitos).")
    
    df["CNPJ"] = df["CNPJ"].astype(str).str.zfill(14)
    resultados = df[df["CNPJ"].str.contains(query)]

    return {
        "quantidade_resultados": len(resultados),
        "resultados": resultados.to_dict(orient="records")
    }


@app.get("/buscar-uf")
def buscar_uf(query: str = Query(..., min_length=2, max_length=2)):
    if not query.isalpha():
        raise HTTPException(status_code=400, detail="A UF deve conter exatamente 2 letras.")

    resultados = df[df["UF"].str.upper() == query.upper()]

    return {
        "quantidade_resultados": len(resultados),
        "resultados": resultados.to_dict(orient="records")
    }

@app.get("/buscar-registro-ans")
def buscar_registro_ans(query: str = Query(..., min_length=1)):
    resultados = df[df["Registro_ANS"].astype(str).str.contains(query)]
    return {"quantidade_resultados": len(resultados), "resultados": resultados.to_dict(orient="records")}

@app.get("/buscar-telefone")
def buscar_telefone(query: str = Query(..., min_length=1)):
    resultados = df[df["Telefone"].astype(str).str.contains(query)]
    return {"quantidade_resultados": len(resultados), "resultados": resultados.to_dict(orient="records")}

@app.get("/buscar-representante")
def buscar_representante(query: str = Query(..., min_length=1)):
    resultados = df[df["Representante"].str.lower().str.contains(query.lower())]
    return {"quantidade_resultados": len(resultados), "resultados": resultados.to_dict(orient="records")}

@app.get("/buscar-email")
def buscar_email(query: str = Query(..., min_length=1)):
    resultados = df[df["Endereco_eletronico"].str.lower().str.contains(query.lower())]
    return {"quantidade_resultados": len(resultados), "resultados": resultados.to_dict(orient="records")}