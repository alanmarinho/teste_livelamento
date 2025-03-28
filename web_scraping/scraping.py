import os
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
import zipfile

SCRAPING_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
BASE_PATH = "web_scraping"


async def download_pdf(url_pdf, file_name):

    try:
        PDF_FOLDER = "pdfs"
        pdf_folder = os.path.join(BASE_PATH, PDF_FOLDER)
        os.makedirs(pdf_folder, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(url_pdf) as response:
                if response.status == 200:
                    file_path = os.path.join(BASE_PATH, PDF_FOLDER, file_name)
                    async with aiofiles.open(file_path, "wb") as file:
                        content = await response.read()
                        await file.write(content)
                else:
                    print(f"Failed to download PDF. Status code: {response.status}")
    except Exception as err:
        print(f"Download item error: {err}")
        return False


async def get_pdfs():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(SCRAPING_URL) as response:
                if response.status != 200:
                    print("Error when accessing the page")
                    return

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                for link in soup.find_all("a", href=True):
                    if "ANEXO" in link.get_text().upper():
                        href = link["href"]
                        if href.lower().endswith(".pdf"):
                            url_pdf = urljoin(SCRAPING_URL, href)
                            file_name = href.split("/")[-1]
                            await download_pdf(url_pdf, file_name)
                compact_files(directory="pdfs", file_name="anexos.zip")
    except Exception as err:
        print(f"Get PDFs error: {err}")
        return False


def compact_files(directory, file_name):
    try:

        COMPACT_FOLDER = "compacts"
        zip_folder = os.path.join(BASE_PATH, COMPACT_FOLDER)
        os.makedirs(zip_folder, exist_ok=True)
        zip_path = os.path.join(BASE_PATH, COMPACT_FOLDER, file_name)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file), directory),
                    )
    except Exception as err:
        print(f"Compact PDFs error: {err}")
        return False
