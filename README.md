# Pipeline de Dados IoT

Projeto para processamento, armazenamento e visualização de dados de temperatura usando:
- Python
- PostgreSQL (Docker)
- Streamlit

## Como rodar

1. Subir o banco:
```bash
docker compose up -d
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Rodar ingestão:
```bash
python src/load_data.py
```

4. Rodar dashboard:
```bash
streamlit run src/dashboard.py
```
