
def ligar(id_device):
    print(id_device + " ligado!")

def desligar(id_device):
    print(id_device + " desligado!")

def alerta(id_device, msg, var=None):
    if var is None:
        print(id_device + " recebeu o alerta:\n")
        print(msg)
    else:
        print(id_device + " recebeu o alerta:\n")
        print(msg + " " + str(var))

# Variáveis extraídas da seção dispositivos
sistema = "sistema"  # ID_DEVICE
ativo = 0  # ID_OBS
luz = "luz"  # ID_DEVICE
estado = 0  # ID_OBS

# Comandos executados em ordem
ativo = True
estado = False
if ativo == True:
    ligar(sistema)
if estado != True:
    ligar(luz)
else:
    desligar(luz)
