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

$OBS → OBSCOND$

$OBS → OBSCOND \;\;AND\;\; OBS$

$OBSCOND → ID\_OBS \;\;OPLOGIC \;\;VAL$

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

Outra mudança significativa foi a mudança de `OBS` para separar a parte condicional da parte com `AND` para tratar melhor a recursão.

## 2. Funcionamento do Analisador

### 2.1. Leitura do arquivo
O analisador (analisador.py) quando rodado lê do terminal o nome do arquivo .obsact a ser lido e então gera um arquivo **.py** correspondente (compilado) de mesmo nome. No início de cada arquivo são definidas as funções padrão da linguagem.

```python
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

```python
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

Antes de entender as regras específicas da linguagem aqui aplicadas, precisamos entender como lidamos com erros: Caso o sistema encontre algum erro (seja léxico, seja sintático) ele aborta. Como o intuito do programa é ser apenas um compilador esta funcionalidade tem razão de ser; ao encontrar algum erro não se deve escrever nada no arquivo de saída. 

#### **2.3.1. Lista de Dispositivos**

A funcionalidade mais elementar da linguagem ObsAct é a criação dos devices
e suas respectivas variáveis (`ID_OBS`). Para a análise sintática desta parte
apenas precisamos nos ater às seguintes regras:

$PROGRAM → DEV\_SEC \;\; CMD\_LIST$

$DEV\_SEC → dispositivos : DEV\_LIST \; fimdispositivos$

$DEV\_LIST → DEVICE \;\; DEV\_LIST \;|\; DEVICE$

$DEVICE → ID\_DEVICE \;|\; ID\_DEVICE \; [ID\_OBS]$

$ID\_DEVICE →$ ```^[a-zA-Z]{1,100}$```

$ID\_OBS →$ ```^[a-zA-Z][a-zA-Z0-9]{0,99}$```

Para a criação da aplicação (inicialmente apenas desta parte criamos as regras, note que a gramática está incompleta por enquanto e será completada posteriormente):

```python
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
        # ID_DEVICE com ID_OBSos componentes
        symbol_table[p[1]] = 'ID_DEVICE'
        symbol_table[p[3]] = 'ID_OBS'
        p[0] = ('device_with_obs', p[1], p[3])

def p_id_device(p):
    ...

def p_id_obs(p):
    ...
```

Além de uma regra de erro que captura qualquer inconsistência e aborta o 
programa. 

Para garantir a consistência de ambos os tipos de `ID`, tanto `ID_OBS` quanto `ID_DEVICE`, foram adicionados verificações adicionais nas funções próprias. `ID_DEVICE`, por exemplo, não pode conter números, e esta verificação é feita. (Além é claro de que, como não podem ser palavras reservadas é necessário realizar também esta verificação.)

```python
def p_id_device(p):
    'ID_DEVICE : ID'
    # Verifica se é uma palavra reservada
    reserved_words = [...]
    if p[1] in reserved_words:
        print(f"ERRO semântico: '{p[1]}' é uma palavra reservada, não pode ser nome de dispositivo")
        ...
    # Verifica se contém apenas letras (a-z, A-Z)
    elif not p[1].isalpha():
        print(f"ERRO semântico: '{p[1]}' não é um nome de dispositivo válido (deve conter apenas letras, sem números)")
        ...
    # Verifica se o comprimento está entre 1 e 100 caracteres
    elif len(p[1]) < 1 or len(p[1]) > 100:
        print(f"ERRO semântico: '{p[1]}' tem comprimento inválido ({len(p[1])}). Deve ter entre 1 e 100 caracteres.")
        ...
    else:
        p[0] = p[1]

def p_id_obs(p):
    'ID_OBS : ID'
    # Verifica se é uma palavra reservada
    reserved_words = [...]
    if p[1] in reserved_words:
        print(f"ERRO semântico: '{p[1]}' é uma palavra reservada, não pode ser nome de observável")
        ...
    else:
        p[0] = p[1]
```



