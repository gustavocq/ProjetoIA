from pydantic import BaseModel

class ClasseDeDados(BaseModel):
    id: int
    cidade_id: int
    genero: str
    experienciaRelevante: bool
    matriculadoFaculdade: str
    escolaridade: str
    tempoDeExperiencia: int
    tempoNoUltimoEmprego: int
    horasDeTreinamento: int
    ultimoSalario: float
    percentualCompatibilidade: float
