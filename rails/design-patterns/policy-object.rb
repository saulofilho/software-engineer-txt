class UserPolicy
  attr_reader :user, :record

  def initialize(user, record)
    @user = user
    @record = record
  end

  def update?
    user.admin?
  end
end

policy = UserPolicy.new(current_user, @user)
policy.update?
