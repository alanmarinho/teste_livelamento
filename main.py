import cmd
import asyncio
from web_scraping import scraping
from tranformacao_dados import tranformacao
from banco_dados import banco


class MyCLI(cmd.Cmd):
    prompt = ">> "
    intro = """
    "Teste de nivelamento IntuitiveCare Alan Marinho.
    
    Comandos:
    'exe 1' - executar TESTE DE WEB SCRAPING
    'exe 2' - executar TESTE DE TRANSFORMAÇÃO DE DADOS
    'exe 3 db' - carregar os dados no banco
    'exe 3 q1' - query maires gasto no ultimo trimestre
    'exe 3 q1' - query maiores gastos no ultimo ano
    
    ---------------
    
    exit (para sair)"
    """

    def do_hello(self, line):
        print("Hello, World!")

    def do_exit(self, line):
        return True

    def do_exe(self, line):
        comandos = {
            "1": self.async_teste1,
            "2": self.async_teste2,
            "3 db": self.async_teste3_db,
            "3 q1": self.async_teste3_query1,
            "3 q2": self.async_teste3_query2,
        }

        if line in comandos:
            self.run_async(comandos[line])
        else:
            print(f"Erro: '{line}' não é um comando válido.")

    def run_async(self, coroutine):
        asyncio.run(coroutine())

    def postcmd(self, stop, line):
        print(self.intro)
        return stop

    async def async_teste1(self):
        print("Executando TESTE DE WEB SCRAPING...")
        await scraping.get_pdfs()
        print("Finalizado!")

    async def async_teste2(self):
        print("Executando TESTE DE TRANSFORMAÇÃO DE DADOS...")
        tranformacao.extract_tables()
        print("Finalizado!")

    async def async_teste3_db(self):
        print(
            "Preparando banco, esse processo pode demorar um pouco devido a grande quantidade de dados!"
        )
        banco.prepare_db()
        print("Finalizado!")

    async def async_teste3_query1(self):
        print(
            "Maiores gastos no ultimo trimestre na categoria 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '"
        )
        banco.query1()

    async def async_teste3_query2(self):
        print(
            "Maiores gastos no ultimo ano na categoria 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '"
        )
        banco.query2()


if __name__ == "__main__":
    MyCLI().cmdloop()
