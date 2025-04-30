# Antes de aplicar KISS
class User
  def initialize(age)
    if age < 0
      raise "Idade não pode ser negativa"
    end

    @age = age
  end
end

# Depois de aplicar KISS
class User
  def initialize(age)
    @age = age
  end

  def age_valid?
    @age >= 0
  end
end
