#!/usr/bin/env python
#Imports
import pika
import sys
import os
import locale
####################### Parte visual apenas #######################
def exibir_menu():
    print("Menu:")
    print("1. Tempo")
    print("2. Status")
    print("3. Alerta")
    print("4. Erro")
    print("5. Finalizar")

def exibir_tempo_tipos():
    print("Tempo:")
    print("1. Pre Lancamento")
    print("2. Desacoplar Propulsor 1")
    print("3. Ativar Propulsor 2")
    print("4. Desligar Propulsor 2")
    print("5. Retornar para tipos de notificacao")

def exibir_status_tipos():
    print("Status:")
    print("1. Analise de Dados do Voo")
    print("2. Avaliacao de Sucesso de Voo")
    print("3. Retornar para tipos de notificacao")  
####################### Fim Parte visual #######################

#funcao para envio de mensagem, utilizando a estrategia de topicos
def enviar_mensagem(chave, mensagem):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    routing_key = chave if len(chave) > 2 else 'anonymous.info'
    message = mensagem
    channel.basic_publish(
        exchange='topic_logs', routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()

#funcao principal
def main():
    #Mensagem inicial, marcando inicio do lançamento
    #enviar_mensagem("tempo.prelancamento","Iniciando Processo de Lancamento. Contagem regressiva de 30s")
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        #Esse match com os IFs horrorosos basicos são para direcionar as mensagens
        #As escolhas definem o tipo de mensagem a ser enviado, nesse caso, a routing_key e a mensagem em si.
        match opcao:
            case "1":
                os.system('cls') # Limpando a tela
                exibir_tempo_tipos()
                opcaoTempo = input("Relatar notificacao de que tipo de evento: ")
                if opcaoTempo == "1":
                    enviar_mensagem("tempo.prelancamento",input("Informe a mensagem: "))
                elif opcaoTempo == "2":
                    enviar_mensagem("tempo.propulsor1","Desacoplando primeiro propulsor")
                elif opcaoTempo == "3":
                    enviar_mensagem("tempo.ativaPropulsor2","Ativando segundo propulsor")
                elif opcaoTempo == "4":
                    enviar_mensagem("tempo.DesligaPropulsor2","Desativando segundo Propulsor")
                elif opcaoTempo == "5":
                    pass
                else:
                    print("Opção inválida. Tente novamente.")
            case "2":
                os.system('cls') # Limpando a tela
                exibir_status_tipos()
                opcaoStatus = input("Relatar notificacao de que tipo de evento: ")
                if opcaoStatus == "1":
                    enviar_mensagem("status.analisedadosvoo",input("Descreva a analise do voo: "))
                elif opcaoStatus == "2":
                    enviar_mensagem("status.avaliacaosucesso",input("Avalie o sucesso do voo: "))
                elif opcaoStatus == "3":
                    pass
                else:
                    print("Opção inválida. Tente novamente.")
            case "3":
                os.system('cls') # Limpando a tela
                enviar_mensagem("alerta.anomalias",input("Alerta! Descreva a anomalia encontrada: "))
            case "4":
                os.system('cls') # Limpando a tela
                enviar_mensagem("erro.avarias",input("Erro! Descreva as avarias encontradas: "))
            case "5":
                os.system('cls') # Limpando a tela
                sys.exit()
            case _:
                print("Opção inválida. Tente novamente.")
        os.system('cls') # Limpando a tela

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    main()