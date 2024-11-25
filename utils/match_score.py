def calculate_match_score(user1, user2):
    """Calculate match score based on preferences and return it as a percentage."""
    try:
        # Check if both users have preferences and profiles
        if not hasattr(user1, 'preference') or not hasattr(user2, 'preference'):
            return 0  # Return 0 if either user doesn't have preferences
        
        if not hasattr(user1, 'profile') or not hasattr(user2, 'profile'):
            return 0  # Return 0 if either user doesn't have a profile

        score = 0
        max_score = 0
        
        # Get user preferences
        preference1 = user1.preference
        preference2 = user2.preference

        # Gender preference
        if preference1.gender and preference2.gender and preference1.gender == preference2.gender:
            score += 10
        max_score += 10

        # Age preference
        if user2.date_of_birth and hasattr(user2, 'profile') and hasattr(user2.profile, 'age'):
            if preference1.min_age and preference1.max_age and user2.profile.age:
                if preference1.min_age <= user2.profile.age <= preference1.max_age:
                    score += 10
            max_score += 10

        # Height preference
        if hasattr(user2, 'profile') and hasattr(user2.profile, 'height'):
            if preference1.min_height and preference1.max_height and user2.profile.height:
                if preference1.min_height <= user2.profile.height <= preference1.max_height:
                    score += 10
            max_score += 10

        # Weight preference
        if hasattr(user2, 'profile') and hasattr(user2.profile, 'weight'):
            if preference1.min_weight and preference1.max_weight and user2.profile.weight:
                if preference1.min_weight <= user2.profile.weight <= preference1.max_weight:
                    score += 10
            max_score += 10

        # Income preference
        if hasattr(user2, 'profile') and hasattr(user2.profile, 'income'):
            if preference1.min_income and preference1.max_income and user2.profile.income:
                if preference1.min_income <= user2.profile.income <= preference1.max_income:
                    score += 10
            max_score += 10

        # Location preference
        if (hasattr(user2, 'profile') and hasattr(user2.profile, 'location') and 
            preference1.preferred_location and user2.profile.location):
            if preference1.preferred_location == user2.profile.location:
                score += 10
            max_score += 10

        # Occupation preference
        if (hasattr(user2, 'profile') and hasattr(user2.profile, 'occupation') and 
            preference1.preferred_occupation and user2.profile.occupation):
            if preference1.preferred_occupation == user2.profile.occupation:
                score += 5
            max_score += 5

        # Religion preference
        if (hasattr(user2, 'profile') and hasattr(user2.profile, 'religion') and 
            preference1.preferred_religion and user2.profile.religion):
            if preference1.preferred_religion == user2.profile.religion:
                score += 5
            max_score += 5
        
        # Mother tongue preference
        if (hasattr(user2, 'profile') and hasattr(user2.profile, 'mother_tongue') and
            preference1.preferred_language and user2.profile.mother_tongue):
            if preference1.preferred_language == user2.profile.mother_tongue:
                score += 5
            max_score += 5

        # Calculate percentage
        if max_score > 0:
            match_percentage = (score / max_score) * 100
        else:
            match_percentage = 0

        return match_percentage

    except Exception as e:
        # Log the error if you have logging set up
        print(f"Error calculating match score: {str(e)}")
        return 0

