from geral import *



class AutomatePGCP:
    def __init__(self) -> None:
        print("Iniciando o programa")

        config = carregar_config()

        self.navegador = abrir_navegador()
        self.ambiente = config["ambiente"]
        self.username = config["usuario"]
        self.senha = config["senha"]

    
    @log_terminal_automacao("Realizando o login")
    def login(self):
        navegador = self.navegador

        navegador.get(f"https://{self.ambiente}.pgcp.com.br/app/dashboard")
        navegador.find_element(By.CLASS_NAME, "login__input.login__input--cpf").send_keys(self.username)
        navegador.find_element(By.CLASS_NAME, "login__input.login__input--password").send_keys(self.senha)
        navegador.find_element(By.CLASS_NAME, "login__button.login__button-signin").click()
        WebDriverWait(navegador, 10).until(EC.any_of(
            EC.visibility_of_element_located((By.ID, "sidebarNav")),
            EC.url_contains("dashboard")))
        
    
    def tela_inicial():
        
        # testar filtros

        pass


    def usuario(self, filtros, criar, editar):
        navegador = self.navegador

        def usuarios_filtros():

            @log_terminal_automacao('Testando o filtro "Pesquisar" com um CPF')
            def usuarios_filtro_cpf(self: AutomatePGCP):

                # Acessar página de usuários filtrar pelo username e espera até ele aparecer no corpo da tabela
                navegador.get(f"https://{self.ambiente}.pgcp.com.br/app/users")
                WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))
                navegador.find_element(By.CLASS_NAME, "form-control.filter__search-input").send_keys(self.username)
                navegador.find_element(By.CLASS_NAME, "unit__button.filtro").click() # Esse botão tem a classe light-blue também
                WebDriverWait(navegador, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "tbody"), "Idrissa Akuna Elba"))
            
            @log_terminal_automacao('Testando o filtro "Perfil" com um perfil aleatório')
            def usuarios_filtro_perfil(self: AutomatePGCP):

                # Acessar página de usuários filtrar pelo
                navegador.get(f"https://{self.ambiente}.pgcp.com.br/app/users")
                WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "tbody")))

                # Pega o resultado da primeira busca
                resultadosDoFiltro = navegador.find_elements(By.CLASS_NAME, "table-sectors__row")
                resultadosDoFiltro = [f"{i.text}" for i in resultadosDoFiltro]
                
                # Pega todos os perfis seleciona um e clica pra filtrar
                perfis = navegador.find_elements(By.CLASS_NAME, "role-content__option")
                perfis = perfis[1:]
                navegador.find_element(By.CLASS_NAME, "select-perfil").send_keys(random.choice(perfis).text)
                navegador.find_element(By.CLASS_NAME, "unit__button.filtro").click() # Esse botão tem a classe light-blue também
                sleep(0.5)

                # Pega o resultado da segunda busca
                resultadosDoNovoFiltro = navegador.find_elements(By.CLASS_NAME, "table-sectors__row")
                resultadosDoNovoFiltro = [f"{i.text}" for i in resultadosDoNovoFiltro]
                
                # Faz a comparação
                if resultadosDoFiltro == resultadosDoNovoFiltro: raise NotImplementedError.add_note("O resultado do filtro não mudou")
                
                

            return usuarios_filtro_cpf(self), usuarios_filtro_perfil(self)


        @log_terminal_automacao("Testando a criação de usuário")
        def usuarios_criar():
            pass

        @log_terminal_automacao("Testando editar usuário")
        def usuarios_editar():
            pass

        if filtros: usuarios_filtros()