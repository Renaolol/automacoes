import random
from time import sleep
class Personagens:
    def __init__(self,nome:str):
        self.nome = nome
        self.lvl = 1
        self.vida = 100
        self.exp = 0
        self.prox_lvl = 100
        self.exp_kill = self.lvl*50
        self.dano=self.lvl*5
        self.defesa=self.lvl * 2

    def attack(self,mult):
        return int(self.dano*mult)
    
    def calc_vida(self,dano):
        self.vida = self.vida - ((dano-self.defesa) if dano >= self.defesa else 0)

    def calcula_exp(self,xp_kill):
        self.exp = self.exp + xp_kill
        self.lvl += 1 if self.exp >= self.prox_lvl else 0
        self.dano += self.dano if self.exp >= self.prox_lvl else 0
        #Prox level precisa ser o último
        self.prox_lvl += self.prox_lvl if self.exp >= self.prox_lvl else 0
        
x = Personagens("Renan")
for z in range(100):
    y = Personagens("Goblin")
    print("--------- Nova Rodada ---------")
    print(f"---- rodada {z}")
    while y.vida > 0:
        multiplicador = random.randrange(1,7)
        dano = x.attack(multiplicador)
        print(f'o dano de ataque foi {dano} (Dano base de ataque {x.dano}) e o multiplicador de dano foi {multiplicador}')   
        print(f'Vida do {y.nome}: {y.vida}, Defesa do {y.nome}:{y.defesa}')
        y.calc_vida(dano)
        print(f"Nova vida de {y.nome} = {y.vida}")
        if y.vida <=0:
            x.calcula_exp(y.exp_kill)
            print(f'{x.nome}, está no level {x.lvl}, atualmente com {x.exp} e para o próx level é necessário {x.prox_lvl} e o dano é {x.dano}')
