from calculations import calculate_target_audience, calculate_budget

# Define input data (example values)
total_population = 72462
foreign_percentage = 3.6
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
education_rate = 0.304  # Higher education percentage

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

# Calculate audience estimates
audience_results = calculate_target_audience(
    total_population, foreign_percentage, age_distribution,
    homeownership_rates, education_rate, social_media_usage_sarah,
    social_media_usage_non_sarah, margin_of_errors
)

print("Audience Estimation Results:")
for key, value in audience_results.items():
    print(f"{key}: {value:.2f}")

# Define CPM and budget inputs
cpm_ranges = {
    "Google Display": (5, 10),
    "YouTube": (10, 20),
    "Meta (Facebook/Instagram)": (10, 20),
    "LinkedIn": (30, 50)
}

# Define ad frequency per user per month (adjust as needed)
ad_frequency_per_month = 10  

# Adjusted audience sizes (example)
adjusted_target_audience_splits = {
    "Sarah (höhere Bildung)": audience_results["Sarah_Effective_Reach_Higher_Ed"],
    "Nicht-Sarah (höhere Bildung)": audience_results["Non_Sarah_Effective_Reach_Higher_Ed"],
    "Alle ohne höhere Bildung": total_population - audience_results["Sarah_Effective_Reach_Higher_Ed"] - audience_results["Non_Sarah_Effective_Reach_Higher_Ed"]
}

# Generate 12-month period
from datetime import datetime, timedelta
start_date = datetime(2025, 5, 1)
months = [start_date + timedelta(days=30 * i) for i in range(12)]

# Calculate budget
budget_results = calculate_budget(adjusted_target_audience_splits, cpm_ranges, ad_frequency_per_month, months)

print("\nBudget Estimation Results (for one month):")
for key, (min_budget, expected_budget, max_budget) in budget_results.items():
    print(f"{key}: Min: {min_budget:.2f} €, Expected: {expected_budget:.2f} €, Max: {max_budget:.2f} €")