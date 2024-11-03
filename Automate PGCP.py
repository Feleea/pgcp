import context
from program import admin

pgcp = admin.AutomatePGCP()

pgcp.login()
pgcp.usuario(True, False, False)