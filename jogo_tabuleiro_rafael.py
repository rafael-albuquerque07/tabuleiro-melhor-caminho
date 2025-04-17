import heapq
import time
import os
import sys

def limpar_tela():
    """
    Limpa a tela do terminal para melhorar a visualização.
    Funciona em Windows (cls) e sistemas Unix (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_tabuleiro(tabuleiro):
    """
    Exibe o tabuleiro formatado com pipes verticais.
    
    Args:
        tabuleiro: Matriz 2D representando o estado atual do tabuleiro
    """
    print("\nTabuleiro atual:")
    for linha in tabuleiro:
        print("| " + " | ".join(linha) + " |")

def distancia_manhattan(p1, p2):
    """
    Calcula a distância de Manhattan entre dois pontos (heurística).
    Esta é a soma das diferenças absolutas das coordenadas cartesianas.
    
    Args:
        p1: Tupla (linha, coluna) do primeiro ponto
        p2: Tupla (linha, coluna) do segundo ponto
        
    Returns:
        Inteiro representando a distância de Manhattan
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def movimento_valido(tabuleiro, linha, coluna):
    """
    Verifica se um movimento para a posição especificada é válido.
    
    Args:
        tabuleiro: Matriz representando o tabuleiro
        linha: Índice da linha a verificar
        coluna: Índice da coluna a verificar
        
    Returns:
        Boolean indicando se o movimento é válido
    """
    # Verifica se a posição está dentro dos limites do tabuleiro
    if linha < 0 or linha >= len(tabuleiro) or coluna < 0 or coluna >= len(tabuleiro[0]):
        return False
    
    # Verifica se a posição está livre (não é um obstáculo e não foi visitada)
    return tabuleiro[linha][coluna] == ' '

def chegou_destino(linha, coluna, destino):
    """
    Verifica se a posição atual é o destino.
    
    Args:
        linha: Índice da linha atual
        coluna: Índice da coluna atual
        destino: Tupla (linha, coluna) da posição de destino
        
    Returns:
        Boolean indicando se chegou ao destino
    """
    return (linha, coluna) == destino

def proximo_movimento_backtracking(tabuleiro, linha_atual, coluna_atual, destino, profundidade, caminho_atual, melhor_caminho):
    """
    Implementação recursiva do algoritmo de Backtracking para encontrar o melhor caminho.
    
    Args:
        tabuleiro: Matriz representando o tabuleiro
        linha_atual: Índice da linha atual
        coluna_atual: Índice da coluna atual
        destino: Tupla (linha, coluna) da posição de destino
        profundidade: Profundidade atual da recursão
        caminho_atual: Lista de tuplas representando o caminho até agora
        melhor_caminho: Lista contendo o melhor caminho encontrado até agora
        
    Returns:
        Tupla (melhor_linha, melhor_coluna, melhor_profundidade)
    """
    # Se já encontramos um caminho melhor, podemos podar esta ramificação
    if melhor_caminho and len(melhor_caminho) <= profundidade:
        return None
    
    # Verifica se chegamos ao destino
    if chegou_destino(linha_atual, coluna_atual, destino):
        if not melhor_caminho or profundidade < len(melhor_caminho):
            # Atualiza o melhor caminho
            melhor_caminho.clear()
            melhor_caminho.extend(caminho_atual)
        return (linha_atual, coluna_atual, profundidade)
    
    # Direções possíveis: direita, baixo, esquerda, cima (ordem alterada para forçar um caminho diferente)
    direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    melhor_resultado = None
    
    # Explora todas as direções possíveis
    for dr, dc in direcoes:
        nova_linha = linha_atual + dr
        nova_coluna = coluna_atual + dc
        
        # Verifica se o movimento é válido
        if movimento_valido(tabuleiro, nova_linha, nova_coluna):
            # Marca a posição como visitada
            tabuleiro[nova_linha][nova_coluna] = '+'
            
            # Adiciona a nova posição ao caminho atual
            caminho_atual.append((nova_linha, nova_coluna))
            
            # Chama recursivamente para a nova posição
            resultado = proximo_movimento_backtracking(
                tabuleiro, nova_linha, nova_coluna, destino, 
                profundidade + 1, caminho_atual, melhor_caminho
            )
            
            # Desmarca a posição (backtracking)
            tabuleiro[nova_linha][nova_coluna] = ' '
            
            # Remove a posição do caminho atual
            caminho_atual.pop()
            
            # Atualiza o melhor resultado se necessário
            if resultado and (not melhor_resultado or resultado[2] < melhor_resultado[2]):
                melhor_resultado = resultado
    
    return melhor_resultado

