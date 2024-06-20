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

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Configuração de CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Caminho para o banco de dados em Excel
db_ia = 'Banco/db_ia.xlsx'

# Carregar dados do banco ao iniciar o programa
dataFrame = MetodosUteis.carregarDados(db_ia)

@app.post('/selecaoCandidatos', response_model=List[ClasseDeDados])
def selecaoCandidatos(weights: Perguntas):
    """
    Filtra e seleciona os candidatos com base nos parâmetros fornecidos.
    """
    try:
        # Filtra os dados do DataFrame com base nos critérios fornecidos
        dataFrameFiltrado = dataFrame[
            (dataFrame['escolaridade'] >= weights.escolaridade) &
            (dataFrame['experienciaRelevante'] == weights.experienciaRelevante) &
            (dataFrame['horasDeTreinamento'] >= weights.horasDeTreinamento) &
            (dataFrame['matriculadoFaculdade'] >= weights.matriculadoFaculdade) &
            (dataFrame['tempoNoUltimoEmprego'] >= weights.tempoNoUltimoEmprego)
        ]

        # Preenche a lista de candidatos com base no DataFrame filtrado
        listaCandidatos = MetodosUteis.preencherClasse(dataFrameFiltrado)
        # Ordena a lista de candidatos com base no percentual de compatibilidade
        listaCandidatos = sorted(listaCandidatos, key=lambda x: x.percentualCompatibilidade, reverse=True)
        # Retorna apenas os 10 melhores candidatos
        listaCandidatos = listaCandidatos[:10]

        return listaCandidatos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/baixarSelecaoCandidatos')
def baixarSelecaoCandidatos(weights: Perguntas):
    """
    Gera um relatório Excel dos candidatos selecionados com base nos parâmetros fornecidos.
    """
    try:
        # Seleciona os candidatos com base nos parâmetros fornecidos
        dadosSelecao = selecaoCandidatos(weights)
        # Nome do arquivo de relatório
        nomeRelatorio = f"Download/Relacao_Candidatos_{date.today().strftime('%d.%m.%Y')}.xlsx"

        if not os.path.exists(nomeRelatorio):
            # Converte os dados selecionados para um dicionário
            dados_dict = [obj.dict() for obj in dadosSelecao]
            # Cria um DataFrame com os dados
            df = pd.DataFrame(dados_dict)
            # Salva o DataFrame em um arquivo Excel
            df.to_excel(nomeRelatorio, index=False)

        # Retorna o arquivo Excel gerado como resposta
        return FileResponse(nomeRelatorio, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=nomeRelatorio)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    # Executa o aplicativo FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)
