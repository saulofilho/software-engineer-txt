class ButtonComponent < ViewComponent::Base
  def initialize(text:)
    @text = text
  end

  def call
    content_tag(:button, @text, class: "btn btn-primary")
  end
end
