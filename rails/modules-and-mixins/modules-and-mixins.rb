# Modules allow sharing behavior across classes.

module Flyable
  def fly
    "I'm flying!"
  end
end

class Bird
  include Flyable
end

bird = Bird.new
puts bird.fly  # I'm flying!
