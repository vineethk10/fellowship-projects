from dotenv import load_dotenv

from country_client import CountryClient
from result_saver import ResultSaver


def main():
    load_dotenv()

    client = CountryClient(timeout=10)
    saver = ResultSaver("country_results.json")

    user_input = input("Enter a country name: ")

    result = client.fetch(user_input)
    client.display(result)
    saver.save(user_input, result)


if __name__ == "__main__":
    main()