class UserDecorator < SimpleDelegator
  def formatted_name
    "Sr(a). #{name}"
  end
end

user = User.find(1)
decorated_user = UserDecorator.new(user)
puts decorated_user.formatted_name  # => "Sr(a). Alice"
