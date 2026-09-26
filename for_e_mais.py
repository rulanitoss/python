lista_de_utilizadores = ["Ruan"]
print(" Sistema_de_cadastro ")
continuar = "sim"

while continuar == "sim":
  novo_nome = input ("Escreva o nome do utilizador para cadastrar: ")
  lista_de_utilizadores.append(novo_nome)
  print(f"SUCESSO {novo_nome} foi adcionado")
  
  continuar = input("Quer cadrastar mais alguem?(sim/nao): ).lower()")
  for usuario in lista_de_utilizadores:
    print(f"{usuario}")