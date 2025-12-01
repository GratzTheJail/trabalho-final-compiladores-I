
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
temperatura = "temperatura"  # ID_OBS
Lampada = "Lampada"  # ID_DEVICE

# Prints das variáveis identificadas
print("Termometro - ID_DEVICE")
print("temperatura - ID_OBS")
print("Lampada - ID_DEVICE")
