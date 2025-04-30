No Rails, **concern** é uma forma de organizar e reutilizar código em **models** e **controllers**. Ele é um módulo que permite agrupar lógica comum para evitar duplicação, facilitando a manutenção e organização do código.

### Uso principal do **concern**:

1. **Reutilização de código**: Compartilhar lógica entre múltiplos models ou controllers.
2. **Organização**: Separar responsabilidades e manter os arquivos mais limpos.
3. **Facilidade de manutenção**: Evita código duplicado e melhora a modularização.

---

### Como usar concern em models

Os **concerns** de models ficam no diretório `app/models/concerns/` e são incluídos nos models usando `include`.

### Exemplo:

Criando um concern para timestamps personalizados:

```ruby
# app/models/concerns/timestampable.rb
module Timestampable
  extend ActiveSupport::Concern

  included do
    before_create :set_created_at
  end

  def set_created_at
    self.created_at = Time.current
  end
end

```

Agora podemos incluir esse concern em qualquer model:

```ruby
# app/models/user.rb
class User < ApplicationRecord
  include Timestampable
end

```

---

### Como usar concern em controllers

Os **concerns** de controllers ficam no diretório `app/controllers/concerns/` e funcionam de forma similar aos de models.

### Exemplo:

Criando um concern para autenticação:

```ruby
# app/controllers/concerns/authenticatable.rb
module Authenticatable
  extend ActiveSupport::Concern

  included do
    before_action :authenticate_user!
  end

  private

  def authenticate_user!
    redirect_to login_path unless current_user
  end
end

```

Agora podemos incluir esse concern em qualquer controller:

```ruby
# app/controllers/dashboard_controller.rb
class DashboardController < ApplicationController
  include Authenticatable
end

```

---

### Resumo

- **Concerns** ajudam a manter o código DRY (Don't Repeat Yourself).
- Permitem organizar funcionalidades compartilhadas de forma modular.
- Podem ser usados tanto em models quanto em controllers.
- 