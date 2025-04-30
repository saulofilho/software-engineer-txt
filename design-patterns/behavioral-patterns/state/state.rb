class Order
  attr_accessor :state

  def initialize
    @state = CreatedState.new(self)
  end

  def next
    @state.next
  end
end

class CreatedState
  def initialize(order)
    @order = order
  end

  def next
    puts "Moving to Paid"
    @order.state = PaidState.new(@order)
  end
end

class PaidState
  def initialize(order); end
  def next
    puts "Order already paid"
  end
end