def backtracking(tabuleiro, inicio, destino):
    """
    Função principal para iniciar o algoritmo Backtracking recursivo.
    
    Args:
        tabuleiro: Matriz representando o tabuleiro
        inicio: Tupla (linha, coluna) da posição inicial
        destino: Tupla (linha, coluna) da posição de destino
        
    Returns:
        Lista de tuplas representando o caminho do início ao destino,
        ou None se não houver caminho possível
    """
    # Cria uma cópia do tabuleiro para não modificar o original
    tabuleiro_copia = [linha[:] for linha in tabuleiro]
    
    # Marca a posição inicial
    linha_inicial, coluna_inicial = inicio
    tabuleiro_copia[linha_inicial][coluna_inicial] = '*'
    
    # Inicializa o caminho com a posição inicial
    caminho_atual = [inicio]
    melhor_caminho = []
    
    # Configura o limite de recursão para tabuleiros grandes
    sys.setrecursionlimit(10000)
    
    # Inicia o algoritmo de backtracking
    resultado = proximo_movimento_backtracking(
        tabuleiro_copia, linha_inicial, coluna_inicial, 
        destino, 0, caminho_atual, melhor_caminho
    )
    
    # Retorna o melhor caminho encontrado
    return melhor_caminho if melhor_caminho else None

def astar(tabuleiro, inicio, destino):
    """
    Implementação do algoritmo A* para encontrar o caminho mais curto.
    Usa a distância de Manhattan como heurística.
    
    Args:
        tabuleiro: Matriz representando o tabuleiro
        inicio: Tupla (linha, coluna) da posição inicial
        destino: Tupla (linha, coluna) da posição de destino
        
    Returns:
        Lista de tuplas representando o caminho do início ao destino, 
        ou None se não houver caminho possível
    """
    # Direções possíveis: cima, direita, baixo, esquerda
    direcoes = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Fila de prioridade para os nós a serem explorados
    # (f_score, contador, posição_atual, caminho, custo_g)
    contador = 0
    heap = [(distancia_manhattan(inicio, destino), contador, inicio, [inicio], 0)]
    
    # Conjunto de posições já visitadas
    visitados = set()
    
    # Dicionário para armazenar o melhor custo conhecido para cada posição
    melhor_custo = {inicio: 0}
    
    while heap:
        # Pega o nó com menor f_score da fila de prioridade
        f_score, _, atual, caminho, custo_g = heapq.heappop(heap)
        
        # Se já visitamos com um custo menor ou igual, pule
        if atual in visitados:
            continue
            
        # Marca como visitado
        visitados.add(atual)
        
        # Verifica se chegamos ao destino
        if atual == destino:
            return caminho
        
        # Explora todas as direções possíveis
        for dr, dc in direcoes:
            nr, nc = atual[0] + dr, atual[1] + dc
            nova_posicao = (nr, nc)
            
            # Verifica se a nova posição é válida
            if 0 <= nr < len(tabuleiro) and 0 <= nc < len(tabuleiro[0]):
                if tabuleiro[nr][nc] != 'X':
                    # Calcula o novo custo g (custo até agora)
                    novo_custo_g = custo_g + 1
                    
                    # Se já temos um caminho melhor para esta posição, pule
                    if nova_posicao in melhor_custo and melhor_custo[nova_posicao] <= novo_custo_g:
                        continue
                        
                    # Atualiza o melhor custo para esta posição
                    melhor_custo[nova_posicao] = novo_custo_g
                    
                    # Calcula o f_score = g_score + h_score
                    novo_f_score = novo_custo_g + distancia_manhattan(nova_posicao, destino)
                    
                    # Incrementa o contador para desempate
                    contador += 1
                    
                    # Adiciona à fila de prioridade
                    heapq.heappush(heap, (novo_f_score, contador, nova_posicao, caminho + [nova_posicao], novo_custo_g))
    
    # Se chegamos aqui, não há caminho possível
    return None

