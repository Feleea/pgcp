import requests
import json
import os
import zipfile
from io import BytesIO
from dotenv import load_dotenv, dotenv_values
import time


class atualizar_versao():
    def __init__(self) -> None:

        # Versão do programa instalada
        self.versao_instalada = self.get_versao_instalada()
        print(self.versao_instalada)
        time.sleep(1)

        load_dotenv()

        # Variaveis
        self.token = dotenv_values()["token"]
        self.repo_nome = "auto-pgcp"
        self.repo_proprietario = "Feleea"
        self.informacoes = self.consultar_repositorio()


        # Versão mais recente do programa
        self.versao_atual = self.informacoes["name"]

        # Atualiza o programa
        if self.versao_instalada != self.versao_atual: self.atualizar_arquivos()

        time.sleep(1)
        


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


    def get_versao_instalada(self):
        """Pega as informações da versão instalada"""

        diretorio_raiz = os.path.dirname(os.path.dirname(__file__))
        for dirpath, dirnames, filenames in os.walk(diretorio_raiz):
            if "program" in dirnames:
                with open(f"program/version", "r", encoding='utf-8') as file:
                    version = file.read().strip()
                    return version

        '''with open(f"program/version", "r", encoding='utf-8') as new_notepad:
            new_notepad.write("v0.0.0")
            return '''


    def update_version_file(self):
        """Atualiza as informações da versão instalada"""

        diretorio_raiz = os.path.dirname(os.path.dirname(__file__))
        for dirpath, dirnames, filenames in os.walk(diretorio_raiz):
            if "program" in dirnames:
                with open(f"program/version", "w", encoding='utf-8') as file:
                    print(self.versao_atual)
                    return file.write(self.versao_atual)
                

    def atualizar_arquivos(self):
        """Baixa todos os arquivos da nova versão para atualização"""

        arquivoZip = self.informacoes["zipball_url"]

        resposta_zip = requests.get(arquivoZip, stream=True)

        with zipfile.ZipFile(BytesIO(resposta_zip.content)) as zip_ref:
            print(zip_ref.filelist)
            zip_ref.extractall(os.path.dirname(os.path.dirname(__file__)))

        self.update_version_file()




                
