from py_ms_cognitive import PyMsCognitiveWebSearch


def read_bing_key():
    """
    Reads the BING API key from a file called 'bing.key'.
    returns: a string which is either None, i.e. no key found, or with a key.
     Remember: put bing.key in your .gitignore file to avoid committing it!
    """
    bing_api_key = None
    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError('bing.key not found')

    return str(bing_api_key)


def run_query(search_terms):
    bing_api_key = read_bing_key()
    if not bing_api_key:
        raise KeyError("Bing Key Not Found")

    # Create our results list which we'll populate.
    results = []
    # Custom params
    params = 'mkt=ru-RU'

    try:
        search_service = PyMsCognitiveWebSearch(bing_api_key, search_terms, custom_params=params)
        json_response = search_service.search(limit=11, format='json')  # 1 - 10

    except:
        print("Error when querying the Bing API")

    # Loop through each page returned, populating out results list.
    # dict_keys(['json', 'deep_links', 'snippet', 'url', 'title', 'name', 'description', 'id', 'display_url'])
    for idx in range(11):
        results.append({'title': json_response[idx].title,
                        'link': json_response[idx].display_url,
                        'summary': json_response[idx].description})

    return results


def main():
    query = input("Enter a query: ")
    results = run_query(query)
    for result in results:
        print(result['title'])
        print('-' * len(result['title']))
        print(result['summary'])
        print(result['link'])
        print()

if __name__ == '__main__':
    main()
