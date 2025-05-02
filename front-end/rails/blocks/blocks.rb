def repeat(n)
  n.times { yield }
end

repeat(3) { puts "Hello!" }
