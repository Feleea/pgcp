import re
import os
from bs4 import BeautifulSoup
from templates._geral import webdriver, By, InvalidSessionIdException, NoSuchWindowException, procurar_arquivos
from threading import Thread 
import sys


def logs_corretor():
    """Deixa apenas os dez últimos arquivos txt de logs na pasta e retorna uma lista com o nome dos arquivos"""

    dir_main_path = os.path.dirname(f"{os.path.realpath(__file__)}")
    try:
        dir_logs = os.path.join(dir_main_path, "logs")
        list_dir = os.listdir(dir_logs)
        while len(list_dir) > 9:
            os.remove(f"{dir_logs}/{list_dir[0]}")
            # list_dir = os.listdir(dir_logs)
            
        return list_dir
    
    except FileNotFoundError:
        os.mkdir(os.path.join(dir_main_path, "logs"))


def verificar_ortografia(navegador: webdriver.Chrome, run: str, frontEnd: bool, words: str=""):
    """lista de palavras https://www.ime.usp.br/~pf/dicios/br-utf8.txt"""
    
    page = navegador.page_source
    url = navegador.current_url
    nome_do_arquivo = f'Possíveis erros de digitação {run}.txt'
    dir_this_path = os.path.dirname(f"{os.path.realpath(__file__)}")


    def verificar_pagina_corrigida():
        """Verificar se o corretor já passou pela pagina atual"""

        if os.path.isfile(f"{dir_this_path}/logs/{nome_do_arquivo}"):
            with open(procurar_arquivos(f"{dir_this_path}/logs/{nome_do_arquivo}"), 'r', encoding='utf-8') as new_notepad:
                if url in new_notepad: return True

    def campos_obrigatorios(navegador: webdriver.Chrome):

        motivos_do_obrigatorio = []
        obrigatorio = navegador.find_elements(By.TAG_NAME, 'input')
        for item in obrigatorio:
            try: motivo = item.get_attribute('data-val-required')
            except: continue
            
            if motivo is None:
                continue
            for palavra in motivo.split():
                motivos_do_obrigatorio.append(palavra)

        return motivos_do_obrigatorio

    def novo_notepad():
        """Cria um novo bloco de notas para salvar as palavras erradas"""

        nome_do_arquivo = f'Possíveis erros de digitação {run}.txt'
        dir_this_path = os.path.dirname(f"{os.path.realpath(__file__)}")

        # Se o arquivo já existir não tenta criar ou escrever o texto da legenda novamente
        if os.path.isfile(f"{dir_this_path}/logs/{nome_do_arquivo}"): return dir_this_path, nome_do_arquivo

        with open(procurar_arquivos(f"{dir_this_path}/logs/{nome_do_arquivo}"), 'a', encoding='utf-8') as new_notepad:
            new_notepad.write("Legenda:\nUm tio(~) na frente da palavra, ela está naquelas mensagens que o navegador dá"
                              " quando um campo obrigatório não foi preenchido\n")
            new_notepad.write("Dois tios(~~), ela está no retorno do backend, aquela mensagem vermelha ou verde"
                              " que aparece no sistema quando alguma regra foi/não foi atendida\n\n")

    def salvar_palavras_erradas_notepad():
        """Escreve a palavra encontrada na página web, que não foi localizada nos dicionários"""

        def tratar_palavra(word):
            word_no_specials = re.sub('[!#$%&*(),.;:?+←↑→↓<>]', '', word).lower() # Remove caracteres especiais na palavra
            word_no_specials = re.sub('[0-9]-[0-9]', '', word_no_specials) # Remove traços entre números
            word_no_specials = re.sub('[0-9]/[0-9]', '', word_no_specials) # Remove barras entre números
            word_no_specials = re.sub('[0-9]_[0-9]', '', word_no_specials) # Remove underline entre números

            if word_no_specials in palavras_conteudo: return
            if word_no_specials in palavras_ignoradas_conteudo: return
            if word_no_specials in nomes_propios_conteudo: return
            if word_no_specials in sobrenomes_conteudo: return

            if re.fullmatch(r"\d+", word_no_specials): # Ignora se for apenas números
                return
            if re.fullmatch(r'(?=.*[a-zA-Z])(?=.*\d).*', word_no_specials): # Ignora a string que possui letras e números
                return
            if re.fullmatch(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9\.a-zA-Z0-9]{1,6}', word): # Ignora a string se for um e-mail
                return
            if re.fullmatch(r'\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}', word): # Ignora se for um CNPJ
                return
            
            return word_no_specials

        # Procura palavras erradas no corpo da página
        for word in words: 
            word_no_specials = tratar_palavra(word)
            # Escreve palavras erradas encontradas no corpo da página no bloco de notas
            if type(word_no_specials) == str:
                with open(procurar_arquivos(f"{dir_this_path}/logs/{nome_do_arquivo}"), 'a', encoding='utf-8') as new_notepad:
                    new_notepad.write(f"{word_no_specials}\n")
        
        # Procura palavras erradas nos elementos html da página
        for word in obrigatorios:
            word_no_specials = tratar_palavra(word)
            # Escreve palavras erradas encontradas nos elementos html da página no bloco de notas
            if type(word_no_specials) == str:
                with open(procurar_arquivos(f"{dir_this_path}/logs/{nome_do_arquivo}"), 'a', encoding='utf-8') as new_notepad:
                    new_notepad.write(f"~~{word_no_specials}\n")

    def cabecalho_novo_notepad():
        with open(procurar_arquivos(f"{dir_this_path}/logs/{nome_do_arquivo}"), 'a', encoding='utf-8') as new_notepad:
            new_notepad.write(f"Inicio: {url}\n-----------------------------------------------------------\n")

    def rodape_novo_notepad():
        with open(procurar_arquivos(f"{dir_this_path}/logs/{nome_do_arquivo}"), 'a', encoding='utf-8') as new_notepad:
            new_notepad.write(f"Fim: {url}\n-----------------------------------------------------------\n")


    if verificar_pagina_corrigida(): return

    print(f"Corretor rodando na página {url}")

    # Pegar as palavras no dicionário
    with open(procurar_arquivos("palavras_geral.txt"), 'r', encoding='utf-8') as palavras:
        palavras_conteudo = palavras.read().lower()

    # pegar as palavras ignoradas
    with open(procurar_arquivos("palavras_ignoradas.txt"), 'r', encoding='utf-8') as palavras_ignoradas:
        palavras_ignoradas_conteudo = palavras_ignoradas.read().lower()

    # Pegar os nomes propios
    with open(procurar_arquivos("nomes_propios.txt"), 'r', encoding='utf-8') as nomes_propios:
        nomes_propios_conteudo = nomes_propios.read().lower()

    # Pegar sobrenomes
    with open(procurar_arquivos("sobrenomes_geral.txt"), 'r', encoding='utf-8') as sobrenomes:
        sobrenomes_conteudo = sobrenomes.read().lower()

    if frontEnd:
        # Extraindo todo o texto da página
        soup = BeautifulSoup(page, "html.parser")
        page_text = soup.get_text()

        # Separando os inputs obrigatorios em uma lista
        obrigatorios = campos_obrigatorios(navegador)

        # Separando as palavras em uma lista
        words = page_text.split()
    else:
        words = words
    
    novo_notepad()
    cabecalho_novo_notepad()
    salvar_palavras_erradas_notepad()
    rodape_novo_notepad()

    print(f"Corretor concluido na página {url}")
    

