# Algoritmos em Strings
# # KMP (Knuth-Morris-Pratt)
def compute_lps(pat: str) -> list[int]:
    """Constrói o array LPS (longest proper prefix-suffix)."""
    n = len(pat)
    lps = [0] * n
    length = 0
    i = 1
    while i < n:
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(txt: str, pat: str) -> list[int]:
    """
    Retorna as posições iniciais de todas ocorrências de pat em txt.
    """
    lps = compute_lps(pat)
    res = []
    i = j = 0
    while i < len(txt):
        if txt[i] == pat[j]:
            i += 1
            j += 1
            if j == len(pat):
                res.append(i - j)
                j = lps[j - 1]
        else:
            if j:
                j = lps[j - 1]
            else:
                i += 1
    return res

if __name__ == "__main__":
    text = "ABABDABACDABABCABAB"
    pat  = "ABABCABAB"
    print("KMP found at:", kmp_search(text, pat))
    # saída: [10]


# # Rabin-Karp
def rabin_karp_search(txt: str, pat: str,
                      base: int = 256, mod: int = 101) -> list[int]:
    """
    Usa hash de rolling para buscar pat em txt.
    base = tamanho do alfabeto, mod = primo para reduzir colisões.
    """
    n, m = len(txt), len(pat)
    if m > n:
        return []
    h_pat = 0
    h_txt = 0
    power = 1
    for _ in range(m - 1):
        power = (power * base) % mod
    # hash inicial
    for i in range(m):
        h_pat = (h_pat * base + ord(pat[i])) % mod
        h_txt = (h_txt * base + ord(txt[i])) % mod
    res = []
    for i in range(n - m + 1):
        if h_pat == h_txt and txt[i:i+m] == pat:
            res.append(i)
        if i < n - m:
            h_txt = (h_txt - ord(txt[i]) * power) % mod
            h_txt = (h_txt * base + ord(txt[i + m])) % mod
            h_txt = (h_txt + mod) % mod
    return res

if __name__ == "__main__":
    print("RK found at:", rabin_karp_search("hello hello", "lo h"))
    # saída: [3]


# # Z-Algorithm
def z_array(s: str) -> list[int]:
    """
    Constrói o array Z onde Z[i]=tamanho do maior prefixo começando em i.
    """
    n = len(s)
    Z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            Z[i] = min(r - i + 1, Z[i - l])
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
        if i + Z[i] - 1 > r:
            l, r = i, i + Z[i] - 1
    Z[0] = n
    return Z

if __name__ == "__main__":
    print("Z-array:", z_array("aabcaabxaaaz"))
    # saída: [12,1,0,0,3,1,0,0,2,1,0,0]


# # Aho-Corasick
class AhoNode:
    def __init__(self):
        self.next = {}      # char → AhoNode
        self.fail = None    # fallback
        self.out = []       # padrões que terminam aqui

class AhoCorasick:
    def __init__(self, patterns: list[str]):
        self.root = AhoNode()
        # build trie
        for idx, pat in enumerate(patterns):
            node = self.root
            for ch in pat:
                node = node.next.setdefault(ch, AhoNode())
            node.out.append(idx)
        # build fail links
        queue = []
        for child in self.root.next.values():
            child.fail = self.root
            queue.append(child)
        # BFS
        qi = 0
        while qi < len(queue):
            curr = queue[qi]; qi += 1
            for ch, nxt in curr.next.items():
                queue.append(nxt)
                f = curr.fail
                while f and ch not in f.next:
                    f = f.fail
                nxt.fail = f.next[ch] if f and ch in f.next else self.root
                nxt.out += nxt.fail.out

    def search(self, text: str, patterns: list[str]) -> list[tuple[int,int]]:
        """
        Retorna lista de (padrão_idx, posição_final_em_text).
        """
        res = []
        node = self.root
        for i, ch in enumerate(text):
            while node and ch not in node.next:
                node = node.fail
            node = node.next.get(ch, self.root)
            for pat_idx in node.out:
                res.append((pat_idx, i))
        return res

if __name__ == "__main__":
    pats = ["he", "she", "his", "hers"]
    ac = AhoCorasick(pats)
    hits = ac.search("ahishers", pats)
    print("Aho–Corasick matches:", [(pats[i], pos) for i, pos in hits])
    # e.g. [('his', 2), ('he', 3), ('she', 4), ('hers', 7)]


# # Suffix Array + LCP
def build_suffix_array(s: str) -> list[int]:
    """
    Constrói suffix array em O(n·log n) via sort simples.
    """
    return sorted(range(len(s)), key=lambda i: s[i:])

def build_lcp_array(s: str, sa: list[int]) -> list[int]:
    """
    LCP entre sufixos adjacentes no SA em O(n²) simples.
    """
    n = len(s)
    lcp = [0] * n
    for i in range(1, n):
        a, b = sa[i-1], sa[i]
        length = 0
        while a + length < n and b + length < n and s[a+length] == s[b+length]:
            length += 1
        lcp[i] = length
    return lcp

if __name__ == "__main__":
    text = "banana"
    sa = build_suffix_array(text)
    lcp = build_lcp_array(text, sa)
    print("SA:", sa)    # [5,3,1,0,4,2]
    print("LCP:", lcp)  # [0,1,3,0,0,2]


# # Trie com compressão
class CompressedTrieNode:
    def __init__(self):
        self.children = {}  # label_str → CompressedTrieNode
        self.is_end = False

class CompressedTrie:
    def __init__(self):
        self.root = CompressedTrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        while word:
            # tenta achar aresta com prefixo comum
            for label, child in list(node.children.items()):
                # encontra o maior prefixo comum entre label e word
                common = ""
                for x, y in zip(label, word):
                    if x == y:
                        common += x
                    else:
                        break
                if common:
                    # caso 1: label é todo prefixo
                    if common == label:
                        word = word[len(common):]
                        node = child
                    else:
                        # split da aresta
                        suffix_label = label[len(common):]
                        new_child = CompressedTrieNode()
                        new_child.children[suffix_label] = child
                        new_child.is_end = False
                        node.children.pop(label)
                        node.children[common] = new_child
                        # resto de word
                        word = word[len(common):]
                        if word:
                            new2 = CompressedTrieNode()
                            new2.is_end = True
                            new_child.children[word] = new2
                        else:
                            new_child.is_end = True
                        return
                    break
            else:
                # sem prefixo comum, cria aresta nova
                new = CompressedTrieNode()
                new.is_end = True
                node.children[word] = new
                return
        # palavra vazia depois de percorrer arestas
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        while word:
            for label, child in node.children.items():
                if word.startswith(label):
                    word = word[len(label):]
                    node = child
                    break
            else:
                return False
        return node.is_end

if __name__ == "__main__":
    trie = CompressedTrie()
    for w in ["test", "team", "teal"]:
        trie.insert(w)
    print(trie.search("team"))  # True
    print(trie.search("tea"))   # False
    print(trie.search("teal"))  # True
