import socket, os, sys 

PORT = 80
CODE_PAGE = 'uft-8'
BUFFER_SIZE = 4096

url = input('Digite a URL completa do arquivo: ')
if not url.startswith('http://'):
    url = 'http://' + url

slash_index = url.find('/', 7)
if slash_index == -1:
    sys.exit('URL inválida. Certifique-se de que está no formato correto.')

url_host = url[7:slash_index]
url_path = url[slash_index:]

def send_request(request, host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, PORT))
        sock.sendall(request.encode())
        response = b''
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            response += data
        return response

head_request = f"HEAD {url_path} HTTP/1.1\r\nHost: {url_host}\r\nConnection: close\r\n\r\n"
head_response = send_request(head_request, url_host)

try:
    header, _ = head_response.split(b'\r\n\r\n', 1)
except ValueError:
    sys.exit("Resposta do servidor está em um formato inesperado.")

content_length = None
for line in header.split(b'\r\n'):
    if line.lower().startswith(b'content-length:'):
        content_length = int(line.split(b': ')[1])
        break

if content_length is None:
    sys.exit("Não foi possível obter o tamanho do conteúdo.")

get_request = f"GET {url_path} HTTP/1.1\r\nHost: {url_host}\r\nConnection: close\r\n\r\n"
get_response = send_request(get_request, url_host)

try:
    _, file_data = get_response.split(b'\r\n\r\n', 1)
except ValueError:
    sys.exit("Resposta do servidor está em um formato inesperado.")

if b'200 OK' not in get_response:
    sys.exit(f"Falha ao baixar o arquivo. Resposta do servidor:\n{get_response.decode('utf-8')}")

while len(file_data) < content_length:
    data = send_request('', url_host)
    if not data:
        break
    file_data += data

file_name = os.path.basename(url_path)

with open(file_name, 'wb') as f:
    f.write(file_data)
print(f'Arquivo baixado e salvo como: {file_name}')
