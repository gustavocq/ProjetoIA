import pandas as pd
import os
from fastapi import FastAPI
from typing import List
from PerguntasDTO import Perguntas
from ClasseDeDados import ClasseDeDados
from MetodosUteis import MetodosUteis
from datetime import date
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos os domínios. Modifique para uma lista específica se necessário.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

db_ia = 'Banco/db_ia.xlsx'  # Banco de dados
# Carregar banco ao iniciar o programa
dataFrame = MetodosUteis.carregarDados(db_ia)

@app.post('/selecaoCandidatos', response_model=List[ClasseDeDados])
def selecaoCandidatos(weights: Perguntas):
    # Filtrar dados com base nas perguntas
    dataFrameFiltrado = dataFrame[
        (dataFrame['escolaridade']         >= weights.escolaridade)         &
        (dataFrame['experienciaRelevante'] == weights.experienciaRelevante) &
        (dataFrame['horasDeTreinamento']   >= weights.horasDeTreinamento)   &
        (dataFrame['matriculadoFaculdade'] >= weights.matriculadoFaculdade) &
        (dataFrame['tempoNoUltimoEmprego'] >= weights.tempoNoUltimoEmprego)
    ]  

    listaCandidatos = MetodosUteis.preencherClasse(dataFrameFiltrado)
    listaCandidatos = sorted(listaCandidatos, key=lambda x: x.percentualCompatibilidade, reverse=True)
    listaCandidatos = listaCandidatos[:10]

    return listaCandidatos

@app.post('/baixarSelecaoCandidatos', response_model=List[ClasseDeDados])
def baixarSelecaoCandidatos(weights: Perguntas):
    # Fazer uma chamada para o endpoint selecaoCandidatos
    dadosSelecao = selecaoCandidatos(weights)
    nomeRelatorio = f"Download/Relacao_Candidatos_{date.today().strftime('%d.%m.%Y')}.xlsx"

    # Verifica se o arquivo Excel já existe
    if not os.path.exists(nomeRelatorio):
        dados_dict = [obj.dict() for obj in dadosSelecao]   
        df = pd.DataFrame(dados_dict)
        df.to_excel(nomeRelatorio, index=False)

    # Retorna o arquivo Excel como uma resposta de download
    return FileResponse(nomeRelatorio, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=nomeRelatorio)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
