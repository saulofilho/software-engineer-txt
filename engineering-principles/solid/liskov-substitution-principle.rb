# Antes de aplicar LSP
class Bird
  def fly
    puts "Flying!"
  end
end

class Penguin < Bird
  def fly
    raise "Penguins can't fly!"
  end
end

# Depois de aplicar LSP
class Bird
  def move
    puts "Moving!"
  end
end

class Sparrow < Bird
  def move
    puts "Flying!"
  end
end

class Penguin < Bird
  def move
    puts "Waddling!"
  end
end
