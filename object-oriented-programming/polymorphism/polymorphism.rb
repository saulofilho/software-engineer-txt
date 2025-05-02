class Animal
  def speak
    raise NotImplementedError, "This method should be overridden"
  end
end

class Dog < Animal
  def speak
    "Woof!"
  end
end

class Cat < Animal
  def speak
    "Meow!"
  end
end

# animals = [Dog.new, Cat.new]
# animals.each { |animal| puts animal.speak }

# Woof!
# Meow!
