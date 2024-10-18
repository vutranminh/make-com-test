import requests

def fetch_random_fact():
    """
    Fetches a random fact from the Numbers API.
    """
    url = "http://numbersapi.com/random/trivia"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        return f"An error occurred: {e}"

def main():
    fact = fetch_random_fact()
    print("Random Fact:")
    print(fact)

if __name__ == "__main__":
    main()
