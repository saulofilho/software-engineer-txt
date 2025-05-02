class PaymentStrategy
  def pay(amount); end
end

class CreditCardPayment < PaymentStrategy
  def pay(amount)
    puts "Paying #{amount} with credit card"
  end
end

class PaypalPayment < PaymentStrategy
  def pay(amount)
    puts "Paying #{amount} with PayPal"
  end
end

class PaymentProcessor
  def initialize(strategy)
    @strategy = strategy
  end

  def process(amount)
    @strategy.pay(amount)
  end
end
