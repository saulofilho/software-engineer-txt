# Arrays e Strings em Ruby

# Inverter string
s = "hello"
puts s.reverse  # => "olleh"

# Encontrar subarray com soma máxima (Kadane)
def max_subarray(nums)
  max_sum = curr = nums.first
  nums.drop(1).each do |num|
    curr    = [num, curr + num].max
    max_sum = [max_sum, curr].max
  end
  max_sum
end

puts max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])  # => 6

# Rotacionar array
def rotate_array(arr, k)
  k %= arr.size
  arr[-k, k] + arr[0, arr.size - k]
end

p rotate_array([1,2,3,4,5,6,7], 3)  # => [5,6,7,1,2,3,4]


# Listas Ligadas em Ruby
class ListNode
  attr_accessor :val, :next

  def initialize(val = 0, nxt = nil)
    @val  = val
    @next = nxt
  end
end

# Reverter lista ligada
def reverse_list(head)
  prev = nil
  curr = head
  while curr
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
  end
  prev
end

# Detectar ciclo (Floyd’s Cycle Detection)
def has_cycle(head)
  slow = fast = head
  while fast && fast.next
    slow = slow.next
    fast = fast.next.next
    return true if slow == fast
  end
  false
end

# Mesclar duas listas ordenadas
def merge_lists(l1, l2)
  dummy = ListNode.new
  tail  = dummy
  while l1 && l2
    if l1.val < l2.val
      tail.next, l1 = l1, l1.next
    else
      tail.next, l2 = l2, l2.next
    end
    tail = tail.next
  end
  tail.next = l1 || l2
  dummy.next
end


# Pilhas e Filas

# Pilha simples usando Array
stack = []
stack.push(1)
stack.push(2)
puts stack.pop  # => 2

# Pilha com valor mínimo em O(1)
class MinStack
  def initialize
    @stack     = []
    @min_stack = []
  end

  def push(x)
    @stack << x
    @min_stack << x if @min_stack.empty? || x <= @min_stack.last
  end

  def pop
    val = @stack.pop
    @min_stack.pop if val == @min_stack.last
    val
  end

  def top
    @stack.last
  end

  def get_min
    @min_stack.last
  end
end

# Exemplo MinStack
ms = MinStack.new
ms.push(3)
ms.push(5)
ms.push(2)
puts ms.get_min  # => 2
ms.pop
puts ms.get_min  # => 3

# Fila circular
class CircularQueue
  def initialize(k)
    @queue = Array.new(k)
    @size  = k
    @head  = -1
    @tail  = -1
  end

  def en_queue(val)
    return false if (@tail + 1) % @size == @head
    @head = 0 if @head == -1
    @tail = (@tail + 1) % @size
    @queue[@tail] = val
    true
  end

  def de_queue
    return false if empty?
    if @head == @tail
      @head = @tail = -1
    else
      @head = (@head + 1) % @size
    end
    true
  end

  def front
    empty? ? nil : @queue[@head]
  end

  def rear
    empty? ? nil : @queue[@tail]
  end

  def empty?
    @head == -1
  end

  def full?
    (@tail + 1) % @size == @head
  end
end

# Exemplo CircularQueue
cq = CircularQueue.new(3)
puts cq.en_queue(1)  # => true
puts cq.en_queue(2)  # => true
puts cq.en_queue(3)  # => true
puts cq.en_queue(4)  # => false (full)
puts cq.rear         # => 3
puts cq.de_queue     # => true
puts cq.en_queue(4)  # => true
puts cq.rear         # => 4
