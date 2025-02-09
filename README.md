## repositorio da disicplina de Padrões
# IFMaps


## Integrantes
- [Daniel Barbosa Vasconcelos]
- [Victor José ]

## Descrição

O trabalho consiste em implementar um sistema de mapeamento de informações de IFPB campus capina grande. O sistema deve permitir a criação de mapas de informações de uma empresa, onde cada mapa é composto por nós e arestas. Cada nó representa uma informação da empresa e cada aresta representa uma relação entre duas informações. O sistema deve permitir a criação de mapas de informações de uma empresa, onde cada mapa é composto por nós e arestas.

## Padrões Utilizados

- **Singleton**: Utilizado para garantir que a classe de conexão com o banco de dados seja instanciada apenas uma vez.
- **Facede**: Utilizado para fornecer uma interface simplificada para a criação de mapas de informações.
- **Factory**: Utilizado para criar instâncias de classes de conexão com o banco de dados.
- **Strategy**: Utilizado para definir algoritmos de mapeamento de informações.
- **Observer**: Utilizado para notificar os observadores sobre a criação de um novo mapa de informações.
- **Proxy**: Utilizado para controlar o acesso a um objeto de conexão com o banco de dados.

## Diagrama de Classes
<img src=".static\img\diagrama_classe.png" alt="Diagrama de Classes" width="100%"/>

.static\img\diagrama_classe.png
## Diagrama de Casos de Uso

<img src="..static\img\diagrama_uso.png" alt="Diagrama de Casos de Uso" width="100%"/>
## Como executar

1. Clone o repositório
2. Instale as dependências
```bash
pip install -r requirements.txt
```
3. Execute o arquivo Facade.py
```bash
python Facade.py
```