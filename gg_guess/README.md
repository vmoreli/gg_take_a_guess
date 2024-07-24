# Pitaco - Um jogo de advinhação para amantes de geografia

Pitaco é um jogo desenvolvido em Django, no qual o objetivo do usuário é acertar um país aleatório a partir de uma série de dicas, que vão sendo desbloqueadas a medida que palpites errados são feitos. Quanto mais dicas necessárias para o acerto, menos pontos o usuário ganhará.

É necessário estar logado para jogar o jogo! O site contém um leaderboard geral que exibe o top 10 usuários com mais pontos.
A partir do momento em que um usuário acerta um país no jogo, esse país não aparecerá mais em suas futuras partidas.

Funções de gerenciamento de usuários:
    - Cadastro, login, logout
    - Mudança de senha
    - Exclusão de conta

As informações dos países são obtidas por meio da API RestCountries.

