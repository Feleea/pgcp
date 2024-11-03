# auto-pgcp
 
# Como instalar:

 ### 1. Criar ambiente virtual no VScode
 * ctrl + shifit + P > Python: Create Environment

 ## Scripts no PC
 - Get-ExecutionPolicy -List
 - Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
 - Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser

 ### 2. Ativar o ambiente virtual
 ```bash
 .venv\Scripts\Activate.ps1
 ```

 ### 3. Instalar as bibliotecas
 * Durante a criação do ambiente virtual o VS code também pergunta se você deseja instalar as dependencias e deixa esse arquivo como sugestão, é só selecionar ele e continuar com a criação do ambiente virtual. Caso isso não ocorra, instale as bibliotecas com a linha abaixo no terminal.
 ```bash
 pip install -r requirements.txt
 ```

 pyinstaller --onefile --distpath ".\dist\main\" update_pgcp.py