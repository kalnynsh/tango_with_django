import json
import urllib.request
import urllib.parse


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
    return bing_api_key


def run_query(search_terms):
    """
    Given a string containing search terms (query),
    returns a list of results from the Bing search engine.
    """
    bing_api_key = read_bing_key()
    if not bing_api_key:
        raise KeyError("Bing Key Not Found")

    # Spesify the base url (/bing/v5.0/search)
    root_url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'
    # service = 'Web' Not use in v.5.0

    # Specify how many results we wish to be returned per page.
    # Offset specifies where in the results list to start from.
    # With results_per_page = 10 and offset = 11,
    # this would start from page 2.
    results_per_page = 10
    offset = 0
    mkt = 'ru-RU'  # market place Russia
    safesearch = 'Moderate'

    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stores within variable query.
    query = "'{0}'".format(search_terms)

    # Turn the query into an HTML encoded string, using urllib
    # Use the line relevant to your version of Python.
    query = urllib.parse.quote(query)

    # Construct the latter part of our request's URL.
    # Sets the format of the response to JSON and set other properties.
    search_url = "{0}?$format=json&$count={1}&$offset={2}" \
                 "&mkt={3}&safesearch={4}&q={5}".format(
                    root_url,
                    results_per_page,
                    offset,
                    mkt,
                    safesearch,
                    query, )

    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''

    # Setup a password manager to help authenticate our request.
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    password_mgr.add_password(None, search_url, username, bing_api_key)

    # Create our results list which we'll populate.
    results = []

    try:
        # Prepare for connecting to Bing's servers.
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

        # Connect to the server and read the response generated.
        response = urllib.request.urlopen(search_url).read()
        response = response.decode('utf-8')

        # Convert the string response to a Python dictionary object.
        json_response = json.loads(response)

        # Loop through each page returned, populating out results list.
        for result in json_response['d']['results']:
            results.append({'title': result['Title'],
                            'link': result['Url'],
                            'summary': result['Description']})
    except:
        print("Error when querying the Bing API")

        # Return the list of results to the calling function.
    return results


def main():
    query = input("Enter a query:")
    results = run_query(query)
    for result in results:
        print(result['title'])
        print('-' * len(result['title']))
        print(result['summary'])
        print(result['link'])
        print()

if __name__ == '__main__':
    main()
