
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
Termometro = "Termometro"  # ID_DEVICE
temperatura = 0  # ID_OBS
Ventilador = "Ventilador"  # ID_DEVICE
status = 0  # ID_OBS

# Comandos executados em ordem
status = True
