
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
sala = "sala"  # ID_DEVICE
cozinha = "cozinha"  # ID_DEVICE
quarto = "quarto"  # ID_DEVICE
temperatura = 0  # ID_OBS
banheiro = "banheiro"  # ID_DEVICE

# Comandos executados em ordem
alerta(sala, "Alarme incendio")
alerta(cozinha, "Alarme incendio")
alerta(quarto, "Alarme incendio")
alerta(banheiro, "Alarme incendio")
alerta(sala, "Temperatura normal", temperatura)
alerta(quarto, "Temperatura normal", temperatura)
alerta(cozinha, "Mensagem individual")
