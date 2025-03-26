# Intercept calls to undefined methods.

class DynamicClass
  def method_missing(name, *args)
    "You tried to call #{name} with #{args.inspect}"
  end
end

obj = DynamicClass.new
puts obj.unknown_method(1, 2, 3)
# You tried to call unknown_method with [1, 2, 3]
