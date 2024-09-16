import socket, os, sys

# a) o programa deverá solicitar a URL completa de uma imagem na WEB
url = input('Digite a URL completa do arquivo: ') #seja pdf ou mp3 ou imagem
if not url.startswith('http://'):
    url = 'http://' + url

slash_index = url.find('/', 7)
if slash_index == -1:
    sys.exit('URL inválida. Certifique-se de que está no formato correto.')

url_host = url[7:slash_index]
url_img = url[slash_index:]

# b) A partir da URL, separar a parte correspondente ao HOST da parte correspondente ao IMAGE
url_request = f"GET {url_img} HTTP/1.1\r\nHost: {url_host}\r\nConnection: close\r\n\r\n"

HOST_PORT = 80
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 4096

def obter_tamanho_conteudo(cabecalho):
    for linha in cabecalho.split('\r\n'):
        if linha.lower().startswith('content-length'):
            return int(linha.split(': ')[1])
    return 0

sock_img = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_img.connect((url_host, HOST_PORT))
sock_img.sendall(url_request.encode())

response = b''
while True:
    data = sock_img.recv(BUFFER_SIZE)
    if not data:
        break
    response += data

sock_img.close()

header, image_data = response.split(b'\r\n\r\n', 1)

if b'200 OK' not in header:
    sys.exit(f"Falha ao baixar o arquivo. Resposta do servidor:\n{header.decode(CODE_PAGE)}")

# Controlar o download do conteúdo da resposta com base no tamanho informado no
# HEADER
content_length = None
for line in header.split(b'\r\n'):
    if b'Content-Length:' in line:
        content_length = int(line.split(b' ')[1])
        break

if content_length is None:
    sys.exit("Não foi possível obter o tamanho do conteúdo.")

while len(image_data) < content_length:
    data = sock_img.recv(BUFFER_SIZE)
    if not data:
        break
    image_data += data

sock_img.close()

# c) Obter o nome do arquivo da imagem a partir da URL informada
file_name = os.path.basename(url_img)

# d) Efetuar o download da imagem na mesma pasta do programa, salvando-a com o mesmo nome que ela possui na URL.
with open(file_name, 'wb') as f:
    f.write(image_data)
print(f'Imagem baixada e salva como: {file_name}')