import pandas as pd
from ClasseDeDados import ClasseDeDados
import json

class MetodosUteis:
    # Função para carregar dados do arquivo Excel
    def carregarDados(arquivo_xlsx):    
        df = pd.read_excel(arquivo_xlsx)  
        return df

    def preencherClasse(df):
        
        cont = 0 #Index para desconsiderar cabeçalho
        list = []

        # Carregar o JSON contendo os códigos e descrições
        with open('Banco/codigos.json', 'r') as f:
            dados = json.load(f)

        # Criar dicionários com codigos
        codigoGenero       = {item['codigo']: item['descricao'] for item in dados['genero']}
        codigoMatriculado  = {item['codigo']: item['descricao'] for item in dados['matriculadoFaculdade']}
        codigoEscolaridade = {item['codigo']: item['descricao'] for item in dados['escolaridade']}


        # Converter cada linha do DataFrame em uma instância de Perguntas
        for row in df.iterrows():      

            cont =+ 1
            list.append(ClasseDeDados(
                id = row[cont]['id'],
                cidade_id = row[cont]['cidade_id'],
                genero = codigoGenero.get(row[cont]['genero']),
                experienciaRelevante = row[cont]['experienciaRelevante'],
                matriculadoFaculdade = codigoMatriculado.get(row[cont]['matriculadoFaculdade'], ''),
                escolaridade = codigoEscolaridade.get(row[cont]['escolaridade'], ''),
                tempoDeExperiencia = row[cont]['tempoDeExperiencia'],
                tempoNoUltimoEmprego = row[cont]['tempoNoUltimoEmprego'],
                horasDeTreinamento = row[cont]['horasDeTreinamento'],
                ultimoSalario = row[cont]['ultimoSalario']
            ))      
        
        return list
    