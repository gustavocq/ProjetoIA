import pandas as pd
from ClasseDeDados import ClasseDeDados
import json
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import NotFittedError

class MetodosUteis:

    @staticmethod
    def carregarDados(arquivo_xlsx):    
        """Carrega dados do arquivo Excel."""
        try:
            df = pd.read_excel(arquivo_xlsx)
            df['ultimoSalario'] = df['ultimoSalario'].astype(float)  # Certifique-se de que o salário é float
            return df
        except Exception as e:
            raise FileNotFoundError(f"Erro ao carregar dados do arquivo {arquivo_xlsx}: {e}")

    @staticmethod
    def preencherClasse(df):
        """Preenche a classe de dados com as informações dos candidatos e calcula a compatibilidade."""
        try:
            lista = []

            with open('Banco/codigos.json', 'r') as f:
                dados = json.load(f)

            codigoGenero = {item['codigo']: item['descricao'] for item in dados['genero']}
            codigoMatriculado = {item['codigo']: item['descricao'] for item in dados['matriculadoFaculdade']}
            codigoEscolaridade = {item['codigo']: item['descricao'] for item in dados['escolaridade']}

            colunasDesejadas = ['escolaridade', 'experienciaRelevante', 'horasDeTreinamento', 'matriculadoFaculdade', 'tempoNoUltimoEmprego']
            dfColunasComPeso = MetodosUteis.separarColunas(df, colunasDesejadas)
            modelo = MetodosUteis.treinarIA(dfColunasComPeso)

            for row in df.itertuples(index=False):
                dfProbabilidade = [getattr(row, col) for col in colunasDesejadas]
                probabilidade = modelo.predict_proba([dfProbabilidade])[0][1] * 100

                lista.append(ClasseDeDados(
                    id=row[0],
                    cidade_id=row[1],
                    genero=codigoGenero.get(row[2], 'Nao Informado'),
                    experienciaRelevante=row[3],
                    matriculadoFaculdade=codigoMatriculado.get(row[4], 'Nao matriculado'),
                    escolaridade=codigoEscolaridade.get(row[5], 'Escola Fundamental Completo'),
                    tempoDeExperiencia=row[6],
                    tempoNoUltimoEmprego=row[7],
                    horasDeTreinamento=row[8],
                    ultimoSalario=float(row[10]),  # Certifique-se de que o salário é float
                    percentualCompatibilidade=round(probabilidade, 2)
                ))

            return lista
        except NotFittedError:
            raise RuntimeError("O modelo de IA não foi treinado corretamente.")
        except Exception as e:
            raise RuntimeError(f"Erro ao preencher dados: {e}")

    @staticmethod
    def treinarIA(dataFrame):
        """Treina o modelo de IA com os dados fornecidos."""
        try:
            target = (dataFrame['escolaridade'] >= 5).astype(int)
            modelo = LogisticRegression()
            modelo.fit(dataFrame, target)
            return modelo
        except Exception as e:
            raise RuntimeError(f"Erro ao treinar IA: {e}")

    @staticmethod
    def separarColunas(dataFrame, colunas_desejadas):
        """Separa as colunas desejadas do DataFrame."""
        try:
            return dataFrame[colunas_desejadas]
        except KeyError as e:
            raise ValueError(f"Coluna não encontrada: {e}")
