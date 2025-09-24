# Threads Example (Concurrency - MRI Ruby GIL applies)

threads = []
5.times do |i|
  threads << Thread.new { puts "Thread #{i}" }
end
threads.each(&:join

# Parallel Processing with fork (for true parallel execution)

puts "Main Process PID: #{Process.pid}"

fork do
  puts "Child Process PID: #{Process.pid}"
end

Process.wait
puts "Child Process finished"
