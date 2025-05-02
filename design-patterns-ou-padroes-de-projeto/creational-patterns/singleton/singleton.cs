using System;

public sealed class Logger
{
    private static readonly Logger _instance = new Logger();

    // Construtor privado impede instanciamento externo
    private Logger() {}

    public static Logger Instance => _instance;

    public void Log(string message)
    {
        Console.WriteLine($"LOG: {message}");
    }
}

// Uso do Singleton
class Program
{
    static void Main()
    {
        var logger1 = Logger.Instance;
        var logger2 = Logger.Instance;

        logger1.Log("Isso é um Singleton!");

        Console.WriteLine(Object.ReferenceEquals(logger1, logger2));  // true
    }
}
