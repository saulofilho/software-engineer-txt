Registry Pattern 

O Registry Pattern no Ruby é um padrão que fornece um repositório global para armazenar e recuperar instâncias de objetos com base em alguma chave. Ele é útil quando precisamos de um ponto centralizado para gerenciar instâncias de classes em um sistema.

- Ele organiza objetos dentro de um sistema de maneira centralizada.
- Define como diferentes partes do código acessam e compartilham instâncias específicas.
- Não se encaixa em padrões criacionais (como Singleton ou Factory) porque não gerencia diretamente a criação de objetos, apenas seu armazenamento e recuperação.
- Também não é um padrão comportamental, pois não lida com a comunicação entre objetos ou seus comportamentos.
