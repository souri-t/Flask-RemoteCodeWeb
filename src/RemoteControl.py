import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html

# RemoteControl Class
class RemoteControl:
    
    def __init__(self, outGpioPort):
        self.GPIO = outGpioPort
        self.FREQ = 38.0
        self.GAP_MS = 100
        self.GAP_S = self.GAP_MS  / 1000.0

    """
    Generate carrier square wave.
    """
    def __carrier(self, gpio, frequency, micros):
        wf = []
        cycle = 1000.0 / frequency
        cycles = int(round(micros/cycle))
        on = int(round(cycle / 2.0))
        sofar = 0
        for c in range(cycles):
            target = int(round((c+1)*cycle))
            sofar += on
            off = target - sofar
            sofar += off
            wf.append(pigpio.pulse(1<<gpio, 0, on))
            wf.append(pigpio.pulse(0, 1<<gpio, off))
        return wf

    """
    Send IR wave
    """
    def send(self, codes):
        pi = pigpio.pi() # Connect to Pi.

        if not pi.connected:
            exit(0)

        try:

            # Create wave
            emit_time = time.time()
            marks_wid = {}
            spaces_wid = {}

            wave = [0]*len(codes)

            for i in range(0, len(codes)):
                ci = int(codes[i])
                if i & 1: # Space
                    if ci not in spaces_wid:
                        pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                        spaces_wid[ci] = pi.wave_create()
                    wave[i] = spaces_wid[ci]
                else: # Mark
                    if ci not in marks_wid:
                        wf = self.__carrier(self.GPIO, self.FREQ, ci)
                        pi.wave_add_generic(wf)
                        marks_wid[ci] = pi.wave_create()
                    wave[i] = marks_wid[ci]

            delay = emit_time - time.time()

            if delay > 0.0:
                time.sleep(delay)

            pi.wave_chain(wave)

            while pi.wave_tx_busy():
                time.sleep(0.002)

            emit_time = time.time() + self.GAP_S

            for i in marks_wid:
                pi.wave_delete(marks_wid[i])

            marks_wid = {}

            for i in spaces_wid:
                pi.wave_delete(spaces_wid[i])

            spaces_wid = {}
            
            return True

        except Exception as e:
            print('catch Exception:', e)
            return False

        finally:
            if pi.connected:
                pi.stop() # Disconnect from Pi.
