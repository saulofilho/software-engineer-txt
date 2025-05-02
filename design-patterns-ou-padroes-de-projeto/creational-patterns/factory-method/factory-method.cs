using System;

public class Car
{
    public void Drive()
    {
        Console.WriteLine("Dirigindo um carro 🚗");
    }
}

public class Bike
{
    public void Ride()
    {
        Console.WriteLine("Pedalando uma bicicleta 🚲");
    }
}

public static class VehicleFactory
{
    public static object Create(string type)
    {
        return type switch
        {
            "car" => new Car(),
            "bike" => new Bike(),
            _ => throw new ArgumentException("Tipo de veículo desconhecido")
        };
    }
}

// Uso da Factory
class Program
{
    static void Main()
    {
        var vehicle1 = VehicleFactory.Create("car") as Car;
        var vehicle2 = VehicleFactory.Create("bike") as Bike;

        vehicle1?.Drive();  // "Dirigindo um carro 🚗"
        vehicle2?.Ride();   // "Pedalando uma bicicleta 🚲"
    }
}