Por padrão o compilador inicializa todas as variáveis (definidas na seção de
dispositivos) como variáveis em python com o nome correspondente e tendo
como valor atribuido uma string com o próprio nome (que pode ser alterado
posteriormente sem complicações, pois python não é estaticamente tipado).

```python
for var_name, var_type in symbol_table.items():
    codigo_python += f'{var_name} = "{var_name}"  # {var_type}\n'
```

#### **2.3.2. Comandos**

**2.3.2.1. Atribuição**

Para o comando de atribuição foram adicionadas algumas regras. (Por enquanto a gramática está incompleta, pois só foi aplicado o comando de atribuição).

```python
def p_cmd_list(p):
    '''CMD_LIST : CMD PT_VIRG CMD_LIST
                | CMD PT_VIRG'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_cmd(p):
    '''CMD : ATTRIB'''
    p[0] = p[1]

def p_attrib(p):
    'ATTRIB : DEF ID_OBS IGUAL VAL'
    # Verifica se o ID_OBS foi declarado na seção de dispositivos
    id_name = p[2]
    if id_name and id_name in symbol_table and symbol_table[id_name] == 'ID_OBS':
        assignments.append((id_name, p[4]))
        p[0] = ('attrib', id_name, p[4])
        print(f"Atribuição válida: {id_name} = {p[4]}")
    else:
        if id_name:
            if id_name not in symbol_table:
                print(f"ERRO semântico: '{id_name}' não foi declarado")
            elif symbol_table[id_name] != 'ID_OBS':
                print(f"ERRO semântico: '{id_name}' não é um observável (é {symbol_table[id_name]})")
            print("Arquivo .py NÃO gerado devido a erros na análise!")
            sys.exit(1)
        p[0] = None

def p_val(p):
    '''VAL : NUM
           | BOOL'''
    p[0] = p[1]

def p_bool(p):
    '''BOOL : TRUE
            | FALSE'''
    p[0] = p[1] == 'True'  # Converte para valor booleano Python
```

Para fazer alguma atribuição é checado se o símbolo consta no dicionário existente de símbolos e se é `ID_OBS`. As atribuições são salvas em uma lista correspondente (`assignments = []`). Esta lógica será posteriormente reformulada para abarcar outros possíveis comandos.

As atribuições são então escritas após as definições da seção de dispositivos. Para garantir que as variáveis `ID_OBS` são sempre iguais a 0 quando não há atribuição como foi pedido elas são sempre inicializadas como sendo iguais a zero e posteriormente, se houver atribuição, seu valor é mudado como consta nela.

```python
# Adiciona as declarações de variáveis para cada símbolo encontrado
        for var_name, var_type in symbol_table.items():
            if var_name:
                if var_type == 'ID_DEVICE':
                    codigo_python += f'{var_name} = "{var_name}"  # {var_type}\n'
                elif var_type == 'ID_OBS':
                    # Inicializa ID_OBS com 0 por padrão
                    codigo_python += f'{var_name} = 0  # {var_type}\n'

        codigo_python += '\n# Atribuições da seção de comandos\n'
        # Adiciona as atribuições encontradas
        for var_name, value in assignments:
            if var_name and var_name in symbol_table:
                value_str = str(value)
                codigo_python += f'{var_name} = {value_str}\n'
```

Como o próprio parser garante que os números e os booleanos sejam escritos corretamente (também como são escritos em python), não há necessidade de qualquer conversão deste tipo.

**2.3.2.2. Ação**

Para expandir a linguagem com comandos de ação, foram implementadas as regras correspondentes aos comandos `ACT`, conforme definido na gramática. Esses comandos permitem realizar ações sobre dispositivos, como ligar/desligar, enviar alertas e difundir mensagens.

Para permitir a execução de comandos na ordem em que aparecem no arquivo fonte, a estrutura de dados foi modificada: em vez de uma lista separada apenas para atribuições (`assignments`), agora utiliza-se uma lista única de comandos (`commands`) que armazena tanto atribuições (`ATTRIB`) quanto ações (`ACT`).

