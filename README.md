# EV3 Advanced PID Line Follower

Um sistema de navegação autônoma para robôs seguidores de linha utilizando o bloco LEGO Mindstorms EV3 e a biblioteca Pybricks (MicroPython). Este projeto implementa um controlador PID (Proporcional-Integral-Derivativo) otimizado com cálculo de tempo real ($dt$), frenagem dinâmica em curvas e sistema *anti-windup*.

## Funcionalidades

* **Controle PID no Domínio do Tempo:** O termo derivativo é calculado utilizando o tempo real de cada ciclo de processamento (`StopWatch`), evitando instabilidades causadas por gargalos de processamento.
* **Velocidade Dinâmica (Frenagem Adaptativa):** O robô ajusta sua velocidade linear com base no erro atual. Ele acelera em retas e reduz a velocidade automaticamente em curvas acentuadas, garantindo que não saia da pista.
* **Calibração Interativa:** Rotina de inicialização guiada pela tela do EV3 para ler os valores exatos de reflexão de luz do ambiente (branco e preto), calculando o `offset` (ponto de equilíbrio) de forma autônoma.
* **Proteção Anti-Windup:** Limite imposto ao acúmulo da variável integral para evitar que o robô faça correções agressivas ou descontrole após longos períodos fora da linha.
* **Arquitetura Orientada a Objetos:** Código estruturado em classes para fácil manutenção, escalabilidade e parametrização.

## Hardware Necessário

* 1x Bloco LEGO Mindstorms EV3
* 2x Motores Grandes (Tração)
* 1x Sensor de Cor EV3
* Cabos de conexão

**Mapeamento de Portas:**
* **Porta A:** Motor Direito
* **Porta D:** Motor Esquerdo
* **Porta S1:** Sensor de Cor (virado para o chão)

## Software Necessário

* [Pybricks MicroPython](https://pybricks.com/) instalado no EV3 (via cartão MicroSD).
* Visual Studio Code com a extensão do EV3 MicroPython (ou interface web do Pybricks).

## Como Executar

1. Monte o robô com os motores e o sensor de cor nas portas especificadas.
2. Transfira o código `main.py` para o bloco EV3.
3. Ao iniciar o programa, siga as instruções na tela do bloco:
   * Posicione o sensor sobre a parte **BRANCA** da pista e pressione qualquer botão no EV3.
   * Posicione o sensor sobre a linha **PRETA** da pista e pressione qualquer botão no EV3.
4. O robô calculará o *offset* ideal, emitirá um bipe duplo e começará a seguir a linha automaticamente utilizando o algoritmo PID.

## Ajuste de Parâmetros (Tuning)
Para adaptar o robô a diferentes pistas ou modelos físicos, edite as seguintes variáveis no método `__init__` da classe `SeguidorDeLinha`:
* `self.kp`, `self.ki`, `self.kd`: Constantes de sintonia do controlador PID.
* `self.tp_maximo`: Velocidade base nas retas (ex: 300).
* `self.fator_frenagem`: O quanto a velocidade é reduzida proporcionalmente ao erro em curvas.