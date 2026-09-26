print("======login====")

nametag1 = input("Escreva seu nome de usuario:")
Senha1 = input("Digite sua senha:")

print("====Verificação====")

nametag2 = input("Escreva seu nome de usuario:")
Senha2 = input("Digite sua senha:")

while nametag1 != nametag2 or Senha1 != Senha2:
    print("[ERRO] senha ou dados incorretos")
  
    nametag2 = input("Escreva seu nome de usuario:")
  
    Senha2 = input("Digite sua senha:")
  
if nametag1 == nametag2 and Senha1 == Senha2: 
    print("seja bem vindo")