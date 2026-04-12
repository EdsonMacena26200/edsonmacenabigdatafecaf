import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def get_engine():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL não encontrada no arquivo .env")
    return create_engine(database_url)


def prepare_dataframe(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Renomear colunas para nomes SQL-friendly
    df = df.rename(columns={
        "room_id/id": "room_id",
        "out/in": "location_type"
    })

    # Converter data e temperatura
    df["noted_date"] = pd.to_datetime(df["noted_date"], errors="coerce")
    df["temp"] = pd.to_numeric(df["temp"], errors="coerce")

    # Remover linhas inválidas
    df = df.dropna(subset=["noted_date", "temp"]).copy()

    # Criar colunas derivadas
    df["reading_date"] = df["noted_date"].dt.date
    df["reading_hour"] = df["noted_date"].dt.hour

    return df


def create_views(engine):
    views_sql = """
    CREATE OR REPLACE VIEW avg_temp_por_ambiente AS
    SELECT
        room_id,
        ROUND(AVG(temp)::numeric, 2) AS avg_temp
    FROM temperature_readings
    GROUP BY room_id;

    CREATE OR REPLACE VIEW leituras_por_hora AS
    SELECT
        reading_hour AS hora,
        COUNT(*) AS contagem
    FROM temperature_readings
    GROUP BY reading_hour
    ORDER BY reading_hour;

    CREATE OR REPLACE VIEW temp_max_min_por_dia AS
    SELECT
        reading_date AS data,
        MAX(temp) AS temp_max,
        MIN(temp) AS temp_min
    FROM temperature_readings
    GROUP BY reading_date
    ORDER BY reading_date;

    CREATE OR REPLACE VIEW media_temp_in_out AS
    SELECT
        location_type,
        ROUND(AVG(temp)::numeric, 2) AS avg_temp
    FROM temperature_readings
    GROUP BY location_type;
    """

    with engine.begin() as conn:
        for statement in views_sql.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))


def main():
    csv_path = Path("data/IOT-temp.csv")

    if not csv_path.exists():
        raise FileNotFoundError("Arquivo CSV não encontrado em data/IOT-temp.csv")

    engine = get_engine()
    df = prepare_dataframe(str(csv_path))

    df.to_sql("temperature_readings", engine, if_exists="replace", index=False)
    create_views(engine)

    print("Dados carregados com sucesso na tabela temperature_readings.")
    print(f"Total de registros inseridos: {len(df)}")
    print("Views criadas:")
    print("- avg_temp_por_ambiente")
    print("- leituras_por_hora")
    print("- temp_max_min_por_dia")
    print("- media_temp_in_out")


if __name__ == "__main__":
    main()
