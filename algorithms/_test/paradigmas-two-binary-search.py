# Binary Search em resposta (parametric search)

# # Mínimo valor viável (e.g., alocação de páginas, capacidade de navio)
def min_max_pages(pages: list[int], students: int) -> int:
    """
    Alocação de páginas:
    Dado um array pages onde pages[i] é o número de páginas do i-ésimo livro,
    e um número de students estudantes, distribuir livros contiguamente
    de modo que o maior total de páginas atribuído a qualquer estudante seja mínimo.
    
    Retorna esse valor mínimo máximo.
    """
    def can_allocate(max_load: int) -> bool:
        required = 1
        current = 0
        for p in pages:
            if p > max_load:
                return False  # um livro excede a capacidade
            if current + p <= max_load:
                current += p
            else:
                required += 1
                current = p
                if required > students:
                    return False
        return True

    lo, hi = max(pages), sum(pages)
    answer = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_allocate(mid):
            answer = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return answer


def ship_capacity(weights: list[int], days: int) -> int:
    """
    Capacidade de navio:
    Dado um array weights onde weights[i] é o peso do i-ésimo pacote,
    determinar a capacidade mínima do navio para transportar todos os pacotes
    em order, dentro de days dias (cada dia carrega até a capacidade em sequência).
    
    Retorna essa capacidade mínima.
    """
    def can_ship(cap: int) -> bool:
        required_days = 1
        current = 0
        for w in weights:
            if w > cap:
                return False  # pacote isolado maior que capacidade
            if current + w <= cap:
                current += w
            else:
                required_days += 1
                current = w
                if required_days > days:
                    return False
        return True

    lo, hi = max(weights), sum(weights)
    answer = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_ship(mid):
            answer = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return answer


if __name__ == "__main__":
    # Exemplo Alocação de Páginas
    books = [100, 200, 300, 400]
    students = 2
    print("Mínimo máximo de páginas por estudante:",
          min_max_pages(books, students))
    # Saída: 500 (divisão ótima: [100,200,300] e [400])

    # Exemplo Capacidade de Navio
    weights = [3,2,2,4,1,4]
    days = 3
    print("Capacidade mínima do navio:",
          ship_capacity(weights, days))
    # Saída: 6 (rotações diárias: [3,2], [2,4], [1,4])
