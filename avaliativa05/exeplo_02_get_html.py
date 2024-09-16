import socket, sys

PORT        = 80
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 4096

def obter_tamanho_conteudo(cabecalho):
    for linha in cabecalho.split('\r\n'):
        if linha.lower().startswith('content-length'):
            return int(linha.split(': ')[1])
    return 0

host = input('\nInforme o nome do HOST ou URL do site: ')

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    tcp_socket.connect((host, PORT))
except:
    print(f'\nERRO.... {sys.exc_info()[0]}')
else:
    tcp_socket.settimeout(10)
    requisicao = f'GET / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\n\r\n'
    try:
        tcp_socket.sendall(requisicao.encode(CODE_PAGE))
    except:
        print(f'\nERRO.... {sys.exc_info()[0]}')
    else:
        print('-'*50)
        resposta_completa = ""

        while True:
            try:
                resposta = tcp_socket.recv(BUFFER_SIZE).decode(CODE_PAGE)
                resposta_completa += resposta
                if not resposta_completa:
                    break
            except socket.timeout:
                print('\nERRO... A operação de recepçao excedeu o tempo limite.')
                break

            cabecalho, _, conteudo_inicial = resposta_completa.partition('\r\n\r\n')

            tamanho_conteudo = obter_tamanho_conteudo(cabecalho)
            conteudo_completo = conteudo_inicial
            conteudo_recebido = len(conteudo_inicial)

            while conteudo_recebido < tamanho_conteudo:
                try:
                    resposta = tcp_socket.recv(BUFFER_SIZE).decode(CODE_PAGE)
                    conteudo_completo += resposta
                    conteudo_recebido += len(resposta)
                except socket.timeout:
                    print('\nERRO... A operação de recepçao excedeu o tempo limite.')
                    break

            with open('output.html', 'w') as f:
                salvo = f.write(conteudo_completo)

        print(resposta_completa)
        print('-'*50)
    tcp_socket.close()