import json
import urllib.parse
import urllib.request
import os.path


def read_web_key():
    """
    Reads the Webhose API key from a file called 'search.key'.
    Returns either None (no key found), or a string representing the key.
    Remember: put search.key in your .gitirnor file to avoid committing it!
    """
    webhose_api_key = None
    file_search_key = 'search.key'

    # Find abs path to file_search_key
    abspath_file_search_key = os.path.abspath(file_search_key)

    # Check out isfile exist
    if not os.path.isfile(abspath_file_search_key):
        # ../ go up stair
        abspath_updir_search_key = os.path.dirname(os.path.dirname(abspath_file_search_key))
        abspath_file_search_key = os.path.join(abspath_updir_search_key, file_search_key)

    try:
        with open(abspath_file_search_key, 'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key


def run_query(search_term, size=10):
    """
    Given a string containing search terms (query), and a number of results to
    return (default of 10), returns a list of results from the Webhose API,
    with each result consisting of a title, link and summery.
    :param search_term: str
    :param size: int
    :return: list
    """
    webhose_api_key = read_web_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'

    # Format the query string - escape special characters.
    query_string = urllib.parse.quote(search_term)

    # Use string formatting to construct the complete API URL
    # search_url is a string split over multiple lines.
    search_url = ('{root_url}?token={key}&format=json&q={query}'
                  '&sort=relevancy&size={size}').format(
        root_url=root_url,
        key=webhose_api_key,
        query=query_string,
        size=size,
    )

    results = []

    try:
        # Connect to the Webhose API, and convert the response to
        # a Python dictionary.
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        # Loop through the posts, appending each to the results list as
        # a dictionary. We restrict the summery to the first 200
        # characters, as summery responses from Webhose can be long!
        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link': post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    # Return the list of results to the calling function.
    return results


def main():
    query = input("Enter a query: ")
    results = run_query(query)
    for result in results:
        print('-' * len(result['title']))
        print(result['title'])
        print(result['summary'])
        print(result['link'])
        print()

if __name__ == '__main__':
    main()