def start_url_monitor(self):
    """Retorna uma função que inicia o monitoramento da URL em uma thread separada."""
    navegador = self.navegador
    run = self.run

    def monitor_url_change(navegador: webdriver.Chrome, run):
        """Monitora as mudanças de URL no navegador e executa a função verificar_ortografia sempre que a URL mudar."""

        last_url = navegador.current_url
        frontEnd = True
        
        while True:
            try:
                current_url = navegador.current_url
                if current_url != last_url:
                    last_url = current_url
                    corretor_thread = Thread(target=verificar_ortografia, args=(navegador, run, frontEnd))
                    corretor_thread.start()
                    corretor_thread.join()

            except InvalidSessionIdException:
                print(f"Encerrando o programa devido à sessão inválida ou problema na janela do navegador. {corretor_thread.name}")
                sys.exit(1)
            
            except NoSuchWindowException:
                sys.exit(1)

            except Exception as e:
                print(f"Erro inesperado: {e}, {corretor_thread.name}, {__name__}")
                print("Encerrando o corretor devido a um erro inesperado.")
                sys.exit(1)

    def _start_url_monitor():
        '''Inicia o monitoramento da URL em uma thread separada.'''

        url_monitor_thread = Thread(target=monitor_url_change, args=(navegador, run))
        url_monitor_thread.daemon = True  # Define a thread como "daemon", ela será encerrada quando o programa principal encerrar.
        url_monitor_thread.start()
    
    return _start_url_monitor()

# Voltar para implementar no futuro
def start_toast_monitor(self):
    '''Retorna uma função que inicia o monitoramento em busca das mensagems de erro e sucesso geradas pelo backend em uma thread separada.'''
    navegador = self.navegador
    run = self.run
    frontEnd = False

    def monitor_toast_displayed(navegador: webdriver.Chrome, run):
        '''Monitora o aparecimento das mensagems de erro e sucesso geradas pelo backend.'''
        while True:
            try:
                print("AQui")
                mensagem = navegador.find_element((By.ID, "toast-container")).text
                # mensagem = navegador.find_element((By.CLASS_NAME, "toast-message")).text
                corretor_toast = Thread(target=verificar_ortografia, args=(navegador, run, frontEnd, mensagem))
                print("Aqui 2")
                corretor_toast.start()
                corretor_toast.join()

            
            except InvalidSessionIdException:
                print("Encerrando o programa devido à sessão inválida ou problema na janela do navegador.")
                sys.exit(1)
                
            except Exception as e:
                print(f"Erro inesperado no monitor_toast: {e}")
                print("Encerrando o corretor devido a um erro inesperado.")
                os._exit(1)

    def _start_toast_monitor():
        '''Inicia o monitoramento em busca das mensagems de erro e sucesso geradas pelo backend em uma thread separada.'''

        toast_monitor_thread = Thread(target=monitor_toast_displayed, args=(navegador, run))
        toast_monitor_thread.daemon = True  # Define a thread como "daemon", ela será encerrada quando o programa principal encerrar.
        toast_monitor_thread.start()

    return _start_toast_monitor()

