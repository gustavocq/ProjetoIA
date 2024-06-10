from pydantic import BaseModel, Field

class Perguntas(BaseModel):
    escolaridade: int = Field(..., ge=1, le=5, description="Nível de escolaridade (1-5)")
    experienciaRelevante: bool
    horasDeTreinamento: int = Field(..., ge=0, description="Número de horas de treinamento")
    matriculadoFaculdade: int = Field(..., ge=0, le=2, description="Status de matrícula")
    tempoNoUltimoEmprego: int = Field(..., ge=0, description="Tempo no último emprego em meses")
