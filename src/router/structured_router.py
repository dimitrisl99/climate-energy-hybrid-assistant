from src.structured_query.co2_query_engine import (
    latest_year_with_co2,
    top_emitters,
    country_emissions,
    compare_countries,
    get_available_countries,
)

def extract_countries_from_query(user_query: str) -> list[str]:
    query = user_query.lower()
    available_countries = get_available_countries()

    matched_countries = []

    for country in available_countries:
        if country.lower() in query:
            matched_countries.append(country)

    return matched_countries

def route_structured_query(user_query: str):
    query = user_query.lower()
    latest_year = latest_year_with_co2()

    if "top" in query and ("emitters" in query or "emissions" in query):
        return top_emitters(latest_year, 10)

    if "greece" in query and ("emissions" in query or "co2" in query):
        return country_emissions("Greece").tail(10)

    if "compare" in query:
        countries = extract_countries_from_query(user_query)

        if countries:
            return compare_countries(countries, latest_year)

    return "I could not route this query yet."


if __name__ == "__main__":
    test_queries = [
        "show me the top emitters",
        "show me greece co2 emissions",
        "compare greece germany france",
        "compare china united states india",
        "compare japan brazil canada",
    ]

    for q in test_queries:
        print(f"\nUSER QUERY: {q}")
        print(route_structured_query(q))

