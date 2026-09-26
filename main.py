print("Tente advinhar o numero entre 1-100")
import random
numero=random.randint(1,100)
palpite=0

while palpite != numero :
    
    palpite = int(input("palpite:"))

    
    if(palpite > numero):
        print("tente um numero menor")
    if(palpite < numero):
        print("tente um numero maior")
    if(palpite == numero):
        print("Você acertou!!!")

