
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
lampada = "lampada"  # ID_DEVICE
sensor = "sensor"  # ID_DEVICE
temperatura = 0  # ID_OBS
arcondicionado = "arcondicionado"  # ID_DEVICE
atuador = "atuador"  # ID_DEVICE
umidade = 0  # ID_OBS

# Comandos executados em ordem
temperatura = 25
umidade = 60
if temperatura > 30 and umidade < 70:
    ligar(arcondicionado)
else:
    desligar(arcondicionado)
alerta(lampada, "Temperatura atual", temperatura)
alerta(lampada, "Alerta geral", umidade)
alerta(sensor, "Alerta geral", umidade)
alerta(arcondicionado, "Alerta geral", umidade)
ligar(lampada)
alerta(sensor, "Sistema ativo")
alerta(lampada, "Mensagem sem variavel")
alerta(arcondicionado, "Mensagem sem variavel")
