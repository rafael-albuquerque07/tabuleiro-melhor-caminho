Jogo de Tabuleiro com Algoritmos de Pathfinding
Este projeto implementa um jogo de tabuleiro interativo que demonstra diferentes algoritmos de pathfinding (Backtracking e A*) em um ambiente visual e educativo.
📝 Descrição da Atividade
✅ O que a atividade pedia:

Backtracking com recursão – ✔️ Implementado corretamente com função recursiva que explora todas as possibilidades.
Tabuleiro NxN com espaços livres e bloqueados ('X') – ✔️ Implementado como matriz 2D com obstáculos.
Marcar o melhor caminho encontrado – ✔️ O caminho é marcado com símbolos () para A e (+) para Backtracking.
Mostrar o tabuleiro formatado com pipes | – ✔️ Implementado na função mostrar_tabuleiro.
Escolher a melhor movimentação – ✔️ Implementado usando profundidade mínima para Backtracking e heurística para A*.

💡 Melhorias implementadas:

Algoritmo A com heurística de Manhattan* – Implementa um algoritmo de pathfinding mais eficiente
Modo interativo – Permite ao usuário escolher entre exploração manual ou automática
Visualização passo a passo – Mostra o progresso do algoritmo em tempo real
Comparação visual de caminhos – Compara o caminho do usuário com o caminho ótimo
Histórico de posições – Mostra todas as posições percorridas durante a exploração manual
Análise educacional – Compara a eficiência dos diferentes caminhos encontrados

💻 Pseudocódigo do Algoritmo Backtracking
Função BacktrackingRecursivo(tabuleiro, posição_atual, destino, profundidade, caminho_atual, melhor_caminho):
    Se já temos um caminho melhor com menor profundidade:
        Retorna nulo (poda)
    
    Se chegamos ao destino:
        Se não temos melhor_caminho OU profundidade < comprimento(melhor_caminho):
            melhor_caminho = caminho_atual
        Retorna (posição_atual, profundidade)
    
    melhor_resultado = nulo
    
    Para cada direção possível (direita, baixo, esquerda, cima):
        nova_posição = mover(posição_atual, direção)
        
        Se movimento_válido(tabuleiro, nova_posição):
            Marcar nova_posição como visitada
            Adicionar nova_posição ao caminho_atual
            
            resultado = BacktrackingRecursivo(tabuleiro, nova_posição, destino, 
                                             profundidade+1, caminho_atual, melhor_caminho)
            
            Desmarcar nova_posição (backtracking)
            Remover nova_posição do caminho_atual
            
            Se resultado é melhor que melhor_resultado:
                melhor_resultado = resultado
    
    Retorna melhor_resultado
💻 Pseudocódigo do Algoritmo A*
Função A*(tabuleiro, início, destino):
    Criar fila_prioridade com nós ordenados por f_score
    f_score = g_score (custo do caminho até agora) + h_score (heurística)
    
    Adicionar nó inicial à fila_prioridade
    visitados = conjunto vazio
    melhor_custo[início] = 0
    
    Enquanto fila_prioridade não estiver vazia:
        atual = Remover nó com menor f_score da fila_prioridade
        
        Se atual está em visitados:
            Continuar
        
        Adicionar atual a visitados
        
        Se atual == destino:
            Retornar caminho encontrado
        
        Para cada direção possível:
            nova_posição = mover(atual, direção)
            
            Se nova_posição é válida:
                novo_g_score = g_score(atual) + 1
                
                Se já temos um caminho melhor para nova_posição:
                    Continuar
                
                melhor_custo[nova_posição] = novo_g_score
                novo_f_score = novo_g_score + distância_manhattan(nova_posição, destino)
                
                Adicionar (novo_f_score, nova_posição, caminho + [nova_posição]) à fila_prioridade
    
    Retornar nulo (não há caminho)
🎮 Como usar o programa

Execute o programa: python jogo_tabuleiro.py
O programa mostrará o tabuleiro inicial e calculará caminhos usando os algoritmos A* e Backtracking
Escolha qual algoritmo usar: A* (*) ou Backtracking (+)
Se escolher A*:

Você poderá optar entre modo manual (definindo seu próprio caminho) ou automático (seguindo o caminho do A*)
No modo manual, você digitará as coordenadas de cada passo
No final, o programa comparará seu caminho com o caminho ótimo do A*


Se escolher Backtracking:

O programa mostrará o caminho encontrado pelo algoritmo passo a passo



🔍 Explicação dos Algoritmos
Backtracking Recursivo
O algoritmo Backtracking explora todas as possibilidades de caminhos recursivamente:

Tenta cada direção possível (direita, baixo, esquerda, cima)
Marca as posições como visitadas temporariamente
Se chegar a um beco sem saída, volta (backtrack) e tenta outro caminho
Mantém o melhor caminho encontrado (com menor profundidade)

A* (A-Star)
O algoritmo A* é mais eficiente, usando uma heurística para guiar a busca:

Utiliza uma função f(n) = g(n) + h(n) para avaliar nós

g(n): custo do caminho do início até o nó n
h(n): estimativa do custo do nó n até o destino (distância de Manhattan)


Usa uma fila de prioridade para sempre expandir o nó mais promissor
Garante encontrar o caminho mais curto se a heurística for admissível

📊 Comparação dos Algoritmos
CaracterísticaBacktrackingA*EficiênciaPode explorar muitos caminhos desnecessáriosMais eficiente, focado em caminhos promissoresCompletudeEncontra um caminho se existirEncontra um caminho se existirOtimidadeNão garante o caminho mais curtoGarante o caminho mais curtoMemóriaUsa menos memóriaPode usar mais memória para rastrear nósHeurísticaNão usaUsa distância de Manhattan
🧠 Valor Educacional
Este projeto demonstra:

Como os algoritmos de pathfinding funcionam visualmente
Diferenças entre abordagens de força bruta (Backtracking) e heurísticas inteligentes (A*)
A importância de funções heurísticas em algoritmos de busca
Visualização de conceitos abstratos de ciência da computação
Interatividade para experimentação de diferentes caminhos e comparação com soluções ótimas

🛠️ Recursos e Estruturas de Dados Utilizadas

Matriz 2D: Para representar o tabuleiro
Recursão: Para implementar o Backtracking
Fila de Prioridade (Heap): Para o algoritmo A*
Heurística de Manhattan: Para estimar distâncias no A*
Conjunto (Set): Para rastrear posições visitadas
Backtracking: Técnica de volta quando um caminho não é promissor

Este projeto combina conceitos fundamentais de algoritmos e estruturas de dados com uma interface interativa que permite aos usuários visualizar e compreender como diferentes algoritmos de pathfinding funcionam na prática.
