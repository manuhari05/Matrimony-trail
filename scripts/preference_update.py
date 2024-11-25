import random
from decimal import Decimal
from user.models import User
from user_preference.models import Preference
from tables.models import GeneralTable

def run():
    # Select a user (you can modify this to select multiple users if needed)
    users = User.objects.all()   # Replace with any logic to select the user
    
    if not users:
        print("No users found!")
        return

    for user in users:
        if user.is_admin:
            continue

        # Skip users who don't have a profile
        if not hasattr(user, 'profile'):
            print(f"No profile found for {user.username}. Skipping...")
            continue

        if Preference.objects.filter(user=user).exists():
            print(f"Preference already exists for {user.username}. Skipping...")
            continue
        # Generate or set values for preferences for each user
        preference_data = {
            'user': user,
            'gender': generate_preferred_gender(user),
            'min_age': generate_preferred_age(user),
            'max_age': generate_preferred_age(user, is_max=True),
            'min_height': generate_preferred_height(),
            'max_height': generate_preferred_height(is_max=True),
            'min_weight': generate_preferred_weight(),
            'max_weight': generate_preferred_weight(is_max=True),
            'min_income': generate_preferred_income(),
            'max_income': generate_preferred_income(is_max=True),
            'preferred_location': generate_preferred_location(user),
            'preferred_education': generate_preferred_education(user),
            'preferred_occupation': generate_preferred_occupation(user),
            'preferred_religion': generate_preferred_religion(user),
            'preferred_language': generate_preferred_language(user),
            'is_active': user.is_active,
        }

        # Create the Preference instance
        preference = Preference.objects.create(**preference_data)

        # Output the result
        print(f"Generated preference for {user.username}: {preference}")


def generate_preferred_gender(user):
    """Generate the preferred gender based on user gender."""
    if str(user.gender) == "Male":
        return "Female"  # Example: if the user is male, prefer female
    elif str(user.gender) == "Female":
        return "Male"  # If female, prefer male
    else:
        return "Other"  # For non-binary users, we can set a different preference.

def generate_preferred_age(user, is_max=False):
    """Generate a preferred age range."""
    min_age = 18  # Default minimum age
    max_age = 55  # Default maximum age
    
    if is_max:
        return random.randint(user.profile.age, max_age)  # max_age is higher than user's age
    else:
        return random.randint(min_age, user.profile.age)  # min_age is lower or equal to user's age

def generate_preferred_height(is_max=False):
    """Generate a preferred height range (in cm)."""
    min_height = 150  # Default minimum height (in cm)
    max_height = 200  # Default maximum height (in cm)
    
    if is_max:
        return random.randint(160, max_height)  # max_height is higher
    else:
        return random.randint(min_height, 170)  # min_height is lower or equal to user's height

def generate_preferred_weight(is_max=False):
    """Generate a preferred weight range (in kg)."""
    min_weight = 45  # Default minimum weight
    max_weight = 120  # Default maximum weight
    
    if is_max:
        return random.randint(50, max_weight)  # max_weight is higher
    else:
        return random.randint(min_weight, 75)  # min_weight is lower or equal to user's weight

def generate_preferred_income(is_max=False):
    """Generate a preferred income range."""
    min_income = Decimal('10000.00')  # Default minimum income
    max_income = Decimal('50000.00')  # Default maximum income
    
    if is_max:
        return Decimal(random.uniform(20000, float(max_income)))  # max income
    else:
        return Decimal(random.uniform(float(min_income), 20000))  # min income

def generate_preferred_location(user):
    """Generate a preferred location from GeneralTable matching user location."""
    # Fetch all locations from the GeneralTable
    locations = GeneralTable.objects.filter(type='location').values_list('name', flat=True)
    
    # If the user has a location preference, we can prioritize that, else choose randomly from the list
    preferred_location = user.profile.location if hasattr(user, 'profile') and user.profile.location else random.choice(locations)
    
    return preferred_location

def generate_preferred_education(user):
    """Generate a preferred education level from GeneralTable."""
    # Fetch all education levels from the GeneralTable
    educations = GeneralTable.objects.filter(type='education').values_list('name', flat=True)
    
    # If the user has an education preference, we can prioritize that, else choose randomly from the list
    preferred_education = user.profile.education if hasattr(user, 'profile') and user.profile.education else random.choice(educations)
    
    return preferred_education

def generate_preferred_occupation(user):
    """Generate a preferred occupation from GeneralTable."""
    # Fetch all occupations from the GeneralTable
    occupations = GeneralTable.objects.filter(type='profession').values_list('name', flat=True)
    
    # If the user has an occupation preference, we can prioritize that, else choose randomly from the list
    preferred_occupation = user.profile.occupation if hasattr(user, 'profile') and user.profile.occupation else random.choice(occupations)
    
    return preferred_occupation

def generate_preferred_religion(user):
    """Generate a preferred religion from GeneralTable."""
    # Fetch all religions from the GeneralTable
    religions = GeneralTable.objects.filter(type='religion').values_list('name', flat=True)
    
    # If the user has a religion preference, we can prioritize that, else choose randomly from the list
    preferred_religion = user.profile.religion if hasattr(user, 'profile') and user.profile.religion else random.choice(religions)
    
    return preferred_religion

def generate_preferred_language(user):
    """Generate a preferred language from GeneralTable."""
    # Fetch all languages from the GeneralTable
    languages = GeneralTable.objects.filter(type='language').values_list('name', flat=True)

    # If the user has a language preference, we can prioritize that, else choose randomly from the list
    preferred_language = user.profile.language if hasattr(user, 'profile') and user.profile.language else random.choice(languages)

    return preferred_language

# Call the run function to generate preferences for a user
if __name__ == "__main__":
    run()
