class UserRepository
  def self.find_active
    User.where(active: true)
  end
end

UserRepository.find_active
