
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
termometro = "termometro"  # ID_DEVICE
temp = 0  # ID_OBS
higrometro = "higrometro"  # ID_DEVICE
hum = 0  # ID_OBS
ventoinha = "ventoinha"  # ID_DEVICE
luz = "luz"  # ID_DEVICE
sensorLuz = 0  # ID_OBS

# Comandos executados em ordem
temp = 22
hum = 45
sensorLuz = 300
if temp >= 25:
    ligar(ventoinha)
if sensorLuz < 200:
    ligar(luz)
alerta(termometro, "Temperatura: ", temp)
