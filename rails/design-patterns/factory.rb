FactoryBot.define do
  factory :user do
    name { "Alice" }
    email { "alice@example.com" }
    password { "password" }
  end
end

let(:user) { create(:user) }
