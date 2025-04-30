class Registry
  @items = {}

  def self.register(key, instance)
    @items[key] = instance
  end

  def self.get(key)
    @items[key]
  end
end

# Uso do Registry
Registry.register(:logger, Logger.new(STDOUT))
logger = Registry.get(:logger)
logger.info("Registry Pattern funcionando!")
