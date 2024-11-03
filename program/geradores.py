import random
from reportlab.pdfgen import canvas
import os


def gerar_pdf(treinamento=(True, False, "random")):
    '''True: doc_valido.pdf\n
    False: page_teste.pdf\n
    random: "doc_valido.pdf" ou "doc_invalido.pdf"'''

    dir_path = os.path.dirname(os.path.realpath(__file__))
    arquivos = ("doc_valido.pdf", "doc_invalido.pdf")
    if type(treinamento) == tuple:
        treinamento = False

    match treinamento:
        case True:
            arquivo = "doc_valido.pdf"
        case False:
            arquivo = "page_teste.pdf"
        case "random":
            arquivo = random.choice(arquivos)

    # VERIFICAR SE O ARQUIVO EXISTE
    for root, dirs, files in os.walk(dir_path):
        if arquivo in files:
            pdf_path = os.path.join(dir_path, f"resources/{arquivo}")
            return pdf_path
    
    # SE NÃO EXISTE, CRIA UM
    c = canvas.Canvas(f"resources/{arquivo}", pagesize="A4")
    c.setFontSize(18)

    if arquivo == "page_teste.pdf": c.drawString(x=150, y=700, text="Esse é um documento de teste")
    elif arquivo == "doc_valido.pdf": c.drawString(x=100, y=700, text="Esse documento está correto. Pode aprovar.")
    elif arquivo == "doc_invalido.pdf": c.drawString(x=100, y=700, text="Esse documento está errado ou invalido. Peça correção.")

    c.save()
    pdf_path = os.path.join(dir_path, f"resources/{arquivo}")
    print(pdf_path)
    return pdf_path


def gerar_cpf():
    cpf = [random.randint(0, 9) for _ in range(9)]  # Gera os 9 primeiros dígitos
    cpf = cpf + calcula_digitos_verificadores(cpf)  # Adiciona os dois últimos dígitos
    return "{}{}{}{}{}{}{}{}{}{}{}".format(*cpf)


def calcula_digitos_verificadores(cpf):
    # Primeiro dígito verificador
    soma = sum([cpf[i] * (10 - i) for i in range(9)])
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # Segundo dígito verificador
    cpf_com_digito1 = cpf + [digito1]
    soma = sum([cpf_com_digito1[i] * (11 - i) for i in range(10)])
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    return [digito1, digito2]


def gerar_cnpj(punctuation = False):
    n = [random.randrange(10) for i in range(8)] + [0, 0, 0, 1]
    v = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 6]
    # calcula dígito 1 e acrescenta ao total
    s = sum(x * y for x, y in zip(reversed(n), v))
    d1 = 11 - s % 11
    if d1 >= 10:
      d1 = 0
    n.append(d1)
    # idem para o dígito 2
    s = sum(x * y for x, y in zip(reversed(n), v))
    d2 = 11 - s % 11
    if d2 >= 10:
      d2 = 0
    n.append(d2)
    if punctuation:
      return "%d%d.%d%d%d.%d%d%d/%d%d%d%d-%d%d" % tuple(n)
    else:
      return "%d%d%d%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)

