class UsersWithActiveSubscriptionQuery
  def self.call
    User.joins(:subscription).where(subscriptions: { active: true })
  end
end

UsersWithActiveSubscriptionQuery.call
