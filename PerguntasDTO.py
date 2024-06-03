from pydantic import BaseModel

class Perguntas(BaseModel):
    escolaridade            : int
    experienciaRelevante    : bool
    horasDeTreinamento      : int
    matriculadoFaculdade    : int
    tempoNoUltimoEmprego    : int