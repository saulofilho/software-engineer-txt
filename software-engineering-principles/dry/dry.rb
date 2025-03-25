# Antes de aplicar DRY
class Order
  def total
    sum = 0
    @items.each do |item|
      sum += item.price
    end
    sum
  end

  def discount
    sum = 0
    @items.each do |item|
      sum += item.discount
    end
    sum
  end
end

# Depois de aplicar DRY
class Order
  def sum_items(attribute)
    @items.sum { |item| item.send(attribute) }
  end

  def total
    sum_items(:price)
  end

  def discount
    sum_items(:discount)
  end
end
