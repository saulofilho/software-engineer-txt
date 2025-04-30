# Antes de aplicar OCP
class AreaCalculator
  def calculate(shape)
    if shape.is_a?(Circle)
      return Math::PI * shape.radius**2
    elsif shape.is_a?(Rectangle)
      return shape.width * shape.height
    end
  end
end

# Depois de aplicar OCP
class AreaCalculator
  def calculate(shape)
    shape.area
  end
end

class Circle
  attr_reader :radius

  def initialize(radius)
    @radius = radius
  end

  def area
    Math::PI * radius**2
  end
end

class Rectangle
  attr_reader :width, :height

  def initialize(width, height)
    @width = width
    @height = height
  end

  def area
    width * height
  end
end
