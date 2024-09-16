import socket, sys

PORT        = 80
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 1024

host = input('\nInforme o nome do HOST ou URL do site: ')

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    tcp_socket.connect((host, PORT))
except:
    print(f'\nERRO.... {sys.exc_info()[0]}')
else:
    requisicao = f'HEAD / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\n\r\n'
    try:
        tcp_socket.sendall(requisicao.encode(CODE_PAGE))
    except:
        print(f'\nERRO.... {sys.exc_info()[0]}')
    else:
        resposta = tcp_socket.recv(BUFFER_SIZE).decode(CODE_PAGE)
        dic_head = {}
        linha = resposta.split('\r\n')
        for linha in linha[1:]:
            if ':' in linha:
                chave, valor = linha.split(': ', 1)
                dic_head[chave] = valor

        with open('dicionario_HEAD.txt', 'w') as file:
            for chave, valor in dic_head.items():
                file.write(f'{chave}: {valor}\n')
        
        with open('dicionario_HEAD.txt', 'r') as file:
            ler_arquivo = file.read()
            print(ler_arquivo)

    tcp_socket.close()