class ProcessPaymentService
  def initialize(user, amount)
    @user = user
    @amount = amount
  end

  def call
    Payment.create(user: @user, amount: @amount)
    # Lógica adicional, como chamar uma API de pagamento
  end
end

ProcessPaymentService.new(user, 100).call
