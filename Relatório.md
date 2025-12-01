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

$ID\_OBS →$ ```^[a-zA-Z][a-zA-Z0-9]{0,99}$```

$AND →$ ```^AND$```





*Obs.: Para simplificações na aplicação usamos expressões regulares em algumas regras da gramática escritas em Regex*

### 1.1. Mudanças na Gramática
$CMD\_SEC$ foi trocado na primeira regra por $CMD\_LIST$ uma vez que $CMD\_SEC$ tinha apenas uma regra que o equivalava a $CMD\_LIST$. Logo, foi feita uma simples substituição.

Todas as regras a partir de (incluindo) $NUM$ são novas regras que definem os terminais das variáveis, operadores lógicos, etc. Para descrever as expressões utiliza-se Regex.

## 2. Funcionamento do Analisador

### 2.1. Leitura do arquivo
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

### 2.2. Analisador léxico

Para a análise léxica primeiramente definimos a lista de tokens que será usada:

```
tokens = (
    'DISPOSITIVOS', 'FIMDISPOSITIVOS', 'DEF', 'QUANDO', 'SENAO', 'AND', 'EXECUTE', 'EM', 'ALERTA_PARA', 'DIFUNDIR', 'LIGAR', 'DESLIGAR', 'TRUE', 'FALSE', 'ID', 'ID_OBS', 'NUM', 'MSG', 'PT_VIRG', 'DOIS_PONTOS', 'IGUAL', 'SETINHA', 'VIRGULA', 'ABRE_COL', 'FECHA_COL', 'OP_NE', 'OP_EQ', 'OP_GT', 'OP_LT', 'OP_GE', 'OP_LE'
)
```

Então definimos as palavras reservadas como constam na gramática. Como na própria gramática já 
são definidos os regex de cada expressão, nao será explicada cada expressão.

A parte mais importante deste analisador é que, realisando alguns testes, foi percebido
que ele reconhecia qualquer `ID` como `ID_DEVICE`, quando poderia ser, na realidade, `ID_OBS`
também. Ou seja, não é possível para o lexer diferenciar entre os dois `ID`s; este discernimento
deve ser feito na parte da análise sintática posteriormente.

De resto, o importante foram alguns testes feitos para *fine-tune* o analisador léxico
para não permitir operadores de tamanho maior que 1, variáveis (IDs) começados em número,
etc.

Caso o analisador léxico encontre alguma inconsistência o programa é abortado
e o arquivo compilado em python não é escrito.

### 2.3. Analisador Sintático

#### 2.3.1. Lista de Dispositivos

A funcionalidade mais elementar da linguagem ObsAct é a criação dos devices
e suas respectivas variáveis (`ID_OBS`). Para a análise sintática desta parte
apenas precisamos nos ater às seguintes regras:

$PROGRAM → DEV\_SEC \;\; CMD\_LIST$

$DEV\_SEC → dispositivos : DEV\_LIST \; fimdispositivos$

$DEV\_LIST → DEVICE \;\; DEV\_LIST \;|\; DEVICE$

$DEVICE → ID\_DEVICE \;|\; ID\_DEVICE \; [ID\_OBS]$

$ID\_DEVICE →$ ```^[a-zA-Z]{1,100}$```

$ID\_OBS →$ ```^[a-zA-Z][a-zA-Z0-9]{0,99}$```

Para a criação da aplicação (inicialmente apenas desta parte criamos as regras):

```
def p_program(p):
    '''program : DEV_SEC'''
    p[0] = p[1]

def p_dev_sec(p):
    'DEV_SEC : DISPOSITIVOS DOIS_PONTOS DEV_LIST FIMDISPOSITIVOS'
    p[0] = p[3]
    print("Dicionário de variáveis encontradas:")
    print(symbol_table)

def p_dev_list(p):
    '''DEV_LIST : DEVICE DEV_LIST
                | DEVICE'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_device(p):
    '''DEVICE : ID_DEVICE
              | ID_DEVICE ABRE_COL ID_OBS FECHA_COL'''
    if len(p) == 2:
        # Apenas ID_DEVICE
        symbol_table[p[1]] = 'ID_DEVICE'
        p[0] = ('device', p[1])
    else:
        # ID_DEVICE com ID_OBS
        symbol_table[p[1]] = 'ID_DEVICE'
        symbol_table[p[3]] = 'ID_OBS'
        p[0] = ('device_with_obs', p[1], p[3])

def p_id_device(p):
    'ID_DEVICE : ID'
    p[0] = p[1]

def p_id_obs(p):
    'ID_OBS : ID'
    p[0] = p[1]
```

Além de uma regra de erro que captura qualquer inconsistência e aborta o 
programa. 

Por padrão o compilador inicializa todas as variáveis (definidas na seção de
dispositivos) como variáveis em python com o nome correspondente e tendo
como valor atribuido uma string com o próprio nome (que pode ser alterado
posteriormente sem complicações, pois python não é estaticamente tipado).

```
for var_name, var_type in symbol_table.items():
    codigo_python += f'{var_name} = "{var_name}"  # {var_type}\n'
```

#### 2.3.2. Comandos

