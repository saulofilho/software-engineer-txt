# Duck typing allows objects to be interchangeable based on their behavior, not their class.

class Duck
  def quack
    "Quack!"
  end
end

class Human
  def quack
    "I can also quack!"
  end
end

def make_it_quack(entity)
  puts entity.quack
end

make_it_quack(Duck.new)   # Quack!
make_it_quack(Human.new)  # I can also quack!
