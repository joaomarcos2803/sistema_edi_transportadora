# Descrição
Servidor gRPC do sistema da transportadora da aplicação de EDI

## Bibliotecas utilizadas
- [protobuf](https://pypi.org/project/protobuf/) 
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [grpcio](https://pypi.org/project/grpcio/)
- [Requests](https://pypi.org/project/requests/)
- [protobuf3_to_dict](https://pypi.org/project/protobuf3-to-dict/)
- [protobuf_to_dict](https://pypi.org/project/protobuf-to-dict/)


## Instruções
1. Clonar repositório
   ```bash
     git clone https://github.com/joaomarcos2803/sistema_edi_transportadora.git
     cd sistema_edi_transportadora
   ```
2. Instalar dependências

   ```bash
     pip install -r requirements.txt
   ```
3. Configurar a engine de conexão com o banco presente no arquivo dao.py.
   ```
    engine = create_engine("postgresql+psycopg2://postgres:teste@localhost:5432/EDI")
   ```

4. Executar o servidor
   ```
     python server.py
   ```
