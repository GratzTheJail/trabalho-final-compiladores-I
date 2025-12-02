
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
Lampada = "Lampada"  # ID_DEVICE
potencia = 0  # ID_OBS
Celular = "Celular"  # ID_DEVICE
bateria = 0  # ID_OBS
Pc = "Pc"  # ID_DEVICE

# Comandos executados em ordem
desligar(Pc)
potencia = 100
ligar(Lampada)
bateria = 2
alerta(Lampada, "Esta escuro")
alerta(Pc, "Celular com bateria ", bateria)
alerta(Celular, "Bateria criticamente baixa")
alerta(Pc, "Bateria criticamente baixa")
alerta(Lampada, "Bateria criticamente baixa")
alerta(Pc, "Bateria em ", bateria)
alerta(Lampada, "Bateria em ", bateria)
