import numpy as np
from scipy.stats import norm


def calculate_target_audience(
        total_population,
        foreign_percentage,
        age_distribution,
        homeownership_rates,
        education_rate,
        social_media_usage_sarah,
        social_media_usage_non_sarah,
        margin_of_errors
):
    """
    Calculates the effective reach for different target audience segments based on given statistical inputs.
    """

    # Step 1: Remove foreign nationals
    foreign_population = total_population * (foreign_percentage / 100)
    austrian_citizens = total_population - foreign_population

    # Step 2: Estimate target age groups in Freistadt based on national distribution
    age_group_population = {
        age: pop * (austrian_citizens / 9000000) for age, pop in age_distribution.items()
    }

    # Step 3: Apply homeownership filter
    homeowners_by_age = {
        age: age_group_population[age] * homeownership_rates[age]
        for age in age_distribution.keys()
    }
    total_homeowners = sum(homeowners_by_age.values())

    # Step 4: Apply education filter
    homeowners_higher_ed = {
        age: homeowners_by_age[age] * education_rate for age in homeowners_by_age.keys()
    }

    # Step 5: Define segments
    sarah_population = homeowners_by_age["30-34"] + homeowners_by_age["35-39"]
    non_sarah_population = sum(
        homeowners_by_age[age] for age in homeowners_by_age.keys() if age not in ["30-34", "35-39"]
    )

    sarah_population_higher_ed = homeowners_higher_ed["30-34"] + homeowners_higher_ed["35-39"]
    non_sarah_population_higher_ed = sum(
        homeowners_higher_ed[age] for age in homeowners_higher_ed.keys() if age not in ["30-34", "35-39"]
    )

    # Step 6: Calculate social media reach
    effective_sarah_reach = sarah_population * (1 - np.prod([1 - p for p in social_media_usage_sarah.values()]))
    effective_non_sarah_reach = non_sarah_population * (
                1 - np.prod([1 - p for p in social_media_usage_non_sarah.values()]))

    effective_sarah_reach_higher_ed = sarah_population_higher_ed * (
                1 - np.prod([1 - p for p in social_media_usage_sarah.values()]))
    effective_non_sarah_reach_higher_ed = non_sarah_population_higher_ed * (
                1 - np.prod([1 - p for p in social_media_usage_non_sarah.values()]))

    # Step 7: Compute final margin of error (weighted combination of input errors)
    combined_margin_of_error = np.sqrt(sum([error ** 2 for error in margin_of_errors.values()]))

    # Output results
    results = {
        "Sarah_Effective_Reach": effective_sarah_reach,
        "Non_Sarah_Effective_Reach": effective_non_sarah_reach,
        "Sarah_Effective_Reach_Higher_Ed": effective_sarah_reach_higher_ed,
        "Non_Sarah_Effective_Reach_Higher_Ed": effective_non_sarah_reach_higher_ed,
        "Margin_of_Error": combined_margin_of_error
    }

    return results


# Example input data
total_population = 72462  # Freistadt population
foreign_percentage = 3.6  # Percentage of foreign nationals
age_distribution = {
    "30-34": 321471 + 307544,
    "35-39": 318121 + 308328,
    "40-44": 312960 + 308711,
    "45-49": 289004 + 289029,
    "50-54": 317491 + 324150,
    "55-59": 357812 + 358600,
    "60-64": 330858 + 338782,
}
homeownership_rates = {
    "30-34": 0.35,
    "35-39": 0.50,
    "40-44": 0.60,
    "45-49": 0.70,
    "50-54": 0.75,
    "55-59": 0.80,
    "60-64": 0.85,
}
education_rate = 0.304  # Percentage with higher education
social_media_usage_sarah = {
    "YouTube": 0.90,
    "Facebook": 0.90,
    "Instagram": 0.95,
    "LinkedIn": 0.60,
}
social_media_usage_non_sarah = {
    "YouTube": 0.75,
    "Facebook": 0.85,
    "Instagram": 0.70,
    "LinkedIn": 0.40,
}
margin_of_errors = {
    "Demographic Assumptions": 0.05,
    "Social Media Behavior": 0.06,
    "Homeownership Estimation": 0.05,
    "Education Filter": 0.04,
}

# Running the function
results = calculate_target_audience(
    total_population,
    foreign_percentage,
    age_distribution,
    homeownership_rates,
    education_rate,
    social_media_usage_sarah,
    social_media_usage_non_sarah,
    margin_of_errors
)

# Displaying results
print("Final Results:")
for key, value in results.items():
    print(f"{key}: {value:.2f}")
