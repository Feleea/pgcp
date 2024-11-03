import context
import att

# Corrigir para pegar o arquivo da dist desse repo e criar a funcionalidade pra abrir e fechar o programa

att.atualizar_versao()
from program import admin

pgcp = admin.AutomatePGCP()

'''except NotImplementedError:
    print("dale")

except Exception as e:
    print(e)'''

'''finally:
    time.sleep(5)
    '''


'''pgcp.login()
pgcp.usuario(True, False, False)'''