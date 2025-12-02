
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
status = 0  # ID_OBS
sensorA = "sensorA"  # ID_DEVICE
valorA = 0  # ID_OBS
sensorB = "sensorB"  # ID_DEVICE
valorB = 0  # ID_OBS

# Comandos executados em ordem
valorA = 100
valorB = 50
status = True
if valorA > 80 and valorB < 60 and status == True:
    ligar(sistema)
if valorA <= 80 and valorB >= 60:
    desligar(sistema)
else:
    alerta(sensorA, "Condicao nao atendida")
