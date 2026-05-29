# Previsão de AVC com Pipeline de Machine Learning

Este projeto desenvolve um pipeline completo de Machine Learning para previsão de ocorrência de AVC (*stroke*) a partir de um dataset público do Kaggle.

O projeto contempla análise exploratória de dados, pré-processamento com `Pipeline` e `ColumnTransformer`, comparação de modelos, rastreamento de experimentos com MLflow, versionamento de dados com DVC, API com FastAPI e execução via Docker Compose.

## Dataset

Dataset utilizado: Stroke Prediction Dataset  
Fonte: Kaggle — `fedesoriano/stroke-prediction-dataset`

A variável-alvo é `stroke`, que indica:

- `0`: paciente sem AVC
- `1`: paciente com AVC

## Estrutura do projeto

```text
Desafio01/
├── data/
│   ├── raw/
│   │   └── healthcare-dataset-stroke-data.csv.dvc
│   └── processed/
│       └── stroke_limpo.csv.dvc
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_modelagem.ipynb
├── screenshots/
├── src/
│   └── api.py
├── mlruns/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Principais etapas

1. Análise exploratória dos dados.
2. Limpeza estrutural:
   - remoção da coluna `id`;
   - remoção do único registro com `gender = Other`;
   - manutenção de `bmi` ausente para tratamento no pipeline.
3. Separação treino/teste com estratificação.
4. Pré-processamento com `Pipeline` e `ColumnTransformer`.
5. Comparação de três modelos:
   - Regressão Logística;
   - Random Forest;
   - Gradient Boosting.
6. Registro dos experimentos no MLflow.
7. Registro do melhor modelo no MLflow Model Registry.
8. Criação de API com FastAPI.
9. Containerização com Docker Compose.
10. Versionamento de dados com DVC.

## Melhor modelo

O melhor modelo foi a Regressão Logística com ajuste de hiperparâmetros.

Resultados no conjunto de teste:

| Métrica | Valor |
|---|---:|
| F1-macro | 0.5366 |
| Recall da classe AVC | 0.8000 |
| ROC-AUC | 0.8395 |

O modelo identificou 40 dos 50 casos reais de AVC no conjunto de teste, mas apresentou muitos falsos positivos. Portanto, deve ser interpretado apenas como apoio inicial de triagem, não como diagnóstico médico.

## Como executar localmente

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a API:

```bash
uvicorn src.api:app --reload
```

Acesse:

```text
http://127.0.0.1:8000/saude
http://127.0.0.1:8000/docs
```

## Como executar com Docker Compose

Suba os serviços:

```bash
docker compose up
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

O MLflow UI ficará disponível em:

```text
http://127.0.0.1:5000
```

## Endpoints da API

### GET `/saude`

Verifica se a API está funcionando e se o modelo foi carregado.

Exemplo de resposta:

```json
{
  "ok": true,
  "modelo": "models:/previsor_avc_stroke@production"
}
```

### POST `/predict`

Realiza a predição para um paciente.

Exemplo de entrada:

```json
{
  "gender": "Female",
  "age": 67.0,
  "hypertension": 0,
  "heart_disease": 1,
  "ever_married": "Yes",
  "work_type": "Private",
  "Residence_type": "Urban",
  "avg_glucose_level": 228.69,
  "bmi": 36.6,
  "smoking_status": "formerly smoked"
}
```

Exemplo de resposta:

```json
{
  "prediction": 1,
  "label": "Com AVC",
  "modelo": "models:/previsor_avc_stroke@production"
}
```

## DVC

Os arquivos CSV são versionados com DVC.

Para verificar o status:

```bash
dvc status
```

Para recuperar os dados a partir do remote configurado:

```bash
dvc pull
```

Remote configurado:

```text
localremote
```

## MLflow

Os experimentos foram registrados em `mlruns/`.

O modelo final foi registrado no Model Registry com o nome:

```text
previsor_avc_stroke
```

Alias de produção:

```text
production
```

URI usada pela API:

```text
models:/previsor_avc_stroke@production
```

## Evidências

A pasta `screenshots/` contém evidências da execução do projeto, incluindo:

- matrizes de confusão dos modelos;
- teste do endpoint `/saude`;
- teste do endpoint `/predict`;
- execução da API via Docker.

## Observações

Este projeto tem finalidade acadêmica. O modelo não deve ser usado como ferramenta de diagnóstico médico.
