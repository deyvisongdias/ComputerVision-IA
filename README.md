# Este repositorio e para codificação do trabalho pratico de inteligencia artificial



## Guia de Instalação e Execução no Linux

### Requisitos
- **Python 3**: É necessário ter o Python 3 instalado no sistema.

- **Graphviz**: O projeto utiliza a biblioteca Graphviz para gerar visualizações da árvore de busca. Para instalar o Graphviz, siga as instruções no [documento oficial](https://pygraphviz.github.io/documentation/stable/install.html).

---

### Configuração do Ambiente Virtual
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
   pip install networkx matplotlib graphviz
   ```

4. **Verificar as bibliotecas instaladas:**
   ```sh
   pip list
   ```
---

### Executando o Programa no Linux
Para rodar o código, ative o ambiente virtual e execute o arquivo principal:
```sh
source venv/bin/activate
python3 app.py
```

Se desejar sair do ambiente virtual após a execução, utilize:
```sh
deactivate
```


