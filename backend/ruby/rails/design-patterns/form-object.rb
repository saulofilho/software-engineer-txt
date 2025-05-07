class UserRegistrationForm
  include ActiveModel::Model

  attr_accessor :name, :email, :password

  validates :name, :email, :password, presence: true

  def save
    return false unless valid?
    User.create(name: name, email: email, password: password)
  end
end

form = UserRegistrationForm.new(name: "Alice", email: "alice@example.com", password: "123456")
form.save if form.valid?
