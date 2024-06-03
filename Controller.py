import pandas as pd
import os.path
from fastapi import FastAPI
from typing import List, Dict
from PerguntasDTO import Perguntas
from ClasseDeDados import ClasseDeDados
from MetodosUteis import MetodosUteis
from datetime import date
from starlette.responses import FileResponse

app = FastAPI()

db_ia = 'Banco\db_ia.xlsx' #Banco de dados

@app.post('/selecaoCandidatos', response_model=List[ClasseDeDados])
def selecaoCandidatos(weights: Perguntas):
    # Carregar banco ao iniciar o programa
    dataFrame = MetodosUteis.carregarDados(db_ia) 

    # Filtrar dados com base nas perguntas
    dataFrameFiltrado = dataFrame[
        (dataFrame['escolaridade']         >= weights.escolaridade)         &
        (dataFrame['experienciaRelevante'] == weights.experienciaRelevante) &
        (dataFrame['horasDeTreinamento']   >= weights.horasDeTreinamento)   &
        (dataFrame['matriculadoFaculdade'] >= weights.matriculadoFaculdade) &
        (dataFrame['tempoNoUltimoEmprego'] >= weights.tempoNoUltimoEmprego)
    ] 

    # Preencher classe de dados com os dados filtrados
    listaCandidatos = MetodosUteis.preencherClasse(dataFrameFiltrado)

    return listaCandidatos

@app.post('/baixarSelecaoCandidatos', response_model=List[ClasseDeDados])
def baixarSelecaoCandidatos(weights: Perguntas):
    # Fazer uma chamada para o endpoint selecao_candidatos
    dadosSelecao = selecaoCandidatos(weights)
    # caminhoRelatorio = 
    nomeRelatorio = f"Download\Relacao Candidatos {date.today().strftime('%d.%m.%Y')}.xlsx"

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
