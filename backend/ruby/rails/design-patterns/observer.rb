class UserObserver < ActiveRecord::Observer
  def after_create(user)
    puts "Novo usuário criado: #{user.name}"
  end
end

# config.active_record.observers = :user_observer
