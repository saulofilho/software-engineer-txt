# Criar um novo usuário
user = User.create(name: "Alice")

# Buscar um usuário
user = User.find(1)

# Atualizar um usuário
user.update(name: "Bob")

# Deletar um usuário
user.destroy
