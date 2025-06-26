import threading
import random
import time

canal_ocupado_por = []
canal_lock = threading.Lock()

class Transmissor(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.tentativas = 0

    def run(self):
        global canal_ocupado_por

        while self.tentativas < 10:
            print(f"[{self.id}] Verificando o meio...")
            time.sleep(0.02)  # Curto tempo de "sensing"

            # ETAPA 1: Verifica o canal (SEM LOCK) — proposital
            if len(canal_ocupado_por) == 0:
                print(f"[{self.id}] Meio parece livre, id [{self.id}] tentando transmitir...")
            else:
                print(f"[{self.id}] Meio ocupado, aplicando backoff...")
                self.backoff()
                continue

            # ETAPA 2: Agora tenta entrar no canal (com lock, simula competição)
            with canal_lock:
                canal_ocupado_por.append(self.id)

            # Simula tempo de transmissão (tempo para permitir que outros entrem também)
            time.sleep(0.2)

            with canal_lock:
                if len(canal_ocupado_por) > 1:
                    print(f"[{self.id}] !!! Colisão detectada com transmissores {canal_ocupado_por}!")
                    self.send_jam_signal()
                    self.backoff()
                else:
                    print(f"[{self.id}] --- Transmissão concluída com sucesso.")

                canal_ocupado_por.clear()

            break  # Sucesso ou colisão tratada

            
    def send_jam_signal(self):
        print(f"[{self.id}] === Enviando jam signal...")

    def backoff(self):
        self.tentativas += 1
        k = min(self.tentativas, 10)
        r = random.randint(0, 2**k - 1)
        espera = r * 0.05
        print(f"[{self.id}] *** Backoff: esperando {espera:.2f} segundos.")
        time.sleep(espera)

# Criando e iniciando os transmissores quase ao mesmo tempo
transmissores = [Transmissor(i) for i in range(1, 6)]

for t in transmissores:
        t.start()
        time.sleep(0.00001)  # Pequeno intervalo entre inícios, aumenta chance de colisão

for t in transmissores:
        t.join()