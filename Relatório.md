# Trabalho Final - INF1022
*Analisador Sintático da Linguagem ObsAct*

*Guilherme Melo Gratz | 2211068*

## 1. Gramática
A gramática que foi fornecida no exercício foi:

$$
PROGRAM → DEV_SEC CMD_SEC

DEV_SEC ➡ *dispositivos :* DEV_LIST *fimdispositivos*
$$

DEV_LIST ➡ DEV ICE DEV LIST | DEV ICE

DEV ICE ➡ ID DEV ICE

DEV ICE ➡ ID DEV ICE [ID OBS]

CM D SEC ➡ CM D LIST

CM D LIST ➡ CM D; CM D LIST | CM D;

CM D ➡ AT T RIB | OBSACT | ACT

AT T RIB ➡ def ID OBS = V AL

OBSACT ➡ quando OBS : ACT

OBSACT ➡ quando OBS : ACT senao ACT

OBS ➡ ID OBS OP LOGIC V AL

OBS ➡ ID OBS OP LOGIC V AL AN D OBS

V AL ➡ N U M | BOOL

ACT ➡ execute ACT ION em ID DEV ICE

ACT ➡ alerta para ID DEV ICE : M SG

ACT ➡ alerta para ID DEV ICE : M SG , ID OBS

ACT ➡ dif undir : M SG − > [DEV LIST N ]

ACT ➡ dif undir : M SG ID OBS − > [DEV LIST N ]

ACT ION ➡ ligar | desligar

DEV LIST N ➡ ID DEV ICE | ID DEV ICE , DEV LIST N

