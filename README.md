# SSH Jump Automation

## Description / Descrição

**English:**

A generic Python script to automate SSH command execution on remote devices through an intermediate jump host. Easily manage and configure multiple devices securely.

**Português:**

Um script genérico em Python para automatizar a execução de comandos SSH em dispositivos remotos através de um host intermediário. Gerencie e configure múltiplos dispositivos de forma segura e eficiente.

## Features / Funcionalidades

- **English:**
  - Connect to a remote device via a jump host.
  - Execute a list of SSH commands automatically.
  - Log all SSH session outputs.
  - Automatically accept unknown host fingerprints.

- **Português:**
  - Conectar-se a um dispositivo remoto via host intermediário.
  - Executar uma lista de comandos SSH automaticamente.
  - Registrar todas as saídas das sessões SSH.
  - Aceitar automaticamente fingerprints de hosts desconhecidos.

## Requirements / Requisitos

- **English:**
  - Python 3.x
  - Paramiko library

- **Português:**
  - Python 3.x
  - Biblioteca Paramiko

## Installation / Instalação

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SEU_USUARIO/ssh-jump-automation.git
   cd ssh-jump-automation
   ```

2. **Install the required Python library:**

   ```bash
   pip install paramiko
   ```

## Configuration

1. **Edit the script (`script.py`):**

   Update the following variables with your environment details:

   ```python
   # Host intermediário
   jump_host = "IP_DO_HOST_INTERMEDIARIO"
   jump_port = 22
   jump_username = "USUARIO_INTERMEDIARIO"
   jump_key_filename = "CAMINHO_PARA_SUA_CHAVE_PRIVADA.ppk"  # Se usar chave
   # jump_password = "SENHA_INTERMEDIARIO"  # Se usar senha

   # Dispositivo alvo
   device_host = "IP_DO_DISPOSITIVO_ALVO"
   device_username = "USUARIO_DISPOSITIVO"
   device_password = "SENHA_DISPOSITIVO"

   # Arquivo de comandos
   commands_file = "commands.txt"
   ```

2. **Prepare the `commands.txt` file:**

   Adicione os comandos SSH que você deseja executar no dispositivo alvo, um por linha. Exemplo:

   ```txt
   show version
   show interfaces
   exit
   ```

## Usage / Uso

**English:**

Run the script using Python:

```bash
python script.py
```

The script will:

1. Connect to the intermediate jump host via SSH.
2. Initiate an SSH session to the target device.
3. Execute the commands listed in `commands.txt`.
4. Log all outputs to `ssh_session.log`.

**Português:**

Execute o script usando Python:

```bash
python script.py
```

O script irá:

1. Conectar-se ao host intermediário via SSH.
2. Iniciar uma sessão SSH no dispositivo alvo.
3. Executar os comandos listados em `commands.txt`.
4. Registrar todas as saídas em `ssh_session.log`.

## Logging

**English:**

All SSH session outputs are logged in `ssh_session.log` for review and troubleshooting.

**Português:**

Todas as saídas das sessões SSH são registradas em `ssh_session.log` para revisão e solução de problemas.

## Security Considerations / Considerações de Segurança

**English:**

- **Credentials Management:** Ensure that your SSH credentials are stored securely. Avoid hardcoding sensitive information in scripts. Consider using environment variables or secure vaults.
- **Host Fingerprints:** Automatically accepting host fingerprints can pose security risks. Ensure you operate in a trusted network environment to prevent Man-in-the-Middle attacks.

**Português:**

- **Gerenciamento de Credenciais:** Certifique-se de que suas credenciais SSH estejam armazenadas de forma segura. Evite codificar informações sensíveis diretamente nos scripts. Considere usar variáveis de ambiente ou cofres de segurança.
- **Fingerprints de Hosts:** Aceitar automaticamente fingerprints de hosts pode representar riscos de segurança. Garanta que você opere em um ambiente de rede confiável para prevenir ataques Man-in-the-Middle.
