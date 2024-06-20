from pydantic import BaseModel, Field

# Define a classe Perguntas para validar as entradas do usuário
class Perguntas(BaseModel):
    escolaridade: int = Field(..., ge=1, le=5, description="Nível de escolaridade (1-5)")
    experienciaRelevante: bool  # Se o candidato tem experiência relevante
    horasDeTreinamento: int = Field(..., ge=0, description="Número de horas de treinamento")
    matriculadoFaculdade: int = Field(..., ge=0, le=2, description="Status de matrícula")
    tempoNoUltimoEmprego: int = Field(..., ge=0, description="Tempo no último emprego em meses")
