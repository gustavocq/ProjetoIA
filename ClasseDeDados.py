from pydantic import BaseModel

class ClasseDeDados(BaseModel):
    id                   : int
    cidade_id            : int
    genero               : int
    experienciaRelevante : bool
    matriculadoFaculdade : int
    escolaridade         : int
    tempoDeExperiencia   : int
    tempoNoUltimoEmprego : int
    horasDeTreinamento   : int
    ultimoSalario        : float