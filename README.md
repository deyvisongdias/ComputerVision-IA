# Este repositorio e para codificação do trabalho pratico de inteligencia artificial

# Guia de Instalação e Execução no Linux

Este projeto utiliza Python e requer algumas dependências para ser executado corretamente no Linux. Siga as etapas abaixo para configurar o ambiente e rodar o código corretamente.

## Requisitos
- **Python 3** instalado no sistema. Para verificar a instalação, execute:
  ```sh
  python3 --version
  ```
  Se não estiver instalado, você pode instalá-lo com:
  ```sh
  sudo apt update
  sudo apt install python3 python3-venv python3-pip
  ```

- **Tkinter**: Este projeto utiliza a biblioteca Tkinter para interfaces gráficas. Instale-a com:
  ```sh
  sudo apt install python3-tk
  ```

## Configuração do Ambiente Virtual
Recomenda-se o uso de um ambiente virtual para gerenciar as dependências do projeto. Siga os passos abaixo:

1. **Criar o ambiente virtual:**
   ```sh
   python3 -m venv venv
   ```

2. **Ativar o ambiente virtual:**
   ```sh
   source venv/bin/activate
   ```

3. **Instalar as dependências:**
   ```sh
   pip install networkx matplotlib
   ```

4. **Verificar as bibliotecas instaladas:**
   ```sh
   pip list
   ```

5. **Desativar o ambiente virtual (opcional):**
   ```sh
   deactivate
   ```

## Executando o Programa no Linux
Para rodar o código, ative o ambiente virtual e execute o arquivo principal:
```sh
source venv/bin/activate
python3 app.py
```
Se desejar sair do ambiente virtual após a execução, utilize:
```sh
deactivate
```

## Observação
Se encontrar problemas de permissão ao executar os comandos, tente adicionar `sudo` antes do comando ou verificar se o Python e os pacotes estão corretamente configurados.

