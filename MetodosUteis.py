import pandas as pd
from ClasseDeDados import ClasseDeDados

class MetodosUteis:
    # Função para carregar dados do arquivo Excel
    def carregarDados(arquivo_xlsx):    
        df = pd.read_excel(arquivo_xlsx)  
        return df

    def preencherClasse(df):
        
        cont = 0 #Index para desconsiderar cabeçalho
        list = []

        # Converter cada linha do DataFrame em uma instância de Perguntas
        for row in df.iterrows():      

            cont =+ 1
            list.append(ClasseDeDados(
                id=row[cont]['id'],
                cidade_id=row[cont]['cidade_id'],
                genero=row[cont]['genero'],
                experienciaRelevante=row[cont]['experienciaRelevante'],
                matriculadoFaculdade=row[cont]['matriculadoFaculdade'],
                escolaridade=row[cont]['escolaridade'],
                tempoDeExperiencia=row[cont]['tempoDeExperiencia'],
                tempoNoUltimoEmprego=row[cont]['tempoNoUltimoEmprego'],
                horasDeTreinamento=row[cont]['horasDeTreinamento'],
                ultimoSalario=row[cont]['ultimoSalario']
            ))      
        
        return list
    