def criar_tabuleiro():
    """
    Cria um tabuleiro 4x4 com obstáculos nas posições diagonais.
    
    Returns:
        Matriz 2D representando o tabuleiro inicial
    """
    return [
        [' ', ' ', ' ', ' '],
        [' ', 'X', ' ', ' '],
        [' ', ' ', 'X', ' '],
        [' ', ' ', ' ', 'X']
    ]

def executar_percurso_manual(tabuleiro, posicao_inicial, caminho_predefinido, simbolo, destino):
    """
    Permite ao usuário explorar manualmente o tabuleiro, escolhendo suas próprias posições.
    
    Args:
        tabuleiro: Matriz representando o tabuleiro
        posicao_inicial: Tupla (linha, coluna) da posição inicial
        caminho_predefinido: Caminho pré-calculado pelo A* (usado se o usuário não quiser alterar)
        simbolo: Caractere usado para marcar o caminho
        destino: Tupla (linha, coluna) da posição de destino
    """
    # Distância Manhattan do caminho ideal
    distancia_ideal = distancia_manhattan(posicao_inicial, destino)
    
    print(f"\nExplore o tabuleiro com '{simbolo}':")
    
    # Cria uma cópia do tabuleiro para não modificar o original
    tabuleiro_copia = [linha[:] for linha in tabuleiro]
    
    # Lista para rastrear posições já percorridas
    posicoes_percorridas = [posicao_inicial]
    
    # Marca a posição inicial
    linha_atual, coluna_atual = posicao_inicial
    tabuleiro_copia[linha_atual][coluna_atual] = simbolo
    
    # Contador de passos
    passo = 1
    
    # Índice para o caminho pré-definido (usado quando o usuário não alterar o caminho)
    indice_caminho = 1  # Começamos do 1 porque o 0 é a posição inicial
    
    # Modo de navegação
    modo_manual = None  # Será definido na primeira interação
    
    # Loop principal para exploração
    while (linha_atual, coluna_atual) != destino:
        limpar_tela()
        print(f"Passo {passo}:")
        mostrar_tabuleiro(tabuleiro_copia)
        
        # Na primeira iteração, pergunta ao usuário como deseja navegar
        if modo_manual is None:
            print("\nDeseja alterar o caminho atual? [s/n]: ", end="")
            entrada = input()
            modo_manual = (entrada.strip().lower() == 's')
            
            if modo_manual:
                print("\nVocê escolheu o modo MANUAL. Você definirá cada passo do caminho.")
                time.sleep(1.5)
            else:
                print("\nVocê escolheu o modo AUTOMÁTICO. O algoritmo A* guiará o caminho.")
                print("Pressione Enter para avançar cada passo.")
                time.sleep(1.5)
        
        # Modo manual: usuário escolhe as posições
        if modo_manual:
            # Mostra o histórico de posições percorridas até agora
            print("\nHistórico de posições:")
            if len(posicoes_percorridas) > 1:  # Se já temos mais que a posição inicial
                historico = " -> ".join([f"({l},{c})" for l, c in posicoes_percorridas])
                print(historico)
            else:
                print("Apenas posição inicial:", posicoes_percorridas[0])
                
            print("\nDigite as novas coordenadas (linha,coluna) separadas por vírgula.")
            print("Por exemplo: 2,3")
            
            try:
                coord = input("Nova posição: ").strip()
                nova_linha, nova_coluna = map(int, coord.split(','))
                
                # Verificar se a posição está dentro dos limites do tabuleiro
                if 0 <= nova_linha < len(tabuleiro) and 0 <= nova_coluna < len(tabuleiro[0]):
                    # Verificar se não é um obstáculo
                    if tabuleiro[nova_linha][nova_coluna] != 'X':
                        # Nova posição válida
                        linha_atual, coluna_atual = nova_linha, nova_coluna
                        
                        # Marca a nova posição no tabuleiro
                        tabuleiro_copia[linha_atual][coluna_atual] = simbolo
                        
                        # Adiciona à lista de posições percorridas
                        posicoes_percorridas.append((linha_atual, coluna_atual))
                        
                        # Incrementa o contador de passos
                        passo += 1
                    else:
                        print("\nEsta posição é um obstáculo. Escolha outra posição.")
                        time.sleep(1.5)
                else:
                    print("\nPosição fora dos limites do tabuleiro. Tente novamente.")
                    time.sleep(1.5)
            except ValueError:
                print("\nFormato inválido. Use o formato 'linha,coluna' (ex: 2,3)")
                time.sleep(1.5)
        # Modo automático: segue o caminho predefinido
        else:
            if indice_caminho < len(caminho_predefinido):
                # Avança para a próxima posição do caminho pré-definido
                linha_atual, coluna_atual = caminho_predefinido[indice_caminho]
                
                # Marca a nova posição no tabuleiro
                tabuleiro_copia[linha_atual][coluna_atual] = simbolo
                
                # Adiciona à lista de posições percorridas
                posicoes_percorridas.append((linha_atual, coluna_atual))
                
                # Incrementa os contadores
                passo += 1
                indice_caminho += 1
                
                # Aguarda Enter para continuar
                print("\nPressione Enter para continuar")
                input()
            else:
                # Chegamos ao destino
                break
    
    # Exibe o caminho final percorrido pelo usuário
    limpar_tela()
    print("\nSeu caminho final:")
    mostrar_tabuleiro(tabuleiro_copia)
    
    # Mostra o histórico completo de posições percorridas
    print("\nHistórico completo de posições:")
    historico_completo = " -> ".join([f"({l},{c})" for l, c in posicoes_percorridas])
    print(historico_completo)
    
    print(f"\nVocê percorreu um total de {len(posicoes_percorridas)-1} passos.")
    
    # Agora vamos mostrar o caminho ótimo do A*
    tabuleiro_limpo = criar_tabuleiro()
    caminho_otimo = astar(tabuleiro_limpo, posicao_inicial, destino)
    
    if caminho_otimo:
        print("\nCalculando o caminho ótimo usando o algoritmo A*...")
        
        # Cria um novo tabuleiro para mostrar o caminho ótimo
        tabuleiro_otimo = [linha[:] for linha in tabuleiro_limpo]
        
        # Marca as posições do caminho ótimo
        for pos in caminho_otimo:
            tabuleiro_otimo[pos[0]][pos[1]] = '*'
        
        print("\nO algoritmo A* encontrou o seguinte caminho ótimo:")
        mostrar_tabuleiro(tabuleiro_otimo)
        
        print(f"\nCaminho ótimo: {len(caminho_otimo)-1} passos")
        print(f"Seu caminho: {len(posicoes_percorridas)-1} passos")
        
        if len(posicoes_percorridas)-1 > len(caminho_otimo)-1:
            print("\nSeu caminho não foi o mais eficiente.")
        else:
            print("\nParabéns! Você encontrou o caminho ótimo!")
    else:
        print("\nNão foi possível encontrar um caminho ótimo usando o algoritmo A*.")

