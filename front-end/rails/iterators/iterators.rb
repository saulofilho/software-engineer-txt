numbers = [1, 2, 3, 4, 5]

# map example
squared = numbers.map { |n| n ** 2 }
puts squared.inspect  # [1, 4, 9, 16, 25]

# select example
evens = numbers.select(&:even?)
puts evens.inspect  # [2, 4]
