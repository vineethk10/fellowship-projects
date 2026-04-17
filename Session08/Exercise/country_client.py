import requests


class CountryClient:
    BASE_URL = "https://restcountries.com/v3.1/name"

    def __init__(self, timeout=10): 
        self.timeout = timeout
    
    def fetch(self, search_term):
        if not search_term or not search_term.strip():
            print(f"[CountryClient] Input cannot be empty.")
            return None
        
        search_term =  search_term.strip()
        url=f'{self.BASE_URL}/{search_term}'

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as network_error:
            print(f"[CountryClient] Network error fetching weather: {network_error}")
            return {}
    
    def display(self,result):
        if not result:
            print("[CountryClient] No result to display.")
            return
        
        country = result[0]
        name = country.get("name", {}).get("common", "N/A")
        official = country.get("name", {}).get("official", "N/A")

        capital_list = country.get("capital", [])
        capital = ", ".join(capital_list) if capital_list else "N/A"

        region = country.get("region", "N/A")
        subregion = country.get("subregion", "N/A")
        population = country.get("population", "N/A")

        currencies_dict = country.get("currencies", {})
        currencies = ", ".join(
            details.get("name", code)
            for code, details in currencies_dict.items()
        ) if currencies_dict else "N/A"

        languages_dict = country.get("languages", {})
        languages = ", ".join(languages_dict.values()) if languages_dict else "N/A"

        flag = country.get("flag", "")

        print("\n" + "-" * 50)
        print("RESULT")
        print(f"Country: {name} {flag}")
        print(f"Official Name: {official}")
        print(f"Capital: {capital}")
        print(f"Region: {region}")
        print(f"Subregion: {subregion}")
        print(f"Population: {population}")
        print(f"Currencies: {currencies}")
        print(f"Languages: {languages}")
        print("-" * 50)