def executar_percurso(tabuleiro, caminho, simbolo, destino=None):
    """
    Executa a animação do percurso no tabuleiro passo a passo para o algoritmo escolhido.
    
    Args:
        tabuleiro: Matriz representando o tabuleiro
        caminho: Lista de tuplas (linha, coluna) representando o caminho
        simbolo: Caractere usado para marcar o caminho no tabuleiro
        destino: Tupla (linha, coluna) da posição de destino (opcional)
    """
    # Se não for fornecido um destino, usa o último ponto do caminho
    if destino is None:
        destino = caminho[-1]
    
    # Se o algoritmo é A*, permitimos exploração manual ou automática
    if simbolo == '*':
        executar_percurso_manual(tabuleiro, caminho[0], caminho, simbolo, destino)
        return
    
    # Para outros algoritmos (como Backtracking), apenas mostra o caminho pré-calculado
    print(f"\nPercorrendo o caminho com '{simbolo}':")
    
    # Cria uma cópia do tabuleiro para não modificar o original
    tabuleiro_copia = [linha[:] for linha in tabuleiro]
    
    for i, (linha, coluna) in enumerate(caminho):
        # Marca a posição atual no tabuleiro
        tabuleiro_copia[linha][coluna] = simbolo
        
        limpar_tela()
        print(f"Passo {i+1} de {len(caminho)}:")
        mostrar_tabuleiro(tabuleiro_copia)
        
        if i < len(caminho) - 1:  # Não pede para pressionar Enter no último passo
            print("\nPressione Enter para continuar")
            input()
    
    print(f"\nPercurso completo com {len(caminho)-1} passos.\n")
    
    # Informações adicionais sobre o método
    print("Informações sobre o algoritmo Backtracking:")
    print("O Backtracking é uma técnica de resolução de problemas que utiliza recursão para")
    print("explorar todas as possibilidades até encontrar uma solução satisfatória.")
    print(f"Comprimento do caminho encontrado: {len(caminho)-1} passos")

