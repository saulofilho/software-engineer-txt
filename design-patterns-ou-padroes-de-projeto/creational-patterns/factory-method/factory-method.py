class Car:
    def drive(self):
        print("Dirigindo um carro 🚗")

class Bike:
    def ride(self):
        print("Pedalando uma bicicleta 🚲")

class VehicleFactory:
    @staticmethod
    def create(type_):
        if type_ == "car":
            return Car()
        elif type_ == "bike":
            return Bike()
        else:
            raise ValueError("Tipo de veículo desconhecido")

# Uso da Factory
vehicle1 = VehicleFactory.create("car")
vehicle2 = VehicleFactory.create("bike")

vehicle1.drive()  # "Dirigindo um carro 🚗"
vehicle2.ride()   # "Pedalando uma bicicleta 🚲"