```python
commands = []  # Lista que armazena todos os comandos na ordem em que aparecem
```

A regra `p_cmd` foi atualizada para aceitar ambos os tipos:

```python
def p_cmd(p):
    '''CMD : ATTRIB
           | ACT'''
    p[0] = p[1]
    commands.append(p[1])  # Adiciona à lista de comandos
```

**Tipos de Ações**

Foram implementadas as seguintes ações, conforme a gramática:

**a) Execute**

Comando para ligar ou desligar um dispositivo.


$ACT → execute \; ACTION\; em\; ID\_DEVICE$

$ACTION → ligar | desligar$


Regra correspondente:

```python
def p_act_execute(p):
    'ACT : EXECUTE ACTION EM ID_DEVICE'
    if p[4] not in symbol_table or symbol_table[p[4]] != 'ID_DEVICE':
        print(f"ERRO semântico: '{p[4]}' não é um dispositivo declarado")
        ...
    p[0] = ('execute', p[2], p[4])
```

**b) Alerta**

Comando para enviar uma mensagem a um dispositivo, opcionalmente incluindo um observável:


$ACT → alerta\; para\; ID\_DEVICE : MSG$

$ACT → alerta\; para\; ID\_DEVICE : MSG ,\; ID\_OBS$


O token composto `ALERTA_PARA` foi separado em dois tokens individuais (`ALERTA` e `PARA`) para maior robustez e evitar conflitos no analisador léxico.

Regras correspondentes:

```python
def p_act_alerta_simples(p):
    'ACT : ALERTA PARA ID_DEVICE DOIS_PONTOS MSG'
    if p[3] not in symbol_table or symbol_table[p[3]] != 'ID_DEVICE':
        print(f"ERRO semântico: '{p[3]}' não é um dispositivo declarado")
        ...
    p[0] = ('alerta_simples', p[3], p[5])  # dispositivo, mensagem

def p_act_alerta_com_var(p):
    'ACT : ALERTA PARA ID_DEVICE DOIS_PONTOS MSG VIRGULA ID_OBS'
    if p[3] not in symbol_table or symbol_table[p[3]] != 'ID_DEVICE':
        print(f"ERRO semântico: '{p[3]}' não é um dispositivo declarado")
        ...
    if p[7] not in symbol_table or symbol_table[p[7]] != 'ID_OBS':
        print(f"ERRO semântico: '{p[7]}' não é um observável declarado")
        ...
    p[0] = ('alerta_com_var', p[3], p[5], p[7])  # dispositivo, mensagem, observável
```

#### **c) Difundir**
Comando para enviar uma mensagem a uma lista de dispositivos:


$ACT → difundir : MSG\; -> [DEV\_LIST\_N]$

$ACT → difundir : MSG \;\;ID\_OBS \;-> [DEV\_LIST\_N]$


Regras correspondentes:

```python
def p_act_difundir_simples(p):
    'ACT : DIFUNDIR DOIS_PONTOS MSG SETINHA ABRE_COL DEV_LIST_N FECHA_COL'
    p[0] = ('difundir_simples', p[3], p[6])  # mensagem, lista de dispositivos

def p_act_difundir_com_var(p):
    'ACT : DIFUNDIR DOIS_PONTOS MSG ID_OBS SETINHA ABRE_COL DEV_LIST_N FECHA_COL'
    if p[4] not in symbol_table or symbol_table[p[4]] != 'ID_OBS':
        print(f"ERRO semântico: '{p[4]}' não é um observável declarado")
        ...
    p[0] = ('difundir_com_var', p[3], p[4], p[7])  # mensagem, observável, lista de dispositivos
```

Também foi aplicada a regra para processar listas de dispositivos nos comandos de difusão:

