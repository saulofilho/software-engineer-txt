class UnitOfWork
  def initialize
    @new_objects = []
    @dirty_objects = []
    @deleted_objects = []
  end

  def register_new(obj)
    @new_objects << obj
  end

  def register_dirty(obj)
    @dirty_objects << obj
  end

  def register_deleted(obj)
    @deleted_objects << obj
  end

  def commit
    @new_objects.each(&:insert)
    @dirty_objects.each(&:update)
    @deleted_objects.each(&:delete)
  end
end

# real example
# app/services/user_registration_service.rb

class UserRegistrationService
  def self.call(user_params, profile_params)
    uow = UnitOfWork.new

    user = User.new(user_params)
    profile = Profile.new(profile_params)

    uow.register { user.save! }
    uow.register { profile.user = user; profile.save! }
    uow.register { AuditLog.create!(action: "UserCreated", data: user.to_json) }

    uow.commit
  end
end
