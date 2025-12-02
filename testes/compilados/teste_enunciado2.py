
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
Monitor = "Monitor"  # ID_DEVICE
Celular = "Celular"  # ID_DEVICE
Termometro = "Termometro"  # ID_DEVICE
temperatura = 0  # ID_OBS

# Comandos executados em ordem
if temperatura > 30:
    alerta(Monitor, " Temperatura em ", temperatura)
    alerta(Celular, " Temperatura em ", temperatura)
