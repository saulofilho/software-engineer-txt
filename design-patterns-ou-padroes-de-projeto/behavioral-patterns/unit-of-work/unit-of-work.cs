using System;
using System.Collections.Generic;

public class UnitOfWork
{
    private readonly List<Action> _operations = new List<Action>();

    public void Register(Action operation)
    {
        _operations.Add(operation);
    }

    public void Commit()
    {
        foreach (var operation in _operations)
        {
            operation();
        }
    }
}

// Exemplo real de uso
public class UserRegistrationService
{
    public static void Call(Dictionary<string, object> userParams, Dictionary<string, object> profileParams)
    {
        var uow = new UnitOfWork();

        var user = new User(userParams);
        var profile = new Profile(profileParams);

        uow.Register(() => user.Save());
        uow.Register(() => { profile.User = user; profile.Save(); });
        uow.Register(() => AuditLog.Create("UserCreated", user.ToJson()));

        uow.Commit();
    }
}

// Mock de classes auxiliares
public class User
{
    public User(Dictionary<string, object> parameters) { /* atribuição */ }
    public void Save() { /* salvar no DB */ }
    public string ToJson() => "{}";
}

public class Profile
{
    public User User { get; set; }
    public Profile(Dictionary<string, object> parameters) { }
    public void Save() { }
}

public static class AuditLog
{
    public static void Create(string action, string data) { }
}
