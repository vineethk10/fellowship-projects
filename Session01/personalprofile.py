# Session 1: 04/05/2026
print("Welcome to the Personal Profile Generator!")
print("Answer the following questions to create your personal profile. \n")
name = input("What is your name? ").strip()
city = input("Which city do you live in? ").strip()
age = input("How old are you? ").strip()
user_age = int(age)
goal = input("What is your main goal in life? ").strip()
hobby = input("What is your favorite hobby? ").strip()
height = float(input("What is your height? "))
profile = f"""
==========================================================================
                           Personal Profile
==========================================================================
                        Name:               {name}
                        City:               {city}
                        Age:                {age} years
                        Height:             {height} inches
                        Hobby:              {hobby}
                        Goal:               {goal}
==========================================================================
"""
print(profile)
print("Thank you for using the Personal Profile Generator!")