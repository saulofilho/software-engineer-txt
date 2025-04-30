class Car
  def drive
    puts "Dirigindo um carro 🚗"
  end
end

class Bike
  def ride
    puts "Pedalando uma bicicleta 🚲"
  end
end

class VehicleFactory
  def self.create(type)
    case type
    when :car then Car.new
    when :bike then Bike.new
    else raise "Tipo de veículo desconhecido"
    end
  end
end

# Uso da Factory
vehicle1 = VehicleFactory.create(:car)
vehicle2 = VehicleFactory.create(:bike)

vehicle1.drive  # "Dirigindo um carro 🚗"
vehicle2.ride   # "Pedalando uma bicicleta 🚲"
