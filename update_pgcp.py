import requests
import json
import os
import shutil
import zipfile
from io import BytesIO
from dotenv import load_dotenv, dotenv_values
import time
import functools


def log_atualizacao(mensagem: str):

    def dale(funcao):

        @functools.wraps(funcao)
        def wrapper(*args, **kwargs):
            # erros = 5
            print(f"{mensagem}", end="\r")

            while True:

                try:
                    result = funcao(*args, **kwargs)
                    print(f"{mensagem} ... \033[32mConcluído.\033[0m")
                    break

                except Exception as e:
                    print("")
                    print("Deu erro")
                    time.sleep(10)
                    print(e)
                    time.sleep(100)
                    # erros -= 1
                    # if erros > 0:
                        # print(f"{mensagem} ... \033[31mErro. Tentando novamente... \033[0m")

                    # else:
                    #   print("Finalizando o programa...", end="\r")

            return result
        
        return wrapper
    
    return dale


class atualizar_versao():
    def __init__(self) -> None:

        # Versão do programa instalada
        self.versao_instalada = self.get_versao_instalada()

        load_dotenv()

        # Variaveis
        self.token = dotenv_values()["token"]
        self.repo_nome = "pgcp"
        self.repo_proprietario = "Feleea"
        self.informacoes = self.consultar_repositorio()

        # Versão mais recente do programa
        self.versao_atual = self.informacoes["tag_name"]

        # Atualiza o programa
        if self.versao_instalada != self.versao_atual:
            self.atualizar_arquivos()
            # self.update_version_file()
        

    @log_atualizacao("Consultando o repositório")
    def consultar_repositorio(self) -> dict:

        url = f"https://api.github.com/repos/{self.repo_proprietario}/{self.repo_nome}/releases/latest"
                
        # Headers com o token de acesso
        headers = {
            # "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Requisição GET para verificar se há atualizações
        resposta = requests.get(url, headers=headers)

        # Verifique se a resposta foi bem-sucedida
        if resposta.status_code != 200: raise ConnectionRefusedError

        return resposta.json()


    @log_atualizacao("Pegando a versão instalada")
    def get_versao_instalada(self):
        """Pega as informações da versão instalada"""

        diretorio_raiz = os.path.dirname(os.path.dirname(__name__))
        for dirpath, dirnames, filenames in os.walk(diretorio_raiz):
            if "_internal" in dirpath:
                with open(f"{dirpath}/version", "r", encoding='utf-8') as file:
                    version = file.read().strip()
                    return version


    @log_atualizacao("Salvando o arquivo version")
    def update_version_file(self):
        """Atualiza as informações da versão instalada"""

        diretorio_raiz = os.path.dirname(os.path.dirname(__name__))
        for dirpath, dirnames, filenames in os.walk(diretorio_raiz):
            if "_internal" in dirpath:
                with open(f"{dirpath}/version", "w", encoding='utf-8') as file:
                    return file.write(self.versao_atual)
                

    @log_atualizacao("Atualizando o programa")
    def atualizar_arquivos(self):
        """Baixa todos os arquivos da nova versão para atualização"""

        arquivoZip = self.informacoes["zipball_url"]
        resposta_zip = requests.get(arquivoZip, stream=True)
        # shutil.rmtree(os.path.join(os.path.dirname("__main__"), "_internal"))

        with zipfile.ZipFile(BytesIO(resposta_zip.content)) as zip_ref:
            for file in zip_ref.filelist:
                if "_internal/" in file.filename:
                    zip_ref.extract(file, "../")
            
            '''for member in zip_ref.namelist():
                if "_internal/" in member and not member.endswith("/"):
                    # Remove o prefixo do diretório base para extrair no local desejado
                    member_path = os.path.relpath(member, start=os.path.commonpath([member]))

                    # Define o caminho completo para extração
                    extract_target_path = os.path.join("_internal/", os.path.basename(member_path))

                    # Extrai o arquivo específico
                    with zip_ref.open(member) as source, open(extract_target_path, "wb") as target:
                        target.write(source.read())'''
                    
            for file in zip_ref.filelist:
                if "main.exe" in file.filename:
                    zip_ref.extract(file, path="../")
                    # zip_ref.extract(file, os.path.join(os.path.dirname(__name__), "_internal/"))
                    break



if __name__ == "__main__":
    print(os.path.dirname("__main__"))
    atualizar_versao()
    time.sleep(300)
