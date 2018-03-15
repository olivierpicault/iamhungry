# coding: utf-8
import json
import random

import requests

google_api_key = 'AIzaSyDV0CBU7zCJD5GZkwHMb2ww8nZt2AbgERs'
google_places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={api_key}&location={lat},{lon}&radius={distance}&type={type}'
google_geocofing_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'


def main():
    lat, lon = getLatLon('48 rue rené clair paris')
    place_type = 'restaurant'  # https://developers.google.com/places/supported_types
    distance = 500  # meters

    restaurants = getPlaces(lat, lon, place_type, distance)

    venues = [
        res for res in restaurants if res.get('rating') > 4 and (
            res.get('opening_hours').get('open_now')
            if 'opening_hours' in res and 'open_now' in res.get('opening_hours')
            else False
        )
    ]

    if len(venues) > 0:
        selected = random.choice(venues)
        print selected.get('name') + ' (' + str(selected.get('rating')) + ')'
        print selected.get('vicinity')
    else:
        print 'no place found'


def getPlaces(lat, lon, place_type, distance):
    """
    Returns a list of places given some args
    Doc: https://developers.google.com/places/web-service/search
    """
    url = google_places_url.format(
        api_key=google_api_key,
        lat=lat,
        lon=lon,
        type=place_type,
        distance=distance
    )
    req = requests.get(url)
    res = json.loads(req.text)

    return res.get('results')


def getLatLon(address):
    """
    Returns the latitude and the longitude for a given address
    Doc: https://developers.google.com/maps/documentation/geocoding/start
    """
    url = google_geocofing_url.format(
        address=address,
        api_key=google_api_key
    )
    req = requests.get(url)
    res = json.loads(req.text)

    data = res.get('results')[0].get('geometry')
    lat = data.get('location').get('lat')
    lon = data.get('location').get('lng')

    return lat, lon


if __name__ == '__main__':
    main()
