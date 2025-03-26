# A singleton method is defined for a single object.

obj = Object.new

def obj.say_hello
  "Hello from singleton method!"
end

puts obj.say_hello  # Hello from singleton method!
