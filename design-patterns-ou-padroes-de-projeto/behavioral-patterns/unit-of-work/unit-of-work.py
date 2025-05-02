class UnitOfWork:
    def __init__(self):
        self._operations = []

    def register(self, operation):
        self._operations.append(operation)

    def commit(self):
        for operation in self._operations:
            operation()

# Exemplo real de uso
class UserRegistrationService:
    @staticmethod
    def call(user_params, profile_params):
        uow = UnitOfWork()

        user = User(user_params)
        profile = Profile(profile_params)

        uow.register(lambda: user.save())
        uow.register(lambda: (setattr(profile, 'user', user), profile.save()))
        uow.register(lambda: AuditLog.create("UserCreated", user.to_json()))

        uow.commit()

# Mock de classes auxiliares
class User:
    def __init__(self, params):
        pass
    def save(self):
        pass
    def to_json(self):
        return "{}"

class Profile:
    def __init__(self, params):
        self.user = None
    def save(self):
        pass

class AuditLog:
    @staticmethod
    def create(action, data):
        pass
