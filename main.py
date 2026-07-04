#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait, StopWatch

class SeguidorDeLinha:
    def __init__(self):
        # Inicialização do Hardware
        self.ev3 = EV3Brick()
        self.motor_dir = Motor(Port.A, Direction.CLOCKWISE)
        self.motor_esq = Motor(Port.D, Direction.CLOCKWISE)
        self.sensor_cor = ColorSensor(Port.S1)
        
        # Constantes do PID (Ajuste esses valores de acordo com a sua pista)
        self.kp = 12.0
        self.ki = 1.0
        self.kd = 116.0
        
        # Variáveis de Controle e Dinâmica
        self.offset = 30           # Valor padrão, será atualizado na calibração
        self.tp_maximo = 300       # Velocidade alvo nas retas
        self.fator_frenagem = 4.0  # O quanto ele freia nas curvas (quanto maior, mais ele freia)
        self.vel_minima = 100      # Velocidade mínima para não travar na curva

    def calibrar(self):
        """
        Lê a cor branca e a cor preta da pista usando os botões do EV3
        para calcular o ponto de equilíbrio (offset) perfeito.
        """
        self.ev3.screen.clear()
        self.ev3.screen.print("Coloque no BRANCO")
        self.ev3.screen.print("e aperte um botao")
        while not any(self.ev3.buttons.pressed()):
            pass
        wait(500)
        branco = self.sensor_cor.reflection()
        self.ev3.speaker.beep(600, 100)
        
        self.ev3.screen.clear()
        self.ev3.screen.print("Coloque no PRETO")
        self.ev3.screen.print("e aperte um botao")
        while not any(self.ev3.buttons.pressed()):
            pass
        wait(500)
        preto = self.sensor_cor.reflection()
        self.ev3.speaker.beep(600, 100)
        
        # Calcula o meio termo exato entre a linha e o fundo
        self.offset = (branco + preto) / 2
        
        self.ev3.screen.clear()
        self.ev3.screen.print("Calibrado!")
        self.ev3.screen.print("Offset:", self.offset)
        wait(2000)

    def iniciar_pid(self):
        """
        Inicia o loop contínuo de navegação autônoma usando o controle PID.
        """
        timer = StopWatch()
        integral = 0.0
        lasterror = 0.0
        
        self.ev3.screen.clear()
        self.ev3.screen.print("Rodando PID...")
        self.ev3.speaker.beep(1000, 300)
        
        # Reseta o cronômetro logo antes de começar a andar
        timer.reset()
        
        while True:
            # 1. Leitura do Sensor e do Tempo (dt)
            light_value = self.sensor_cor.reflection()
            dt = timer.time()
            timer.reset()
            
            # 2. Cálculo do Erro
            error = light_value - self.offset
            
            # 3. Integral (com limite de Anti-Windup para evitar acúmulo excessivo)
            integral += error
            if integral > 50: 
                integral = 50
            elif integral < -50: 
                integral = -50
            
            # 4. Derivada (Calculada com base no tempo real decorrido)
            if dt > 0:
                derivative = (error - lasterror) / dt
            else:
                derivative = 0.0
                
            # 5. Fórmula Clássica do PID (Somando os componentes)
            turn = (self.kp * error) + (self.ki * integral) + (self.kd * derivative)
            
            # 6. Velocidade Dinâmica (Acelera na reta, freia na curva)
            # Usa o valor absoluto do erro para reduzir a velocidade base
            tp = self.tp_maximo - (abs(error) * self.fator_frenagem)
            
            # Garante que o robô não ande para trás ou pare completamente ao tentar ir para frente
            if tp < self.vel_minima:
                tp = self.vel_minima
            
            # 7. Aplicação da força nos motores
            self.motor_dir.run(tp - turn)
            self.motor_esq.run(tp + turn)
            
            # 8. Salva o erro atual para ser o 'erro passado' do próximo ciclo
            lasterror = error

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    # Cria o objeto do robô
    robo = SeguidorDeLinha()
    
    # 1. Realiza a calibração manual
    robo.calibrar()
    
    # 2. Inicia o trajeto
    robo.iniciar_pid()