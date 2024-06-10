import pandas as pd
from ClasseDeDados import ClasseDeDados
import json
from sklearn.linear_model import LogisticRegression

class MetodosUteis:

    # Função para carregar dados do arquivo Excel
    def carregarDados(arquivo_xlsx):    
        df = pd.read_excel(arquivo_xlsx)  
        return df

    def preencherClasse(df):
        
        cont = 0 
        cont2 =0
        list = []

        # Carregar o JSON contendo os códigos e descrições
        with open('Banco/codigos.json', 'r') as f:
            dados = json.load(f)

        # Criar dicionários com codigos
        codigoGenero       = {item['codigo']: item['descricao'] for item in dados['genero']}
        codigoMatriculado  = {item['codigo']: item['descricao'] for item in dados['matriculadoFaculdade']}
        codigoEscolaridade = {item['codigo']: item['descricao'] for item in dados['escolaridade']}

        colunasDesejadas = ['escolaridade', 'experienciaRelevante', 'horasDeTreinamento', 'matriculadoFaculdade', 'tempoNoUltimoEmprego']    
        dfColunasComPeso = separarColunas(df,colunasDesejadas)    
        modelo = treinarIA(dfColunasComPeso)

        # Converter cada linha do DataFrame em uma instância de Perguntas
        for row in df.itertuples(index=False):  

            dfProbabilidade = [getattr(row, col) for col in colunasDesejadas]
            probabilidade = modelo.predict_proba([dfProbabilidade])[0][1] * 100

            listaDf = df.iloc[cont]
            listaDf = pd.DataFrame(listaDf)

            list.append(ClasseDeDados(
                id=row[0],
				cidade_id=row[1],
				genero=codigoGenero.get(row[2]),
				experienciaRelevante=row[3],
				matriculadoFaculdade=codigoMatriculado.get(row[4], ''),
				escolaridade=codigoEscolaridade.get(row[5], ''),
				tempoDeExperiencia=row[6],
				tempoNoUltimoEmprego=row[7],
				horasDeTreinamento=row[8],
				ultimoSalario=row[9],
				percentualCompatibilidade=round(probabilidade, 2)

            ))      
        
        return list
    
def treinarIA(dataFrame):
   
    target = (dataFrame['escolaridade'] >= 5).astype(int)  # Exemplo de critério, ajuste conforme necessário

    # Treinar o modelo
    modelo = LogisticRegression()
    modelo.fit(dataFrame, target)

    return modelo

def separarColunas(dataFrame, colunas_desejadas):
        return dataFrame[colunas_desejadas]
    