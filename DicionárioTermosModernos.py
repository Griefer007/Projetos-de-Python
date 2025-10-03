import time
meme_dict = {
            "CRINGE": "Algo vergonhoso ou constrangedor.",
            "STALKEAR": "Investigar a vida de alguém online.",
            "67": "Palavra que não tem significado comum, mas pode ser considerada com afirmação."
            }
while True:
    word = input("Digite uma palavra moderna que você não entende (escreva todo a palavra em letras maiúsculas): ")
    if word in meme_dict.keys():
        print(meme_dict[word])
        time.sleep(5)
        print('Pesquise outra palavra! :,)')
        time.sleep(2)
        print(' ')
    else:
        print('Não achamos sua palavra... :,(')
        time.sleep(3)
        print(' ')
        stop = input('Quer parar de pesquisar? (Digite tudo maiúsculo)')
        if stop == 'SIM':
            print('Parando...')
            break
        else:
            print('Se digitou não (ou qualquer outra coisa), por favor continue a sua pesquisa!')
            time.sleep(2)
