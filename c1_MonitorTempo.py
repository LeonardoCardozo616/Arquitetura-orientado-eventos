#!/usr/bin/env python
import pika
import sys
import locale
#funcao básico do rabbitmq para receber mensagens baseado em topicos
locale.setlocale(locale.LC_ALL, 'pt-BR.UTF-8')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

#aqui define que a routing key dessa 'estacao de controle e monitoramento' vai ser qualquer assunto relacionado
#ao topico TEMPO
binding_key = "tempo.*" # <--
channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()