# Metaprogramming allows Ruby code to define or modify classes and methods dynamically.

# Defining Methods Dynamically with define_method

class Person
  [:name, :age, :city].each do |attr|
    define_method(attr) do
      instance_variable_get("@#{attr}")
    end

    define_method("#{attr}=") do |value|
      instance_variable_set("@#{attr}", value)
    end
  end
end

person = Person.new
person.name = "Alice"
person.age = 30
puts person.name  # Alice
