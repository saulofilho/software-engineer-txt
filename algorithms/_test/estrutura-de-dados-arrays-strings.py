
# Arrays e Strings:

# # Inverter string
s = "hello"
print(s[::-1])  # 'olleh'


# # Encontrar subarray com soma máxima (Kadane)
def max_subarray(nums):
    max_sum = curr = nums[0]
    for num in nums[1:]:
        curr = max(num, curr + num)
        max_sum = max(max_sum, curr)
    return max_sum

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6


# # Rotacionar array
def rotate_array(arr, k):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

print(rotate_array([1,2,3,4,5,6,7], 3))  # [5,6,7,1,2,3,4]


# # Listas Ligadas:
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# # Reverter lista ligada
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev


# # Detectar ciclo (Floyd’s Cycle)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


# # Mesclar duas listas ordenadas
def merge_lists(l1, l2):
    dummy = tail = ListNode()
    while l1 and l2:
        if l1.val < l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next


# Pilhas e Filas:

# # Implementar pilha/filas usando arrays ou listas
stack = []
stack.append(1)
stack.append(2)
print(stack.pop())  # 2


# # Pilha com valor mínimo em O(1)
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x):
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self):
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def get_min(self):
        return self.min_stack[-1]


# # Fila circular
class CircularQueue:
    def __init__(self, k):
        self.q = [None]*k
        self.size = k
        self.head = self.tail = -1

    def enQueue(self, val):
        if (self.tail + 1) % self.size == self.head:
            return False
        if self.head == -1: self.head = 0
        self.tail = (self.tail + 1) % self.size
        self.q[self.tail] = val
        return True
