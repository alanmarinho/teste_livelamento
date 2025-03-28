import pdfplumber
import pandas as pd
import os
import glob
import re

BASE_PATH = "tranformacao_dados"
pdf_path = "web_scraping/pdfs"
csv_name = "Teste_Alan_Marinho.zip"
CSV_FOLDER = "CSVs"


def find_pdf(directory, identifier="ANEXO_I_"):
    pdf_files = glob.glob(os.path.join(directory, f"*{identifier}*.pdf"))

    if pdf_files:
        pdf_path = pdf_files[0]
        normalized_path = os.path.abspath(pdf_path)
        return normalized_path
    else:
        print(f"Nenhum arquivo PDF encontrado com o identificador '{identifier}'.")
        return None


def legends_normalizer(legends):
    compact_folder = os.path.join(BASE_PATH, "compacts")
    os.makedirs(compact_folder, exist_ok=True)
    pattern = r"(\w+):\s(.*?)(?=\s\w+:|$)"  # regex by ChatGPT
    texto = re.sub(r"\s\w+$", "", legends[0])

    matches = re.findall(pattern, texto)
    data_path = os.path.join(BASE_PATH, CSV_FOLDER, "data.csv")

    df = pd.read_csv(data_path)

    for sigla, descricao in matches:

        if sigla in ["OD", "AMB"]:
            df[sigla] = df[sigla].replace(sigla, descricao)

    compact_path = os.path.join(compact_folder, "Teste_Alan_Marinho.zip")
    df.to_csv(data_path, index=False)
    df.to_csv(compact_path, index=False)

    return matches


def extract_tables():
    pdf = find_pdf(directory=pdf_path)
    if not pdf:
        print("Dados não encontrados")
        return

    all_tables = []
    footers = []

    csv_folder = os.path.join(BASE_PATH, CSV_FOLDER)
    os.makedirs(csv_folder, exist_ok=True)

    with pdfplumber.open(pdf) as pdf:
        for page_number in range(len(pdf.pages)):
            print(f"Processando página {page_number + 1}/{len(pdf.pages)}")
            page = pdf.pages[page_number]

            if page_number == 4:
                footer_text = get_footers(page)
                if footer_text:
                    footers.append(footer_text)
                else:
                    footers.append("")

            table = page.extract_table()

            if table:
                all_tables.append(table)

    if all_tables:
        header = all_tables[0][0]
        flat_table = [item for sublist in all_tables for item in sublist[1:]]

        df = pd.DataFrame(flat_table, columns=header)
        file_path = os.path.join(csv_folder, "data.csv")
        df.to_csv(file_path, index=False)

        legends_normalizer(footers)

    else:
        print("Nenhuma tabela encontrada no PDF.")


def get_footers(page):
    text = page.extract_text()

    if text:
        text = text.replace("\n", " ")
        footer_pattern = r"Legenda:(.*)"
        footer_match = re.search(footer_pattern, text, re.IGNORECASE)

        if footer_match:
            footer_text = footer_match.group(1).strip()

            return footer_text
        else:
            print("Legenda não encontrada.")
            return None
    else:
        print("Texto da página não encontrado.")
        return None
