
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
movimento = 0  # ID_OBS
Higrometro = "Higrometro"  # ID_DEVICE
umidade = 0  # ID_OBS
Lampada = "Lampada"  # ID_DEVICE
potencia = 0  # ID_OBS

# Comandos executados em ordem
potencia = 100
if umidade < 40:
    alerta(Monitor, " Ar seco detectado ")
if movimento == True:
    ligar(Lampada)
else:
    desligar(Lampada)
