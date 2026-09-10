class Temporizador:
    def __init__(self, tiempoTotal):
        self.tiempoTotal = tiempoTotal

        #Ajustes configurables desde Ajustes -> Temporizador
        self.pararTemporizadorAlAcabar = True
        self.alarma = False
        self.volumenAlarma = 50  # en porcentaje (0-100)
        self.randomizarImagenesAlAcabar = False

        #Estado en tiempo real
        self.tiempoRestante = tiempoTotal
        self.contando = False

    def play(self):
        self.contando = True

    def pausa(self):
        self.contando = False

    def avanzarUnSegundo(self):
        if not self.contando or self.tiempoRestante <= 0:
            return False

        self.tiempoRestante -= 1

        if self.tiempoRestante <= 0:
            self.contando = False
            return True

        return False

    def reiniciar(self, respetarSwitchPausa=False):
        self.tiempoRestante = self.tiempoTotal
        if respetarSwitchPausa:
            self.contando = not self.pararTemporizadorAlAcabar
        else:
            self.contando = False

    def tiempoFormateado(self):
        minutos, segundos = divmod(max(self.tiempoRestante, 0), 60)
        return f"{minutos:02d}:{segundos:02d}"