```python
def p_dev_list_n(p):
    '''DEV_LIST_N : ID_DEVICE
                  | ID_DEVICE VIRGULA DEV_LIST_N'''
    if len(p) == 2:
        if p[1] not in symbol_table or symbol_table[p[1]] != 'ID_DEVICE':
            print(f"ERRO semântico: '{p[1]}' não é um dispositivo declarado")
            ...
        p[0] = [p[1]]
    else:
        if p[1] not in symbol_table or symbol_table[p[1]] != 'ID_DEVICE':
            print(f"ERRO semântico: '{p[1]}' não é um dispositivo declarado")
            ...
        p[0] = [p[1]] + p[3]
```

Cada tipo de ação é traduzido para chamadas das funções Python definidas no início do arquivo gerado:

```python
# Processar todos os comandos na ordem em que apareceram
for cmd in commands:
    cmd_type = cmd[0]
    
    if cmd_type == 'attrib':
        # Atribuição (já existente)
        ...
        
    elif cmd_type == 'execute':
        action, device = cmd[1], cmd[2]
        codigo_python += f'{action}({device})\n'
        
    elif cmd_type == 'alerta_simples':
        device, msg = cmd[1], cmd[2]
        codigo_python += f'alerta({device}, "{msg}")\n'
        
    elif cmd_type == 'alerta_com_var':
        device, msg, var = cmd[1], cmd[2], cmd[3]
        codigo_python += f'alerta({device}, "{msg}", {var})\n'
        
    elif cmd_type == 'difundir_simples':
        msg, device_list = cmd[1], cmd[2]
        for device in device_list:
            codigo_python += f'alerta({device}, "{msg}")\n'
            
    elif cmd_type == 'difundir_com_var':
        msg, var, device_list = cmd[1], cmd[2], cmd[3]
        for device in device_list:
            codigo_python += f'alerta({device}, "{msg}", {var})\n'
```

Todas as ações incluem verificações semânticas para garantir que

1. Dispositivos referenciados estejam declarados na seção `DEV_SEC`
2. Observáveis referenciados estejam declarados (se aplicável)
3. Tipos corretos: que um identificador usado como `ID_DEVICE` realmente seja um dispositivo, e não um observável, e vice-versa

Qualquer violação resulta em erro e aborta a geração do arquivo Python.

#### **2.3.2.3. Comandos Condicionais (OBSACT)**

Para completar a linguagem ObsAct, foram implementados os comandos condicionais `OBSACT`, que permitem executar ações com base em condições sobre observáveis. Esses comandos correspondem a estruturas condicionais `if-else` em Python.

A gramática para os comandos condicionais foi estruturada para evitar recursão infinita e ambiguidade.

$OBSACT → quando \;OBS : ACT$

$OBSACT → quando \;OBS : ACT \;senao \;ACT$

$OBS → OBS\_COND$

$OBS → OBS\_COND \;AND\;\; OBS$

$OBS\_COND → ID\_OBS\;\; OPLOGIC \;\;VAL$

$OPLOGIC → \;!= | == | > | < | >= | <=$


Introduzimos um não-terminal intermediário `OBS_COND` para representar uma condição atômica (uma única comparação). A regra para `OBS` foi reestruturada para permitir múltiplas condições conectadas por `AND` sem causar recursão infinita. E por fim, criamos uma regra específica para operadores lógicos, mapeando para os tokens correspondentes.

As regras de produção correspondentes foram implementadas no analisador sintático:

```python
# ---------- OPLOGIC ----------
def p_oplogic(p):
    '''OPLOGIC : OP_NE
               | OP_EQ
               | OP_GT
               | OP_LT
               | OP_GE
               | OP_LE'''
    p[0] = p[1]

def p_obsact_single(p):
    'OBSACT : QUANDO OBS DOIS_PONTOS ACT'
    p[0] = ('obsact', p[2], p[4])

def p_obsact_else(p):
    'OBSACT : QUANDO OBS DOIS_PONTOS ACT SENAO ACT'
    p[0] = ('obsact_else', p[2], p[4], p[6])

def p_obs_single(p):
    'OBS : OBS_COND'
    p[0] = p[1]

def p_obs_with_and(p):
    'OBS : OBS_COND AND OBS'
    p[0] = ('obs_and', p[1], p[3])

def p_obs_cond(p):
    'OBS_COND : ID_OBS OPLOGIC VAL'
    id_name = p[1]
    if id_name not in symbol_table or symbol_table[id_name] != 'ID_OBS':
        print(f"ERRO semântico: '{id_name}' não é um observável declarado")
        ...
    p[0] = ('obs_cond', id_name, p[2], p[3])
```

