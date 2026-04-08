# Session 1: 04/07/2026

def main():

    def convert_length(meters):
        feet = meters * 3.28084
        return feet
    def convert_weight(kilograms):
        pounds = kilograms * 2.20462
        return pounds
    def convert_temperature(celsius):
        fahrenheit = (celsius * 9/5) + 32
        return fahrenheit

    print("=" * 50)
    print("Welcome to the Unit Converter!")
    print("=" * 50)

    print("\n Choose a conversion type:")
    print("1. Length (meters to feet)")
    print("2. Weight (kilograms to pounds)")
    print("3. Temperature (Celsius to Fahrenheit)")

    conversion_choice = input("\nEnter your choice (1, 2, or 3): ")

    if conversion_choice == '1':
        meters = float(input("\nEnter the length in meters: "))
        feet = convert_length(meters)
        print(f"{meters} meters is equal to {feet:.2f} feet.")
    elif conversion_choice == '2':
        kilograms = float(input("\nEnter the weight in kilograms: "))
        pounds = convert_weight(kilograms)
        print(f"{kilograms} kilograms is equal to {pounds:.2f} pounds.")
    elif conversion_choice == '3':
        celsius = float(input("\nEnter the temperature in Celsius: "))
        fahrenheit = convert_temperature(celsius)
        print(f"{celsius} degrees Celsius is equal to {fahrenheit:.2f} degrees Fahrenheit.")
    else:
        print("Invalid choice. Please select a valid conversion type.")

if __name__ == "__main__":
    main()