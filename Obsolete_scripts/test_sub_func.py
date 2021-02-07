def power_generator(num):

    # Create the inner function
    def power_n(power):
        return num ** power

    return power_n

power_two = power_generator(2)
power_three = power_generator(3)
print(power_two(8))
print(power_three(4))