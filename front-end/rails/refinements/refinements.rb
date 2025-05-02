# Refinements modify classes temporarily.

module StringRefinements
  refine String do
    def shout
      upcase + "!!!"
    end
  end
end

using StringRefinements
puts "hello".shout  # HELLO!!!
