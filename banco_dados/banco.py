import mysql.connector
import pandas as pd
import glob
import os
from tabulate import tabulate

BASE_PATH = "banco_dados"
DB_NAME = "db_alan_marinho"
DB_USER = "user"
DB_PASSWORD = "pass"
DB_HOST = "127.0.0.1"
DB_PORT = "3390"


def connect_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        allow_local_infile=True,
    )
    if not conn.is_connected():
        raise Exception("Erro: Não foi possível conectar ao banco de dados.")

    return conn, conn.cursor()


def prepare_db():
    conn, cursor = connect_db()
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS operadoras_de_plano_de_saude_ativas (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            Registro_ANS INT UNIQUE,
            CNPJ TEXT,
            Razao_Social TEXT,
            Nome_Fantasia TEXT,
            Modalidade TEXT,
            Logradouro TEXT,
            Numero TEXT,
            Complemento TEXT,
            Bairro TEXT,
            Cidade TEXT,
            UF TEXT,
            CEP TEXT,
            DDD TEXT,
            Telefone TEXT,
            Fax TEXT,
            Endereco_eletronico TEXT,
            Representante TEXT,
            Cargo_Representante TEXT,
            Regiao_de_Comercializacao INTEGER,
            Data_Registro_ANS DATE
            )
            """
        )
        conn.commit()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS demonstracoes_contabeis( 
                id INT AUTO_INCREMENT PRIMARY KEY,
                DATA DATE,
                REG_ANS INT,
                CD_CONTA_CONTABIL VARCHAR(255),
                DESCRICAO TEXT,
                VL_SALDO_INICIAL DECIMAL(15, 2),
                VL_SALDO_FINAL DECIMAL(15, 2),
                CONSTRAINT fk_reg_ans
                    FOREIGN KEY (REG_ANS) REFERENCES operadoras_de_plano_de_saude_ativas(Registro_ANS)
            )
            """
        )
        conn.commit()

    except Exception as e:
        print(f"Prepare db error {e}")
    finally:
        cursor.close()
        conn.close()


def clean_dataframe(df):
    df = df.where(pd.notnull(df), None)
    return df


def load_data(file, table_name, filds_list):
    conn, cursor = connect_db()

    temp_file = "temp_formatted.csv"
    file.to_csv(temp_file, index=False, sep=";", encoding="utf-8")
    temp_file_path = os.path.abspath(temp_file)
    temp_file_path = temp_file_path.replace("\\", "/")
    try:
        cursor.execute(
            f"""
                LOAD DATA LOCAL INFILE '{temp_file_path}'
                INTO TABLE {table_name}
                FIELDS TERMINATED BY ';'
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 LINES
                {filds_list};
            """
        )
        conn.commit()

        print(f"Dados carregados com sucesso na tabela {table_name}!")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")

    finally:
        cursor.close()
        conn.close()
        os.remove(temp_file)


def import_csv_operadoras(csv_file):
    print(f"Processando arquivo: {csv_file}")
    df = pd.read_csv(csv_file, sep=";", encoding="utf-8")

    df = clean_dataframe(df)

    df["Data_Registro_ANS"] = pd.to_datetime(df["Data_Registro_ANS"], dayfirst=True)
    df["Registro_ANS"] = df["Registro_ANS"].astype(int)
    load_data(
        file=df,
        table_name="operadoras_de_plano_de_saude_ativas",
        filds_list="(Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero, Complemento, Bairro, Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico, Representante, Cargo_Representante, Regiao_de_Comercializacao, Data_Registro_ANS)",
    )


def import_csv_demonstracoes_contabeis(csv_files):
    for i in csv_files:
        print(f"Processando arquivo: {i}")
        df = pd.read_csv(i, sep=";", encoding="utf-8")

        df = clean_dataframe(df)

        df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=False)
        df["REG_ANS"] = df["REG_ANS"].astype(int)
        df["VL_SALDO_INICIAL"] = (
            df["VL_SALDO_INICIAL"].str.replace(",", ".").astype(float)
        )

        df["VL_SALDO_FINAL"] = df["VL_SALDO_FINAL"].str.replace(",", ".").astype(float)

        load_data(
            file=df,
            table_name="demonstracoes_contabeis",
            filds_list="(DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL)",
        )


def imports():
    prepare_db()
    file1 = glob.glob(
        os.path.join(os.path.join(BASE_PATH, "dados", "Relatorio_cadop.csv"))
    )
    if file1:
        import_csv_operadoras(csv_file=file1[0])
    else:
        print("Relatorio não encontrado")

    csv_files = glob.glob(os.path.join(BASE_PATH, "dados", "demonstracoes", "*.csv"))
    if len(csv_files) > 1:

        import_csv_demonstracoes_contabeis(csv_files=csv_files)
    else:
        print("Operadoras não encontradas")


def query1():
    try:
        conn, cursor = connect_db()
        query = """
                SELECT 
                    dc.REG_ANS,
                    ops.Razao_Social,
                    SUM(dc.VL_SALDO_FINAL) AS Total_Despesas
                FROM demonstracoes_contabeis dc
                JOIN operadoras_de_plano_de_saude_ativas ops 
                    ON dc.REG_ANS = ops.Registro_ANS
                WHERE YEAR(DATA) = (SELECT YEAR(DATA) FROM demonstracoes_contabeis ORDER BY DATA DESC LIMIT 1)
                AND QUARTER(DATA) = (SELECT QUARTER(DATA) FROM demonstracoes_contabeis ORDER BY DATA DESC LIMIT 1)
                AND DESCRICAO = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR "
                GROUP BY dc.REG_ANS,ops.Razao_Social
                ORDER BY Total_Despesas DESC
                LIMIT 10;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        tabela = data
        headers = ["Registro ANS", "Razão social", "total gasto"]
        dados = []
        for linha in tabela:
            data = [linha[0], linha[1], f"{linha[2]:,.2f}"]
            dados.append(data)
        print(tabulate(dados, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")

    finally:
        cursor.close()
        conn.close()


def query2():
    try:
        conn, cursor = connect_db()
        query = """
                SELECT 
                    dc.REG_ANS,
                    ops.Razao_Social,
                    SUM(dc.VL_SALDO_FINAL) AS Total_Despesas
                FROM demonstracoes_contabeis dc
                JOIN operadoras_de_plano_de_saude_ativas ops 
                    ON dc.REG_ANS = ops.Registro_ANS
                WHERE YEAR(DATA) = YEAR(CURDATE()) - 1
                AND DESCRICAO = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR "
                GROUP BY dc.REG_ANS,ops.Razao_Social
                ORDER BY Total_Despesas DESC
                LIMIT 10;
                """
        cursor.execute(query)
        data = cursor.fetchall()
        tabela = data
        headers = ["Registro ANS", "Razão social", "total gasto"]
        dados = []
        for linha in tabela:
            data = [linha[0], linha[1], f"{linha[2]:,.2f}"]
            dados.append(data)
        print(tabulate(dados, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
    finally:
        cursor.close()
        conn.close()
