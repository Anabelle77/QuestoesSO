import threading #importa o módulo de threads pra rodar as tarefas simultaneamente
import time #função de tempo 
import random #usado nesse código para gerar os tempos aleatoriamente

compilador = threading.Semaphore(1)  #semáforo que permite apenas 1 thread por vez (só um exclusivo compilando) 
banco_dados = threading.Semaphore(2) #semáforo que permite até 2 threads (2 podem acessar o BD simultaneamente)
print_lock = threading.Lock() #evitar que threads imprimam ao mesmo tempo

class Programador(threading.Thread): #define a classe Programador herdando de threading.Thread
    def __init__(self, id): #método construtor, self, id = parametros do construtor
        super().__init__() #chama o construtor __init__() da classse mãe threading.Thread
        self.id = id
    
    def pensando(self): #método do momento que o programador está pensando
        with print_lock:
            print(f"Programador {self.id} está pensando...")
        time.sleep(random.uniform(0, 2)) #dorme por um tempo aleatorio, tempo que pensa
    
    def compilando(self): #método do momento que o programador está compilando
        with print_lock:
            print(f"Programador {self.id} está compilando.")
        time.sleep(random.uniform(1, 3)) 
        with print_lock:
            print(f"Programador {self.id} terminou de compilar.")
    
    def run(self): #método  principal da thread, o que executa no start()
        time.sleep(random.uniform(0, 3))
        while True: #loop infinito
            self.pensando()
            
            with print_lock:
                print(f"Programador {self.id} quer trabalhar...")
                time.sleep(random.uniform(0, 2))
            
            banco_dados.acquire() #tenta pegar permissão de acesso ao BD, se já tem 2 programadores, thread bloqueia
            with print_lock:
                print(f"Programador {self.id} acessou o banco de dados.")
                time.sleep(random.uniform(1, 3))
            
            compilador.acquire() #tenta pegar o compilador e se já tiver um programador compilando, bloqueia
            with print_lock:
                print(f"Programador {self.id} pegou o compilador.")
                time.sleep(random.uniform(1, 3))
            
            self.compilando()
            
            compilador.release() #programador libera o compilador então outro pode pegar
            with print_lock:
                print(f"Programador {self.id} liberou o compilador.")
            
            banco_dados.release() #vaga liberada ao BD
            with print_lock:
                print(f"Programador {self.id} saiu do banco de dados.")

#criar e iniciar os programadores
programadores = [Programador(i) for i in range(1, 6)]
for p in programadores:
    p.start()