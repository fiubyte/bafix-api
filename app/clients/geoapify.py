import os
import urllib.parse

import requests
from requests.structures import CaseInsensitiveDict


def get_coordinates_from_address(street, street_number):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    address = street + ' ' + street_number
    address_url_encoded = urllib.parse.quote(address + ", Buenos Aires, Argentina")
    url = "https://api.geoapify.com/v1/geocode/search?text=%s&apiKey=%s" % (
        address_url_encoded, os.getenv('GEO_APIFY_API_KEY', '2ae6cb5c373c436ba6616c6b7f4b41dd'))

    resp = requests.get(url, headers=headers)
    coordinates = resp.json().get('features')[0].get('geometry').get('coordinates')
    lat = coordinates[0]
    long = coordinates[1]
    return {lat, long}
