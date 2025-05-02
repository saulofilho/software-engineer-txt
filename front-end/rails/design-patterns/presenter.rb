class UserPresenter
  def initialize(user)
    @user = user
  end

  def display_name
    "#{@user.name.upcase}"
  end
end

presenter = UserPresenter.new(User.find(1))
puts presenter.display_name
