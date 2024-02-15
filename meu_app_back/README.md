## COMO EXECUTAR 

1) Instalar todas as libs python listadas no arquivo `requirements.txt`.

2) Após clonar o repositório, acessar o terminal e executar os comandos descritos abaixo:

    * Criar um ambiente virtual -> Comando no terminal: python -m venv env
    * Ativar o ambiente virtual ->  Comando no terminal PARA WINDOWS: .\env\Scripts\activate (Para MAC e LINUX é utilizado outro comando)
    * Instalar os requisitos -> Comando no terminal: pip install -r requirements.txt
      Se necessário, fazer a atualização utilizando o comando no terminal: python.exe -m pip install --upgrade pip
    * Executar a API utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte. 
      Comando no terminal: flask run --host 0.0.0.0 --port 5000 --reload
    * Abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

