# Antes de aplicar SRP
class Order
  def initialize
    @items = []
  end

  def add_item(item)
    @items << item
  end

  def total
    @items.sum(&:price)
  end

  def save
    # Lógica para salvar no banco de dados
  end
end

# Depois de aplicar SRP
class Order
  def initialize
    @items = []
  end

  def add_item(item)
    @items << item
  end

  def total
    @items.sum(&:price)
  end
end

class OrderRepository
  def save(order)
    # Lógica para salvar no banco de dados
  end
end
