# Entrega do Projeto

Repositório: https://github.com/lguzs/ML---Predicao-de-AVC

## Itens implementados

- Análise exploratória de dados em notebook.
- Pré-processamento com Pipeline e ColumnTransformer.
- Comparação de três modelos de classificação.
- Validação cruzada estratificada.
- Registro de experimentos com MLflow.
- Registro do modelo final no MLflow Model Registry.
- API com FastAPI.
- Endpoints `/saude` e `/predict`.
- Dockerfile e Docker Compose.
- Versionamento dos dados com DVC.
- Evidências em screenshots.

## Modelo final

Modelo selecionado: Regressão Logística.

Métricas no conjunto de teste:

- F1-macro: 0.5366
- Recall da classe AVC: 0.8000
- ROC-AUC: 0.8395

## Interpretação do modelo

O modelo final identificou 40 dos 50 casos reais de AVC no conjunto de teste, alcançando recall de 0.80 para a classe positiva.

Apesar disso, a precisão da classe AVC foi baixa, indicando muitos falsos positivos. Por esse motivo, o modelo deve ser entendido apenas como apoio inicial de triagem, e não como ferramenta de diagnóstico médico.

## Como executar

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar API localmente:

```bash
uvicorn src.api:app --reload
```

Executar com Docker:

```bash
docker compose up
```

Acessos:

```text
API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs
MLflow UI: http://127.0.0.1:5000
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

Os arquivos CSV foram removidos do Git e versionados com DVC.

Comandos usados:

```bash
dvc add data/raw/healthcare-dataset-stroke-data.csv
dvc add data/processed/stroke_limpo.csv
dvc remote add -d localremote dvc_remote
dvc push
```

O remote DVC usado é local:

```text
localremote
```

Como o remote é local, a pasta `dvc_remote/` deve ser incluída caso a entrega seja feita por `.zip`.

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

- matrizes de confusão;
- execução do endpoint `/saude`;
- execução do endpoint `/predict`;
- execução da API via Docker;
- execução do MLflow UI.

## Observação

Este projeto tem finalidade acadêmica. O modelo não deve ser usado como ferramenta de diagnóstico médico.
