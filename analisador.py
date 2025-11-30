import os

# Solicita o nome do arquivo .obsact
nome_arquivo = input("Digite o nome do arquivo .obsact (sem a extensão): ")

nome_arquivo += '.obsact'

# Verifica se o arquivo existe
if not os.path.exists(nome_arquivo):
    print("Erro: Arquivo não encontrado!")
    exit()

# Gera o nome do arquivo .py
nome_py = nome_arquivo.replace('.obsact', '.py')

# Código das funções em Python
codigo_python = '''def ligar(id_device):
    print(id_device + " ligado!")

def desligar(id_device):
    print(id_device + " desligado!")

def alerta(id_device, msg, var=None):
    if var is None:
        print(id_device + " recebeu o alerta:\\n")
        print(msg)
    else:
        print(id_device + " recebeu o alerta:\\n")
        print(msg + " " + str(var))
'''

# Escreve o arquivo .py
with open(nome_py, 'w', encoding='utf-8') as f:
    f.write(codigo_python)

print(f"Arquivo {nome_py} gerado com sucesso!")