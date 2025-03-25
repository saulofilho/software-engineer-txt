# Antes de aplicar DIP
class LightBulb
  def turn_on
    puts "Bulb is on"
  end

  def turn_off
    puts "Bulb is off"
  end
end

class Switch
  def initialize(bulb)
    @bulb = bulb
  end

  def operate
    @bulb.turn_on
  end
end

# Depois de aplicar DIP
class Switchable
  def turn_on; end
  def turn_off; end
end

class LightBulb < Switchable
  def turn_on
    puts "Bulb is on"
  end

  def turn_off
    puts "Bulb is off"
  end
end

class Switch
  def initialize(device)
    @device = device
  end

  def operate
    @device.turn_on
  end
end
