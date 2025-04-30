# Antes de aplicar ISP
class Animal
  def swim
    # Implementação de natação
  end

  def fly
    # Implementação de voo
  end
end

class Fish < Animal
  # Não pode voar, então deixa o método vazio
end

# Depois de aplicar ISP
class Swimmable
  def swim; end
end

class Flyable
  def fly; end
end

class Fish
  include Swimmable
end

class Bird
  include Flyable
  include Swimmable
end
