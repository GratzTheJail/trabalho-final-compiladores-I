import os
import sys
import ply.lex as lex
import ply.yacc as yacc

## ---------- LEITURA DO ARQUIVO --------

# Solicita o nome do arquivo .obsact
nome_arquivo = input("Digite o nome do arquivo .obsact (sem a extensão): ")

nome_arquivo += '.obsact'

# Verifica se o arquivo existe
if not os.path.exists(nome_arquivo):
    print("Erro: Arquivo não encontrado!")
    exit()

# Gera o nome do arquivo .py
nome_py = nome_arquivo.replace('.obsact', '.py')

## ---------- ANÁLISE LÉXICA --------
tokens = (
    'DISPOSITIVOS',
    'FIMDISPOSITIVOS',
    'DEF',
    'QUANDO',
    'SENAO',
    'AND',
    'EXECUTE',
    'EM',
    'ALERTA',
    'PARA',
    'DIFUNDIR',
    'LIGAR',
    'DESLIGAR',
    'TRUE',
    'FALSE',
    'ID',
    'NUM',
    'MSG',
    'PT_VIRG',
    'DOIS_PONTOS',
    'IGUAL',
    'SETINHA',
    'VIRGULA',
    'ABRE_COL',
    'FECHA_COL',
    'OP_NE',
    'OP_EQ',
    'OP_GT',
    'OP_LT',
    'OP_GE',
    'OP_LE'
)

lexical_error_occurred = False

def t_INVALID_OP(t):
    r'={3,}|!={2,}|>{2,}|<{2,}|={1,2}[^=\s]|[^!><=]=[^=\s]'
    print(f"ERRO léxico: operador inválido '{t.value}'")
    t.lexer.skip(len(t.value))
    
    global lexical_error_occurred
    lexical_error_occurred = True
    print("Arquivo .py NÃO gerado devido a erros na análise!")
    sys.exit(1)

# Operadores e símbolos
t_OP_NE = r'!='
t_OP_EQ = r'=='
t_OP_GT = r'>'
t_OP_LT = r'<'
t_OP_GE = r'>='
t_OP_LE = r'<='
t_PT_VIRG = r';'
t_DOIS_PONTOS = r':'
t_IGUAL = r'='
t_SETINHA = r'->'
t_VIRGULA = r','
t_ABRE_COL = r'\['
t_FECHA_COL = r'\]'

# Palavras reservadas
t_DISPOSITIVOS = r'dispositivos'
t_FIMDISPOSITIVOS = r'fimdispositivos'
t_DEF = r'def'
t_QUANDO = r'quando'
t_SENAO = r'senao'
t_AND = r'AND'
t_EXECUTE = r'execute'
t_EM = r'em'
t_ALERTA = r'alerta'
t_PARA = r'para'
t_DIFUNDIR = r'difundir'
t_LIGAR = r'ligar'
t_DESLIGAR = r'desligar'
t_TRUE = r'True'
t_FALSE = r'False'

def t_INVALID_ID(t):
    r'[0-9]+[a-zA-Z_][a-zA-Z0-9_]*'
    print(f"ERRO LÉXICO: token inválido '{t.value}' (números e letras sem separação)")
    t.lexer.skip(len(t.value))

    global lexical_error_occurred
    lexical_error_occurred = True
    print("Arquivo .py NÃO gerado devido a erros na análise!")
    sys.exit(1)

def t_MSG(t):
    r'\"[a-zA-Z0-9 ]{1,100}\"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

def t_NUM(t):
    r'0|[1-9][0-9]*'
    t.value = int(t.value)
    return t


# Como o lexer não diferencia entre ID_DEVICE e ID_OBS, usamos apenas um token ID genérico
# que será classificado corretamente posteriormente.
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]{0,99}'
    reserved = {
        'dispositivos': 'DISPOSITIVOS',
        'fimdispositivos': 'FIMDISPOSITIVOS',
        'def': 'DEF',
        'quando': 'QUANDO',
        'senao': 'SENAO',
        'AND': 'AND',
        'execute': 'EXECUTE',
        'em': 'EM',
        'alerta': 'ALERTA',
        'para': 'PARA',
        'difundir': 'DIFUNDIR',
        'ligar': 'LIGAR',
        'desligar': 'DESLIGAR',
        'True': 'TRUE',
        'False': 'FALSE'
    }
    if t.value in reserved:
        t.type = reserved[t.value]
    else:
        t.type = 'ID'
    return t

# Ignorar espaços em branco
t_ignore = ' \t\n'

