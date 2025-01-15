import paramiko
import time
import re
import logging

# ------------------------------------------------------------------------------
# Configurações de logging
# ------------------------------------------------------------------------------
logging.basicConfig(
    filename="ssh_session.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ------------------------------------------------------------------------------
# Configurações de conexão SSH
# ------------------------------------------------------------------------------
# Host intermediário (ex: uma VM ou um servidor "jump host")
jump_host = "IP_DO_HOST_INTERMEDIARIO"
jump_port = 22
jump_username = "USUARIO_INTERMEDIARIO"
jump_key_filename = (
    "CAMINHO_PARA_SUA_CHAVE_PRIVADA.ppk"  # se usar chave, caso contrário use password
)
# jump_password = "SENHA_INTERMEDIARIO"

# Dispositivo alvo (ex: roteador, switch, OLT, etc.)
device_host = "IP_DO_DISPOSITIVO_ALVO"
device_username = "USUARIO_DISPOSITIVO"
device_password = "SENHA_DISPOSITIVO"

# Arquivo de texto contendo os comandos que serão enviados ao dispositivo alvo
commands_file = "commands.txt"


# ------------------------------------------------------------------------------
# Função para criar a lista de comandos a partir de um arquivo
# ------------------------------------------------------------------------------
def read_commands_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        commands = file.readlines()
    return [command.strip() for command in commands]


# ------------------------------------------------------------------------------
# Função para registrar saída de comando nos logs
# ------------------------------------------------------------------------------
def log_output(output):
    """Registra a saída do dispositivo nos logs."""
    logging.info(output)


# ------------------------------------------------------------------------------
# Fluxo principal de execução
# ------------------------------------------------------------------------------
def main():
    # Leitura dos comandos a partir de um arquivo
    commands_list = read_commands_from_file(commands_file)

    print("Conectando ao host intermediário...")
    # Configurar cliente SSH para o host intermediário
    jump_ssh = paramiko.SSHClient()
    jump_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Caso use senha em vez de chave, substitua a linha de baixo por:
    # jump_ssh.connect(hostname=jump_host, port=jump_port, username=jump_username, password='SENHA_INTERMEDIARIO')
    jump_ssh.connect(
        hostname=jump_host,
        port=jump_port,
        username=jump_username,
        # password=jump_password,
        key_filename=jump_key_filename,
    )
    print("Conexão estabelecida com o host intermediário.")

    # Abrir um shell interativo para, a partir dele, conectar no dispositivo alvo
    print("Iniciando sessão shell para conectar ao dispositivo alvo...")
    device_shell = jump_ssh.invoke_shell()

    # Enviar comando de SSH para o dispositivo alvo
    ssh_command = f"ssh {device_username}@{device_host}\n"
    device_shell.send(ssh_command)

    # Aguardar a solicitação de senha ou confirmação do fingerprint
    while True:
        time.sleep(1)
        output = device_shell.recv(65535)
        output_str = output.decode("utf-8", errors="ignore")
        log_output(output_str)

        # Detectar solicitação de confirmação do fingerprint
        if "are you sure you want to continue connecting" in output_str.lower():
            print("Fingerprint desconhecido. Enviando confirmação 'yes'.")
            device_shell.send("yes\n")
            continue  # Continua o loop para aguardar a próxima solicitação

        # Detectar solicitação de senha
        if "password:" in output_str.lower():
            break

    # Enviar a senha do dispositivo
    device_shell.send(device_password + "\n")

    # Aguardar até que surja um prompt (ajuste a regex se necessário)
    # Exemplo: r'(?:\(.*\))?#' é utilizado para dispositivos que exibem "<algo>#"
    # Caso seu dispositivo seja diferente, adapte para o prompt esperado.
    while True:
        time.sleep(1)
        output = device_shell.recv(65535)
        output_str = output.decode("utf-8", errors="ignore")
        log_output(output_str)

        # Se o dispositivo exibir o prompt com "#", ">", "$" etc., ajuste a expressão
        if re.search(r"(?:\(.*\))?#", output_str) or re.search(r"[\$#>]\s*$", output_str):
            break

    print("Conexão bem-sucedida ao dispositivo alvo. Enviando comandos...")

    # Envia cada comando da lista
    for command in commands_list:
        print(f"Enviando comando: {command}")
        device_shell.send(command + "\n")

        # Captura a saída até encontrar o prompt novamente
        while True:
            time.sleep(1)
            output = device_shell.recv(65535)
            output_str = output.decode("utf-8", errors="ignore")
            log_output(output_str)

            # Se houver paginação tipo '--More--', envia espaço
            if "--More--" in output_str:
                device_shell.send(" ")
            # Se encontrar o prompt, segue para o próximo comando
            elif re.search(r"(?:\(.*\))?#", output_str) or re.search(r"[\$#>]\s*$", output_str):
                break

    print("Todos os comandos foram executados. Finalizando sessão...")

    # Exemplo de saída do dispositivo: se desejar enviar 'exit' ao final
    device_shell.send("exit\n")

    # Espera um pouco pela resposta antes de encerrar
    time.sleep(2)

    # Fecha a conexão com o host intermediário
    jump_ssh.close()
    print("Conexões fechadas com sucesso. Fim da execução.")


# ------------------------------------------------------------------------------
# Ponto de entrada do script
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
