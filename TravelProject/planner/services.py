import requests


class ExternalAPIError(Exception):
    pass


def get_artworks_data(page, limit=10):
    url = "https://api.artic.edu/api/v1/artworks/search"

    response = requests.get(url, timeout=10, params={
        "page": page,
        "limit": limit,
    })

    return response.json()


def get_title_by_external_id(external_id):

    try:
        url = f'https://api.artic.edu/api/v1/artworks/{external_id}'
        response = requests.get(url, timeout=10)

        response.raise_for_status()
        
        data = response.json()
        title = data.get("data", {}).get("title")

        if not title:
            raise ExternalAPIError(f"Missing title")
        
    except requests.RequestException as e:
        raise ExternalAPIError(f"Can not get data from internal API \n Failed on external_id: {external_id} \n error: {str(e)}") from e

    if not title:
        raise ExternalAPIError('Title not returned')
    
    return title



if __name__ == '__main__':
    titles_list = get_title_by_external_id(75644)#75644, 86385, 151363, 20684
    print('\n'.join(titles_list))