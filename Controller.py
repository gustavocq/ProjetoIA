import pandas as pd
import os
from fastapi import FastAPI, HTTPException
from typing import List
from PerguntasDTO import Perguntas
from ClasseDeDados import ClasseDeDados
from MetodosUteis import MetodosUteis
from datetime import date
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

app = FastAPI()

# Configuração de CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_ia = 'Banco/db_ia.xlsx'

# Carregar banco ao iniciar o programa
dataFrame = MetodosUteis.carregarDados(db_ia)

@app.post('/selecaoCandidatos', response_model=List[ClasseDeDados])
def selecaoCandidatos(weights: Perguntas):
    """Filtra e seleciona os candidatos com base nos parâmetros fornecidos."""
    try:
        dataFrameFiltrado = dataFrame[
            (dataFrame['escolaridade'] >= weights.escolaridade) &
            (dataFrame['experienciaRelevante'] == weights.experienciaRelevante) &
            (dataFrame['horasDeTreinamento'] >= weights.horasDeTreinamento) &
            (dataFrame['matriculadoFaculdade'] >= weights.matriculadoFaculdade) &
            (dataFrame['tempoNoUltimoEmprego'] >= weights.tempoNoUltimoEmprego)
        ]

        listaCandidatos = MetodosUteis.preencherClasse(dataFrameFiltrado)
        listaCandidatos = sorted(listaCandidatos, key=lambda x: x.percentualCompatibilidade, reverse=True)
        listaCandidatos = listaCandidatos[:10]

        return listaCandidatos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/baixarSelecaoCandidatos')
def baixarSelecaoCandidatos(weights: Perguntas):
    """Gera um relatório Excel dos candidatos selecionados com base nos parâmetros fornecidos."""
    try:
        dadosSelecao = selecaoCandidatos(weights)
        nomeRelatorio = f"Download/Relacao_Candidatos_{date.today().strftime('%d.%m.%Y')}.xlsx"

        if not os.path.exists(nomeRelatorio):
            dados_dict = [obj.dict() for obj in dadosSelecao]
            df = pd.DataFrame(dados_dict)
            df.to_excel(nomeRelatorio, index=False)

        return FileResponse(nomeRelatorio, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=nomeRelatorio)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
