class User < ApplicationRecord
  validates :name, presence: true
end

class UsersController < ApplicationController
  def index
    @users = User.all
  end
end

<% @users.each do |user| %>
  <p><%= user.name %></p>
<% end %>
