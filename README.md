# Projeto IA

Este projeto implementa uma inteligência artificial para auxiliar o setor de RH na contratação de novos funcionários na área de tecnologia. A IA baseia-se em um banco de dados de candidatos e oferece funcionalidades para selecionar e baixar relatórios dos candidatos mais compatíveis.

## Endpoints

### `POST /selecaoCandidatos`

Retorna um JSON com os candidatos selecionados com base nos parâmetros fornecidos.

**Exemplo de Request:**
```json
{
    "escolaridade": 3,
    "experienciaRelevante": true,
    "horasDeTreinamento": 100,
    "matriculadoFaculdade": 1,
    "tempoNoUltimoEmprego": 12
}
```

**Exemplo de Response:**
```json
[
    {
        "id": 1,
        "cidade_id": 10,
        "genero": "Masculino",
        "experienciaRelevante": true,
        "matriculadoFaculdade": "Curso Meio Periodo",
        "escolaridade": "Ensino Superior Completo",
        "tempoDeExperiencia": 36,
        "tempoNoUltimoEmprego": 12,
        "horasDeTreinamento": 150,
        "ultimoSalario": 5000.00,
        "percentualCompatibilidade": 85.50
    }
]
```

### `POST /baixarSelecaoCandidatos`

Gera um arquivo Excel com os candidatos selecionados.

**Exemplo de Request:**
```json
{
    "escolaridade": 3,
    "experienciaRelevante": true,
    "horasDeTreinamento": 100,
    "matriculadoFaculdade": 1,
    "tempoNoUltimoEmprego": 12
}
```

**Response:** Retorna um arquivo Excel para download.

## Estrutura do Projeto

- **ClasseDeDados.py**: Define a estrutura dos dados dos candidatos.
- **Controller.py**: Contém os endpoints da API e a lógica para filtrar e selecionar candidatos.
- **MetodosUteis.py**: Funções auxiliares para carregar dados, preencher classes e treinar a IA.
- **PerguntasDTO.py**: Define a estrutura das perguntas utilizadas para filtrar candidatos.
- **Codigos.json**: Arquivo JSON contendo os códigos e descrições para gênero, matrícula em faculdade e escolaridade.

## Instruções para Execução

1. Clone o repositório:
    ```bash
    git clone <URL do repositório>
    cd <diretório do projeto>
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate  # Para Windows
    ```

3. Instale as dependências:
    ```bash
    pip install fastapi uvicorn pandas scikit-learn
    ```

4. Execute o servidor:
    ```bash
    uvicorn Controller:app --reload
    ```

5. Acesse a documentação interativa:
    - Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
    - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Estrutura dos Dados

### ClasseDeDados

```python
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
```

### Perguntas

```python
class Perguntas(BaseModel):
    escolaridade: int
    experienciaRelevante: bool
    horasDeTreinamento: int
    matriculadoFaculdade: int
    tempoNoUltimoEmprego: int
```

## Observações

- Certifique-se de que o arquivo `Banco/db_ia.xlsx` e `Banco/codigos.json` estejam corretamente posicionados na estrutura de pastas.
- Ajuste as configurações de CORS conforme necessário na seção de configuração do middleware CORS no `Controller.py`.

## Autor

- **Nome do Autor**: Gustavo Queiroz
- **Contato**: [Seu Email]
```