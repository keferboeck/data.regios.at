import numpy as np
import pandas as pd
from datetime import datetime, timedelta


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
        "Sarah_Effective_Reach": round(effective_sarah_reach),
        "Non_Sarah_Effective_Reach": round(effective_non_sarah_reach),
        "Sarah_Effective_Reach_Higher_Ed": round(effective_sarah_reach_higher_ed),
        "Non_Sarah_Effective_Reach_Higher_Ed": round(effective_non_sarah_reach_higher_ed),
        "Margin_of_Error": round(combined_margin_of_error, 2)
    }

    return results


def calculate_budget(
        adjusted_target_audience_splits, cpm_ranges, ad_frequency_per_month, months
):
    """Calculates the advertising budget per month for each platform and target group."""
    monthly_budget_summary = {}

    for platform, (cpm_min, cpm_max) in cpm_ranges.items():
        for audience, size in adjusted_target_audience_splits.items():
            min_budget = round((size * ad_frequency_per_month / 1000) * cpm_min)
            expected_budget = round((size * ad_frequency_per_month / 1000) * ((cpm_min + cpm_max) / 2))
            max_budget = round((size * ad_frequency_per_month / 1000) * cpm_max)
            monthly_budget_summary[f"{platform} - {audience}"] = (min_budget, expected_budget, max_budget)

    return monthly_budget_summary


def calculate_retargeting_budget(
        adjusted_target_audience_splits, cpm_values, ad_frequency_per_month, interest_levels
):
    """Calculates the retargeting budget for different interest scenarios."""
    retargeting_budget_summary = {}

    for level in interest_levels:
        retargeting_budget_summary[level] = {}
        for platform, avg_cpm in cpm_values.items():
            for audience, size in adjusted_target_audience_splits.items():
                adjusted_size = size * level
                budget = round((adjusted_size * ad_frequency_per_month / 1000) * avg_cpm)
                retargeting_budget_summary[level][f"{platform} - {audience}"] = budget

    return retargeting_budget_summary


# Placeholder function for Google Looker API connection
def connect_to_looker(api_key, api_secret):
    """Sets up a connection to Google Looker API. User must provide API credentials."""
    print("Google Looker API connection is not yet active. Add your credentials to enable it.")
    return None


if __name__ == "__main__":
    print("This script contains functions for audience estimation, budget calculation, and retargeting analysis.")
    print("It also includes a Google Looker API placeholder for future data integration.")
