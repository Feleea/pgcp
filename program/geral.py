from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from winotify import Notification, audio
import random
import os
from time import sleep
from datetime import datetime
import functools
from dotenv import load_dotenv, dotenv_values



def carregar_config():
    load_dotenv()

    return dict(dotenv_values())
    


def abrir_navegador(is_navegador=True) -> webdriver.Chrome:
        
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--log-level=3")
        if not is_navegador: options.add_argument("--headless=new")

        navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        navegador.implicitly_wait(3)

        return navegador



def fechar_navegador(navegador: webdriver.Chrome):
    navegador.quit()



def usuarios(site: str):
    login_senha = {
        "SISVISA": ["bot@sisvisa.com.br", "Felipe@123"], # Login e senha do bot admin e regulado
        "PGLS": ["bot@pgls.com.br", "Felipe@123"], # Login e senha do bot admin e regulado
        "JIRA": ["felipe.oliveira@branef.com.br", "Babymetal@7063"],
        "Engenheiro": ["bot_engenheiro@sisvisa.com.br", "Felipe@123"],
        "Felipe": ["felipe.oliveira@branef.com.br", "Felipe@123"],
        "Arquivo": ["bot_arquivo@sisvisa.com.br", "Felipe@123"],
        "ArquivoPGLS": ["bot_arquivo@pgls.com.br", "Felipe@123"]
    }

    if site in login_senha.keys(): return login_senha[site]



def list_ambiente(ambiente: str=None):
    dict_ambiente = {
        "test": "test",
        "hmlg": "hmlg",
        "staging": "staging",
    }
    
    if ambiente in dict_ambiente: return dict_ambiente[ambiente]

    return dict_ambiente.keys()



def criar_email_provisorio_moakt(nome=f"agente {random.randint(1,99999)}"):
    navegador_email = abrir_navegador(headless=True)
    navegador_email.get("https://moakt.com")
    navegador_email.refresh()
    navegador_email.find_element(By.NAME, "username").send_keys(str(f"{nome}"))
    navegador_email.find_element(By.NAME, "setemail").click()
    email = navegador_email.find_element(By.ID, "email-address").text
    print(f"E-mail {email} provisório criado.")
    return email, navegador_email


def ativar_usuario_moakt(navegador_email: webdriver.Chrome):

    errors = 0

    while True:
            
            email = navegador_email.find_element(By.ID, "email-address").text
            navegador_email.find_element(By.CLASS_NAME, "material-icons.button-blue").click()
            navegador_email.find_element(By.LINK_TEXT, 'PGLS - Confirmação de Cadastro do Usuário').click()
            iframe = navegador_email.find_element(By.TAG_NAME, 'iframe')
            navegador_email.switch_to.frame(iframe)
            link = navegador_email.find_element(By.LINK_TEXT, 'Ativar usuário').get_attribute("href")
            navegador_email.get(link)
            if "/admin/" in navegador_email.current_url:
                navegador_email.find_element(By.ID, "password").send_keys("123")
                navegador_email.find_element(By.CLASS_NAME, "btn.btn-lg.btn-brand.btn-elevate").click()
            else:
                navegador_email.find_element(By.ID, "buttonClose").click()
            WebDriverWait(navegador_email, 5).until(EC.visibility_of(navegador_email.find_element(By.ID, "Email")))
            navegador_email.quit()
            print(f"Usuário {email} ativado.")
            return False
    


def win_notification(msg: str):
    notificacao = Notification(app_id="Cadastro Automatico",
                                title="Notificação da Automação",
                                msg=msg)
    # notificacao.add_actions(label="Abrir navegador", launch=navegador.maximize_window())
    notificacao.set_audio(audio.Reminder, loop=False)
    notificacao.show()


def formatar_cnpj(cnpj: str):
    # Remover caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Formatar o CNPJ
    cnpj_formatado = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
    
    return cnpj_formatado


def apagar_zendesk(navegador: webdriver.Chrome):
    if len(navegador.find_elements(By.ID, "launcher")) > 0:
        elemento = navegador.find_element(By.ID, "launcher")
        navegador.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", elemento)
        return
    if len(navegador.find_elements(By.CLASS_NAME, "zendesk-fake-alert")) > 0:
        elemento = navegador.find_element(By.CLASS_NAME, "zendesk-fake-alert")
        navegador.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", elemento)
        return


def stop(navegador: webdriver.Chrome, skip_stop: bool):
    '''skip_stop = True -> Pula em caso de coicidência\n
       skip_stop = False -> Pausa por 600 segundos'''

    if skip_stop: return

    win_notification("Automação concluida. A tela ficará aberta por 10 minutos antes de fechar sozinha.")
    print("######################## Em pausa ########################")
    sleep(600)
    fechar_navegador(navegador)

# Refatorar
def arquivos_log(log: str):

    def salvar_cnpj_notepad(cnpj: str):
        with open(f"{arquivos_log("cnpjs")}", 'a') as arquivo:
            arquivo.write(f'{datetime.today().strftime("%H:%M:%S - %d/%m/%Y")} - {cnpj}\n')
    
    logs = {
        "cnpjs": "lista de cnpjs criados.txt",
        "processos": "lista de processos criados.txt"
    }
    return logs[log]



# Decorador de log no terminal e erros
def log_terminal_automacao(mensagem: str):

    def dale(funcao, skip_log=False):

        if skip_log: return
        @functools.wraps(funcao)
        def wrapper(*args, **kwargs):
            erros = 5
            navegador = args[0].navegador
            print(f"{mensagem}", end="\r")

            while True:

                try:
                    result = funcao(*args, **kwargs)
                    print(f"{mensagem} ... \033[32mConcluído.\033[0m")
                    break

                except Exception as e:
                    erros -= 1
                    if erros > 0:
                        print(f"{mensagem} ... \033[31mErro. Tentando novamente... \033[0m")
                        navegador.refresh()

                    else:
                        navegador.execute_script("alert('Deu erro aqui viu');")
                        sleep(300)
                        navegador.quit()
                        print("Finalizando o programa...", end="\r")

            return result
        
        return wrapper
    
    return dale


def procurar_arquivos(nome_arquivo) -> str:
    caminho_atual = os.path.realpath(__file__)
    diretorio_raiz = os.path.dirname(os.path.dirname(caminho_atual))
    # diretorio_raiz = os.path.realpath(__file__)
    
    # Caminha pelo diretório raiz e subdiretórios
    for dirpath, dirnames, filenames in os.walk(diretorio_raiz):
        for filename in filenames:
            if nome_arquivo in filename:
                # Adiciona o caminho completo do arquivo encontrado
                return os.path.join(dirpath, filename)
    
    return nome_arquivo


def procurar_pasta(nome_pasta):
    caminho_atual = os.path.realpath(__file__)
    diretorio_raiz = os.path.dirname(os.path.dirname(caminho_atual))
    
    # Caminha recursivamente pelo diretório raiz e subdiretórios
    for dirpath, dirnames in os.walk(diretorio_raiz):
        for dirname in dirnames:
            if nome_pasta in dirname:
                # Adiciona o caminho completo da pasta encontrado
                return os.path.join(dirpath, dirname)
        return 
    
