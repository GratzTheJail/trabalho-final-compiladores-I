# Trabalho Final - INF1022
*Analisador Sintático da Linguagem ObsAct*

*Guilherme Melo Gratz | 2211068*

## 1. Gramática
A gramática que foi fornecida no exercício foi:

$PROGRAM → DEV\_SEC \;\; CMD\_SEC$

$DEV\_SEC → dispositivos : DEV\_LIST \; fimdispositivos$

$DEV\_LIST → DEVICE \;\; DEV\_LIST \;|\; DEVICE$

$DEVICE → ID\_DEVICE \;|\; ID\_DEVICE \; [ID\_OBS]$

$CMD\_SEC → CMD\_LIST$

$CMD\_LIST → CMD;\; CMD\_LIST \;|\; CM D;$

$CMD → ATTRIB \;|\; OBSACT \;|\; ACT$

$AT T RIB → def \; ID\_OBS = V AL$

$OBSACT → quando\; OBS : ACT$

$OBSACT → quando \;OBS : ACT\; senao \;ACT$

$OBS → ID\_OBS \;\;OPLOGIC \;\;VAL$

$OBS → ID\_OBS \;\;OPLOGIC \;\;V AL \;\;AN D\;\; OBS$

$V AL → N U M \;|\; BOOL$

$ACT → execute \;\;ACT ION\;\; em\;\; ID\_DEV ICE$

$ACT → alerta \;para \;\;ID\_DEV ICE : M SG$

$ACT → alerta \;para \;\;ID\_DEV ICE : M SG , ID\_OBS$

$ACT → dif undir : M SG \;−> [DEV\_LIST\_N ]$

$ACT → dif undir : M SG \;\;ID\_OBS \;− > [DEV\_LIST\_N ]$

$ACT ION → ligar \;|\; desligar$

$DEV\_LIST\_N → ID\_DEV ICE \;|\; ID\_DEV ICE ,\; DEV\_LIST\_N$

- Trocar CMD_SEC por CMD_LIST

- Adicionar regras para strings e nomes de variáveis (ER)

testeee