Assim como nos comandos anteriores, o parser verifica se os observáveis usados nas condições foram declarados na seção de dispositivos. As condições com múltiplos `AND` são representadas como uma árvore, onde cada nó é uma condição atômica (`OBS_COND`) ou uma combinação de condições (`obs_and`).

Para converter as estruturas condicionais em código Python, foram implementadas funções auxiliares:

```python
def obs_to_string(obs):
    if obs[0] == 'obs_cond':
        id_name, op, val = obs[1], obs[2], obs[3]
        val_str = str(val)
        return f"{id_name} {op} {val_str}"
    elif obs[0] == 'obs_and':
        left, right = obs[1], obs[2]
        return f"{obs_to_string(left)} and {obs_to_string(right)}"

def generate_command_code(cmd, indent_level=0):
    indent = ' ' * 4 * indent_level
    lines = []
    cmd_type = cmd[0]

    # ... (código para outros tipos de comandos)

    elif cmd_type == 'obsact':
        cond = obs_to_string(cmd[1])
        act_code = generate_command_code(cmd[2], indent_level + 1)
        lines.append(f'{indent}if {cond}:')
        lines.append(act_code)

    elif cmd_type == 'obsact_else':
        cond = obs_to_string(cmd[1])
        act1_code = generate_command_code(cmd[2], indent_level + 1)
        act2_code = generate_command_code(cmd[3], indent_level + 1)
        lines.append(f'{indent}if {cond}:')
        lines.append(act1_code)
        lines.append(f'{indent}else:')
        lines.append(act2_code)

    return '\n'.join(lines)
```

**`obs_to_string`**: Converte a estrutura interna de uma condição em uma string Python válida. Para condições simples, gera `id op valor`; para condições compostas, recursivamente combina as partes com `and`.

 **`generate_command_code`**: Gera código Python com indentação apropriada. Para comandos condicionais, gera estruturas `if` ou `if-else` com o bloco de ação apropriadamente indentado.

Os comandos condicionais são traduzidos para estruturas condicionais em Python pleo esquema:

- **`quando condição : ação`** → `if condição: ação`
- **`quando condição : ação1 senao ação2`** → `if condição: ação1 else: ação2`

Conforme especificado, os comandos `OBSACT` são executados na ordem em que aparecem no arquivo fonte. A gramática não permite aninhamento de condicionais (um `if-else` dentro de outro), mas permite múltiplos blocos condicionais sequenciais:

O analisador realiza várias verificações para garantir a correção dos comandos condicionais.
Qualquer violação resulta em uma mensagem de erro clara e aborta a geração do arquivo Python.

### 2.4. Integração Completa

Com a implementação dos comandos condicionais, a linguagem ObsAct agora suporta todas as funcionalidades especificadas:

1. **Declaração de Dispositivos e Observáveis**
2. **Atribuição de Valores a Observáveis**
3. **Ações sobre Dispositivos** (ligar/desligar, alertas, difusão)
4. **Controle Condicional** baseado em valores de observáveis

O analisador mantém a ordem de execução dos comandos, permitindo misturar atribuições, ações e condicionais em qualquer sequência. Todas as verificações léxicas, sintáticas e semânticas são realizadas, garantindo a geração de código Python correto e executável.

## 3. Testes



## 4. Conclusão

O analisador desenvolvido implementa completamente a linguagem ObsAct, convertendo programas .obsact em código Python executável. Como foi possível perceber, a implementação das diferentes funcionalidades da linguagem foi gradual, mantendo a clareza do código e a robustez das verificações.

O sistema demonstra os princípios fundamentais de construção de compiladores, desde a análise léxica até a geração de código, aplicados a uma linguagem de domínio específico para controle de dispositivos.