def t_error(t):
    print(f"ERRO LÉXICO - Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

    global lexical_error_occurred
    lexical_error_occurred = True
    print("Arquivo .py NÃO gerado devido a erros na análise!")
    sys.exit(1)

lexer = lex.lex()








## --------- ANÁLISE SINTÁTICA ---------
# Dicionário para armazenar as variáveis encontradas
symbol_table = {}
# Lista para armazenar as atribuições encontradas
commands = []

syntax_error_occurred = False

## ---------- DEV_SEC --------

def p_program(p):
    '''program : DEV_SEC CMD_LIST'''
    p[0] = (p[1], p[2])
    print("Análise sintática completa concluída com sucesso!")

def p_program_empty(p):
    'program : '
    p[0] = (None, [])
    print("Arquivo vazio - análise sintática concluída com sucesso!")

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
    reserved_words = ['dispositivos', 'fimdispositivos', 'def', 'quando', 'senao', 
                     'AND', 'execute', 'em', 'alerta', 'para', 'difundir', 
                     'ligar', 'desligar', 'True', 'False']
    if p[1] in reserved_words:
        print(f"ERRO semântico: '{p[1]}' é uma palavra reservada, não pode ser nome de dispositivo")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        p[0] = None
        sys.exit(1)
    # Verifica se contém apenas letras (a-z, A-Z)
    elif not p[1].isalpha():
        print(f"ERRO semântico: '{p[1]}' não é um nome de dispositivo válido (deve conter apenas letras, sem números)")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        p[0] = None
        sys.exit(1)
    elif len(p[1]) < 1 or len(p[1]) > 100:
        print(f"ERRO semântico: '{p[1]}' tem comprimento inválido ({len(p[1])}). Deve ter entre 1 e 100 caracteres.")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        p[0] = None
        sys.exit(1)
    else:
        p[0] = p[1]

def p_id_obs(p):
    'ID_OBS : ID'
    reserved_words = ['dispositivos', 'fimdispositivos', 'def', 'quando', 'senao', 
                     'AND', 'execute', 'em', 'alerta', 'para', 'difundir', 
                     'ligar', 'desligar', 'True', 'False']
    if p[1] in reserved_words:
        print(f"ERRO semântico: '{p[1]}' é uma palavra reservada, não pode ser nome de observável")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        p[0] = None
        sys.exit(1)
    else:
        p[0] = p[1]


## ---------- CMD_LIST --------
def p_cmd_list(p):
    '''CMD_LIST : CMD PT_VIRG CMD_LIST
                | CMD PT_VIRG'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_cmd(p):
    '''CMD : ATTRIB
           | ACT
           | OBSACT'''
    p[0] = p[1]
    commands.append(p[1])


## ---------- ATTRIB --------
def p_attrib(p):
    'ATTRIB : DEF ID_OBS IGUAL VAL'
    # Verifica se o ID_OBS foi declarado na seção de dispositivos
    id_name = p[2]
    if id_name and id_name in symbol_table and symbol_table[id_name] == 'ID_OBS':
        # assignments.append((id_name, p[4]))
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

## ---------- ACT --------

def p_action(p):
    '''ACTION : LIGAR
              | DESLIGAR'''
    p[0] = p[1]

def p_act_execute(p):
    'ACT : EXECUTE ACTION EM ID_DEVICE'
    if p[4] not in symbol_table or symbol_table[p[4]] != 'ID_DEVICE':
        print(f"ERRO semântico: '{p[4]}' não é um dispositivo declarado")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        sys.exit(1)
    p[0] = ('execute', p[2], p[4])

def p_act_alerta_simples(p):
    'ACT : ALERTA PARA ID_DEVICE DOIS_PONTOS MSG'
    if p[3] not in symbol_table or symbol_table[p[3]] != 'ID_DEVICE':
        print(f"ERRO semântico: '{p[3]}' não é um dispositivo declarado")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        sys.exit(1)
    p[0] = ('alerta_simples', p[3], p[5])

def p_act_alerta_com_var(p):
    'ACT : ALERTA PARA ID_DEVICE DOIS_PONTOS MSG VIRGULA ID_OBS'
    if p[3] not in symbol_table or symbol_table[p[3]] != 'ID_DEVICE':
        print(f"ERRO semântico: '{p[3]}' não é um dispositivo declarado")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        sys.exit(1)
    if p[7] not in symbol_table or symbol_table[p[7]] != 'ID_OBS':
        print(f"ERRO semântico: '{p[7]}' não é um observável declarado")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        sys.exit(1)
    p[0] = ('alerta_com_var', p[3], p[5], p[7])

# Regra para ACT difundir sem ID_OBS
def p_act_difundir_simples(p):
    'ACT : DIFUNDIR DOIS_PONTOS MSG SETINHA ABRE_COL DEV_LIST_N FECHA_COL'
    p[0] = ('difundir_simples', p[3], p[6])

# Regra para ACT difundir com ID_OBS
def p_act_difundir_com_var(p):
    'ACT : DIFUNDIR DOIS_PONTOS MSG ID_OBS SETINHA ABRE_COL DEV_LIST_N FECHA_COL'
    if p[4] not in symbol_table or symbol_table[p[4]] != 'ID_OBS':
        print(f"ERRO semântico: '{p[4]}' não é um observável declarado")
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        sys.exit(1)
    p[0] = ('difundir_com_var', p[3], p[4], p[7])

# ---------- OBSACT ----------
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
        print("Arquivo .py NÃO gerado devido a erros na análise!")
        sys.exit(1)
    p[0] = ('obs_cond', id_name, p[2], p[3])

def p_dev_list_n(p):
    '''DEV_LIST_N : ID_DEVICE
                  | ID_DEVICE VIRGULA DEV_LIST_N'''
    if len(p) == 2:
        if p[1] not in symbol_table or symbol_table[p[1]] != 'ID_DEVICE':
            print(f"ERRO semântico: '{p[1]}' não é um dispositivo declarado")
            print("Arquivo .py NÃO gerado devido a erros na análise!")
            sys.exit(1)
        p[0] = [p[1]]
    else:
        if p[1] not in symbol_table or symbol_table[p[1]] != 'ID_DEVICE':
            print(f"ERRO semântico: '{p[1]}' não é um dispositivo declarado")
            print("Arquivo .py NÃO gerado devido a erros na análise!")
            sys.exit(1)
        p[0] = [p[1]] + p[3]

def p_error(p):
    global syntax_error_occurred
    syntax_error_occurred = True
    if p:
        print(f"ERRO de sintaxe na linha {p.lineno}: token inesperado '{p.value}'")
    else:
        print("ERRO de sintaxe: fim inesperado do arquivo")
    print("Arquivo .py NÃO gerado devido a erros na análise!")
    sys.exit(1)

parser = yacc.yacc()





## --------- FUNÇÕES AUXILIARES ---------
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

    if cmd_type == 'attrib':
        var_name, value = cmd[1], cmd[2]
        if isinstance(value, bool):
            value_str = str(value)
        else:
            value_str = str(value)
        lines.append(f'{indent}{var_name} = {value_str}')

    elif cmd_type == 'execute':
        action, device = cmd[1], cmd[2]
        lines.append(f'{indent}{action}({device})')

    elif cmd_type == 'alerta_simples':
        device, msg = cmd[1], cmd[2]
        lines.append(f'{indent}alerta({device}, "{msg}")')

    elif cmd_type == 'alerta_com_var':
        device, msg, var = cmd[1], cmd[2], cmd[3]
        lines.append(f'{indent}alerta({device}, "{msg}", {var})')

    elif cmd_type == 'difundir_simples':
        msg, device_list = cmd[1], cmd[2]
        for device in device_list:
            lines.append(f'{indent}alerta({device}, "{msg}")')

    elif cmd_type == 'difundir_com_var':
        msg, var, device_list = cmd[1], cmd[2], cmd[3]
        for device in device_list:
            lines.append(f'{indent}alerta({device}, "{msg}", {var})')

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




## --------- PROCESSAMENTO DO ARQUIVO .obsact ---------
# Lê o conteúdo do arquivo
with open(nome_arquivo, 'r', encoding='utf-8') as f:
    data = f.read()

symbol_table.clear()
commands.clear()

# Processa com o parser
try:
    result = parser.parse(data, lexer=lexer)

    if not syntax_error_occurred and not lexical_error_occurred and result:
        print("Análise sintática da seção DEV_SEC concluída com sucesso!")
        print("Dicionário de símbolos:", symbol_table)
        print("Comandos encontrados:", commands)


        ##  -------- GERAÇÃO DO ARQUIVO FINAL .PY --------
        # Código das funções em Python
        codigo_python = '''
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

# Variáveis extraídas da seção dispositivos
'''
        if symbol_table:
            # Adiciona as declarações de variáveis para cada símbolo encontrado
            for var_name, var_type in symbol_table.items():
                if var_name:
                    if var_type == 'ID_DEVICE':
                        codigo_python += f'{var_name} = "{var_name}"  # {var_type}\n'
                    elif var_type == 'ID_OBS':
                        codigo_python += f'{var_name} = 0  # {var_type}\n' # Inicializa ID_OBS com 0 por padrão
        else:
            codigo_python += '# Nenhum dispositivo declarado\n'
        
        
        codigo_python += '\n# Comandos executados em ordem\n'
        
        for cmd in commands:
            codigo_python += generate_command_code(cmd) + '\n'

        # Escreve o arquivo .py
        with open(nome_py, 'w', encoding='utf-8') as f:
            f.write(codigo_python)

        print(f"Arquivo {nome_py} gerado com sucesso!")

except Exception as e:
    print(f"ERRO durante a análise sintática: {e}")
    print("Arquivo .py NÃO gerado devido a erros na análise!")
    # Remove o arquivo .py se ele foi criado anteriormente
    if os.path.exists(nome_py):
        os.remove(nome_py)





































# # Função para testar o lexer
# def test_lexer(input_text):
#     print(f"Input: {input_text}")
#     lexer.input(input_text)
    
#     tokens = []
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break
#         tokens.append((tok.type, tok.value, tok.lineno))
    
#     print("Tokens encontrados:")
#     for token in tokens:
#         print(f"  Tipo: {token[0]}, Valor: {token[1]}, Linha: {token[2]}")
#     print("-" * 50)
#     return tokens

# # Testes
# # Teste 1: Declaração de dispositivos
# test_lexer("dispositivos: lampada ventilador fimdispositivos")

# # Teste 2: Definição de variável
# test_lexer("def temperatura = 25")

# # Teste 3: Comando quando-senao
# test_lexer("quando temperatura > 30 AND umidade < 60 execute ligar em ventilador senao execute desligar em ventilador")

# # Teste 4: Alertas
# test_lexer('alerta para lampada: "Temperatura alta" , temp_var')

# # Teste 5: Difusão
# test_lexer('difundir: "Alerta geral" -> [lampada, ventilador, sensor]')

# # Teste 6: Dispositivo com observável
# test_lexer("dispositivos: sensor[temp_sensor] fimdispositivos")

# # Teste 7: Operadores lógicos
# test_lexer("quando status == True execute ligar em lampada")
# test_lexer("quando valor != False execute desligar em dispositivo")
# test_lexer("quando x >= 10 AND y <= 5 execute ligar em lampada")

# # Teste 8: Números e mensagens
# test_lexer('def contador = 100 alerta para dispositivo: "Mensagem de teste 123"')

# # Teste 9: Casos complexos
# test_lexer('dispositivos: lampada sensor[temp] atuador fimdispositivos; def temp = 30; quando temp > 25 execute ligar em lampada; alerta para sensor: "Temperatura alta"')

# # Adicione este teste aos testes existentes
# test_lexer("def preço = 100")  # O 'ç' e 'º' são caracteres inválidos

# test_lexer("def valor = 0123")  # Números não podem começar com 0

# test_lexer('def x = 1; alerta para device: "Esta mensagem tem mais de cem caracteres o que viola a regra da gramática para mensagens pois precisa ser no maximo cem"')

# test_lexer("def 123var = 10")  # ID não pode começar com número

# test_lexer("quando x === 10 execute ligar em lampada")  # '===' não existe

# test_lexer("def var @ = 10; quando x & y execute ligar em lampada")

# # Operadores com múltiplos caracteres inválidos
# test_lexer("quando x ==== 10 execute ligar em lampada")
# test_lexer("quando x !! 5 execute desligar em lampada") 
# test_lexer("quando x >>= 3 execute ligar em lampada")
# test_lexer("quando x =!= 7 execute desligar em lampada")

# # IDs começando com números ou caracteres especiais
# test_lexer("def 99problemas = 99")
# test_lexer("def @var = 10")
# test_lexer("def var#name = 5")
# test_lexer("quando _var > 10 execute ligar em lampada")  # _var deve ser ID válido!

# # Números com zeros à esquerda ou formato inválido
# test_lexer("def valor = 0123")
# test_lexer("def valor = 0")
# test_lexer("def valor = 123abc")
# test_lexer("def valor = 12.34")  # ponto decimal não permitido

# # Mensagens com caracteres especiais ou formato errado
# test_lexer('alerta para lampada: "Mensagem com @caractere_especial!"')
# test_lexer("alerta para lampada: Mensagem_sem_aspas")
# test_lexer('alerta para lampada: "Mensagem com \\"aspas\\" internas"')  # escape não permitido

# # Tokens colados sem espaços
# test_lexer("defx=10")
# test_lexer("quandox>5executeligaremlampada")
# test_lexer("dispositivos:lampada fimdispositivos")

# # Caracteres não-ASCII
# test_lexer("def preço = 100")
# test_lexer("def número = 5")
# test_lexer('alerta para lampada: "Mensagem em português: ç á ã"')