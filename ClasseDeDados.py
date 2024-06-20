from pydantic import BaseModel

# Define a classe de dados que representa um candidato
class ClasseDeDados(BaseModel):
    id: int  # ID do candidato
    cidade_id: int  # ID da cidade do candidato
    genero: str  # Gênero do candidato
    experienciaRelevante: bool  # Se o candidato tem experiência relevante
    matriculadoFaculdade: str  # Status de matrícula do candidato na faculdade
    escolaridade: str  # Nível de escolaridade do candidato
    tempoDeExperiencia: int  # Tempo de experiência do candidato em meses
    tempoNoUltimoEmprego: int  # Tempo no último emprego em meses
    horasDeTreinamento: int  # Número de horas de treinamento que o candidato completou
    ultimoSalario: float  # Último salário do candidato
    percentualCompatibilidade: float  # Percentual de compatibilidade calculado para o candidato