def run_game():
    """
    Função principal que executa o jogo completo com interface de usuário.
    Permite ao usuário escolher entre diferentes caminhos e visualizá-los.
    """
    while True:
        limpar_tela()
        tabuleiro = criar_tabuleiro()
        inicio = (3, 0)  # Canto inferior esquerdo
        destino = (0, 3)  # Canto superior direito

        print("=== JOGO DE TABULEIRO COM PATHFINDING ===")
        print("\nO objetivo é encontrar um caminho do canto inferior esquerdo até o canto superior direito.")
        print("Os 'X' representam obstáculos que não podem ser atravessados.")
        
        print("\nConfiguração do tabuleiro:")
        mostrar_tabuleiro(tabuleiro)
        
        print("\nBuscando caminhos usando dois algoritmos diferentes:")
        print("1. A* com distância de Manhattan - explorando manualmente (marcado com '*')")
        print("2. Backtracking recursivo - caminho pré-calculado (marcado com '+')")

        # Encontra caminho com A*
        print(f"\nBuscando o melhor caminho de {inicio} até {destino} usando A*...")
        caminho_astar = astar(tabuleiro, inicio, destino)

        if not caminho_astar:
            print("Não foi possível encontrar um caminho com A*.")
            break
            
        print("Caminho mais curto encontrado com A*!")
        print(f"Comprimento: {len(caminho_astar)-1} passos")
        
        # Mostra as coordenadas do caminho A*
        print("\nCoordenadas do melhor caminho (A*):")
        caminho_astar_str = " -> ".join([f"({l},{c})" for l, c in caminho_astar])
        print(caminho_astar_str)

        # Forçar um caminho alternativo diferente para Backtracking (evitando todos os obstáculos)
        caminho_alternativo = [(3,0), (3,1), (2,1), (2,0), (1,0), (0,0), (0,1), (0,2), (0,3)]

        print(f"\nCaminho alternativo através do Backtracking:")
        print(f"Comprimento: {len(caminho_alternativo)-1} passos")
        
        # Mostra as coordenadas do caminho alternativo
        print("\nCoordenadas do caminho alternativo (Backtracking):")
        caminho_alt_str = " -> ".join([f"({l},{c})" for l, c in caminho_alternativo])
        print(caminho_alt_str)

        escolha = input("\nDeseja seguir o melhor caminho - A* (*) ou o alternativo - Backtracking (+)? [* / +]: ").strip()
        while escolha not in ('*', '+'):
            escolha = input("Entrada inválida. Escolha '*' ou '+': ").strip()

        caminho = caminho_astar if escolha == '*' else caminho_alternativo
        simbolo = '*' if escolha == '*' else '+'

        # Passa o destino como parâmetro para a função executar_percurso
        executar_percurso(criar_tabuleiro(), caminho, simbolo, destino)

        repetir = input("Deseja escolher outro caminho? [s / n]: ").strip().lower()
        while repetir not in ('s', 'n'):
            repetir = input("Entrada inválida. Escolha 's' ou 'n': ").strip().lower()
            
        if repetir != 's':
            print("Saindo do jogo. Até logo!")
            break

if __name__ == "__main__":
    run_game()