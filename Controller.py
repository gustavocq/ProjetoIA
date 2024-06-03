import pandas as pd
from fastapi import FastAPI
from typing import List, Dict
from PerguntasDTO import Perguntas
from ClasseDeDados import ClasseDeDados
from MetodosUteis import MetodosUteis

app = FastAPI()

# db_ia = 'Banco\db_ia.xlsx'  # Certifique-se de que o arquivo tem extensão .xlsx
db_ia = 'Banco\db_ia.xlsx'

@app.post('/selecaoCandidatos', response_model=List[ClasseDeDados])
def selecao_candidatos(weights: Perguntas):
    # Carregar banco ao iniciar o programa
    data_frame = MetodosUteis.carregarDados(db_ia) 

    # Filtrar dados com base nas perguntas
    data_frame_filtrado = data_frame[
        (data_frame['escolaridade'] >= weights.escolaridade) &
        (data_frame['experienciaRelevante'] == weights.experienciaRelevante) &
        (data_frame['horasDeTreinamento'] >= weights.horasDeTreinamento) &
        (data_frame['matriculadoFaculdade'] >= weights.matriculadoFaculdade) &
        (data_frame['tempoNoUltimoEmprego'] >= weights.tempoNoUltimoEmprego)
    ]
    
    # Preencher classe de dados com os dados filtrados
    lista_candidatos = MetodosUteis.preencherClasse(data_frame_filtrado)   
    
    return lista_candidatos

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
