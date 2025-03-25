def busca_binaria(arr, alvo)
  esquerda, direita = 0, arr.length - 1
  while esquerda <= direita
    meio = (esquerda + direita) / 2
    return meio if arr[meio] == alvo
    arr[meio] < alvo ? esquerda = meio + 1 : direita = meio - 1
  end
  nil
end
