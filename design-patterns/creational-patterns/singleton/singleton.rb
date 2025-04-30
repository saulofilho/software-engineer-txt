require 'singleton'

class Logger
  include Singleton

  def log(message)
    puts "LOG: #{message}"
  end
end

# Uso do Singleton
logger1 = Logger.instance
logger2 = Logger.instance

logger1.log("Isso é um Singleton!")

puts logger1.equal?(logger2)  # true (mesma instância)
