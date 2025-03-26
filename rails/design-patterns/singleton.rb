class LoggerService
  include Singleton

  def log(message)
    puts "[LOG] #{message}"
  end
end

LoggerService.instance.log("Sistema iniciado")
