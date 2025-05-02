class Component
  def render; end
end

class Button < Component
  def render
    puts "Render button"
  end
end

class Panel < Component
  def initialize
    @children = []
  end

  def add(child)
    @children << child
  end

  def render
    @children.each(&:render)
  end
end
