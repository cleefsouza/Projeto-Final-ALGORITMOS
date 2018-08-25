# -*- coding: utf-8 -*-

# importações necessarias
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# função para gerar dicionario de informações
def gerarDicionario(arq):
    # declarando variaveis
    a, b = [],[]
    dic = {}
    
    for t in range(11):
        # criando array dividido por espaços
        a.append(arq.readline().split())

    # excluindo primeira linha desnecessaria
    a.pop(0)

    for u in a:
        # criando array dividindo os iféns
        b.append(u[0].split('-'))
        b.append(u[1].split('-'))

    for key, value in b:
        # gerando um dicionario de chave e valor
        dic[key] = value

    # retornando dicionario gerado
    return dic


# função para gerar pdf
def gerarPdf(dic):
    pdf = 'Lista de Contatos.pdf'
    c = canvas.Canvas(pdf)
    # titulo do pdf
    c.drawString(100,780, "Lista de Contatos")

    a1 = 750
    for key, value in dic.items():
        nomeTel = '{}: {}'.format(str(key), str(value))
        c.drawString(100, a1, nomeTel)
        a1-= 15

    # salvando pdf
    c.save()

    # retornando pdf gerado
    return pdf

# função para enviar email
def enviarEmail():
    # email emissor
    fromaddr = "Email emissor"
    # email receptor
    toaddr = "Email receptor"
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Assunto"
     
    body = "Corpo do email"
     
    msg.attach(MIMEText(body, 'plain'))

    # nome do anexo a ser enviado
    filename = "Lista de Contatos.pdf"
    attachment = open(filename, "rb")
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # senha do email emissor
    server.login(fromaddr, "Senha do emissor")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


# variavel recebe dados do arquivo .txt
arquivo = open('Contatos.txt','r')

# variavel recebendo dicionario gerado
dic = gerarDicionario(arquivo)

# gerando pdf
gerarPdf(dic)

# enviar email com o arquivo em pdf
enviarEmail()
