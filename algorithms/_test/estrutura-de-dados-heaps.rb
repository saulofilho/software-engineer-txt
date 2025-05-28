# Heaps e Estruturas Relacionadas em Ruby

# MinHeap
class MinHeap
  def initialize
    @heap = []
  end

  def push(val)
    @heap << val
    sift_up(@heap.size - 1)
  end

  def pop
    return nil if @heap.empty?
    root = @heap[0]
    last = @heap.pop
    unless @heap.empty?
      @heap[0] = last
      sift_down(0)
    end
    root
  end

  def top
    @heap[0]
  end

  def size
    @heap.size
  end

  def empty?
    @heap.empty?
  end

  private

  def sift_up(i)
    while i > 0
      parent = (i - 1) / 2
      if @heap[i] < @heap[parent]
        @heap[i], @heap[parent] = @heap[parent], @heap[i]
        i = parent
      else
        break
      end
    end
  end

  def sift_down(i)
    n = @heap.size
    while (left = 2*i + 1) < n
      right = left + 1
      smallest = right < n && @heap[right] < @heap[left] ? right : left
      if @heap[smallest] < @heap[i]
        @heap[i], @heap[smallest] = @heap[smallest], @heap[i]
        i = smallest
      else
        break
      end
    end
  end
end

# MaxHeap
class MaxHeap
  def initialize
    @heap = []
  end

  def push(val)
    @heap << val
    sift_up(@heap.size - 1)
  end

  def pop
    return nil if @heap.empty?
    root = @heap[0]
    last = @heap.pop
    unless @heap.empty?
      @heap[0] = last
      sift_down(0)
    end
    root
  end

  def top
    @heap[0]
  end

  def size
    @heap.size
  end

  def empty?
    @heap.empty?
  end

  private

  def sift_up(i)
    while i > 0
      parent = (i - 1) / 2
      if @heap[i] > @heap[parent]
        @heap[i], @heap[parent] = @heap[parent], @heap[i]
        i = parent
      else
        break
      end
    end
  end

  def sift_down(i)
    n = @heap.size
    while (left = 2*i + 1) < n
      right = left + 1
      largest = right < n && @heap[right] > @heap[left] ? right : left
      if @heap[largest] > @heap[i]
        @heap[i], @heap[largest] = @heap[largest], @heap[i]
        i = largest
      else
        break
      end
    end
  end
end

# K maiores/menores elementos
def k_largest(nums, k)
  nums.sort.reverse.take(k)
end

def k_smallest(nums, k)
  nums.sort.take(k)
end

# MedianFinder (mediana em tempo real)
class MedianFinder
  def initialize
    @small = MaxHeap.new  # lower half
    @large = MinHeap.new  # upper half
  end

  def add_num(num)
    # insere em small (max-heap)
    @small.push(num)
    # garante small.top <= large.top
    if !@large.empty? && @small.top > @large.top
      @large.push(@small.pop)
    end
    # balanceia tamanhos
    if @small.size > @large.size + 1
      @large.push(@small.pop)
    elsif @large.size > @small.size
      @small.push(@large.pop)
    end
  end

  def find_median
    if @small.size > @large.size
      @small.top.to_f
    else
      (@small.top + @large.top) / 2.0
    end
  end
end

# Exemplo de uso
if __FILE__ == $PROGRAM_NAME
  data = [5, 3, 8, 1, 2]

  # Min-Heap
  min_heap = MinHeap.new
  data.each { |x| min_heap.push(x) }
  puts "MinHeap top: #{min_heap.top}"                           # => 1
  pops = []
  pops << min_heap.pop while min_heap.size > 0
  puts "MinHeap pop sequence: #{pops.inspect}"                 # => [1,2,3,5,8]

  # Max-Heap
  max_heap = MaxHeap.new
  data.each { |x| max_heap.push(x) }
  puts "MaxHeap top: #{max_heap.top}"                           # => 8
  pops = []
  pops << max_heap.pop while max_heap.size > 0
  puts "MaxHeap pop sequence: #{pops.inspect}"                 # => [8,5,3,2,1]

  # K maiores/menores
  sample = [7,2,9,4,3,8,1]
  p "K maiores: #{k_largest(sample, 3)}"          # => [9,8,7]
  p "K menores: #{k_smallest(sample, 3)}"        # => [1,2,3]

  # MedianFinder
  mf = MedianFinder.new
  stream = [5, 15, 1, 3, 8]
  stream.each do |num|
    mf.add_num(num)
    puts "Após inserir #{num}, mediana = #{mf.find_median}"
  end
  # Saída esperada:
  # Após inserir 5, mediana = 5.0
  # Após inserir 15, mediana = 10.0
  # Após inserir 1, mediana = 5.0
  # Após inserir 3, mediana = 4.0
  # Após inserir 8, mediana = 5.0
end
