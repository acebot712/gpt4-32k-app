import requests

def search_ddg(query):
    url = 'https://api.duckduckgo.com/?q={}&format=json'

    response = requests.get(url=url.format(query))

    if response.json()['Abstract'] == "":
        return "No summary found for this query"
    
    return response.json()['Abstract']

if __name__ == '__main__':
    summary = search_ddg("Python Programming")
    print(summary)
