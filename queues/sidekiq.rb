class HardWorker
  include Sidekiq::Worker

  def perform(name, count)
    puts "Trabalhando #{count} vezes para #{name}"
  end
end

# HardWorker.perform_async("João", 5)
