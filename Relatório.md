# Trabalho Final - INF1022
*Analisador Sintático da Linguagem ObsAct*

*Guilherme Melo Gratz | 2211068*

## 1. Gramática
A gramática que foi fornecida no exercício foi modificada para:

$PROGRAM → DEV\_SEC \;\; CMD\_LIST$

$DEV\_SEC → dispositivos : DEV\_LIST \; fimdispositivos$

$DEV\_LIST → DEVICE \;\; DEV\_LIST \;|\; DEVICE$

$DEVICE → ID\_DEVICE \;|\; ID\_DEVICE \; [ID\_OBS]$

$CMD\_LIST → CMD;\; CMD\_LIST \;|\; CM D;$

$CMD → ATTRIB \;|\; OBSACT \;|\; ACT$

$AT T RIB → def \; ID\_OBS = V AL$

$OBSACT → quando\; OBS : ACT$

$OBSACT → quando \;OBS : ACT\; senao \;ACT$

$OBS → ID\_OBS \;\;OPLOGIC \;\;VAL$

$OBS → ID\_OBS \;\;OPLOGIC \;\;V AL \;\;AND\;\; OBS$

$V AL → N U M \;|\; BOOL$

$ACT → execute \;\;ACT ION\;\; em\;\; ID\_DEV ICE$

$ACT → alerta \;para \;\;ID\_DEV ICE : M SG$

$ACT → alerta \;para \;\;ID\_DEV ICE : M SG , ID\_OBS$

$ACT → dif undir : M SG \;−> [DEV\_LIST\_N ]$

$ACT → dif undir : M SG \;\;ID\_OBS \;− > [DEV\_LIST\_N ]$

$ACT ION → ligar \;|\; desligar$

$DEV\_LIST\_N → ID\_DEV ICE \;|\; ID\_DEV ICE ,\; DEV\_LIST\_N$

$NUM →$ ```[1-9][0-9]*```

$BOOL → True\;|\;False$

$OPLOGIC → \;\;!=\;|\;==\;|\;>\;|\;<\;|\;>=\;|\;<=$

$MSG → \;$```"^[a-zA-Z0-9 ]{1,100}$"```

$ID\_DEVICE →$ ```^[a-zA-Z]{1,100}$```

$ID\_OBS →$ ```^[a-zA-Z_][a-zA-Z0-9_]{0,99}$```

$AND →$ ```^AND$```





*Obs.: Para simplificações na aplicação usamos expressões regulares em algumas regras da gramática escritas em Regex*

### 1.1. Mudanças na Gramática
1. $CMD\_SEC$ foi trocado na primeira regra por $CMD\_LIST$ uma vez que $CMD\_SEC$ tinha apenas uma regra que o equivalava a $CMD\_LIST$. Logo, foi feita uma simples substituição.

2. Todas as regras a partir de (incluindo) $NUM$ são novas regras que definem os terminais das variáveis, operadores lógicos, etc. Para descrever as expressões utiliza-se Regex.

## 2. Funcionamento do Analisador

O analisador (analisador.py) quando rodado lê do terminal o nome do arquivo .obsact a ser lido e então gera um arquivo **.py** correspondente (compilado) de mesmo nome. No início de cada arquivo são definidas as funções padrão da linguagem.

```
def ligar(id_device):
    print(id_device + " ligado!")

def desligar(id_device):
    print(id_device + " desligado!")

def alerta(id_device, msg, var=None):
    if var is None:
        print(id_device + " recebeu o alerta:\\n")
        print(msg)
    else:
        print(id_device + " recebeu o alerta:\\n")
        print(msg + " " + str(var))
```

