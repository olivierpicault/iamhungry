import json
import random
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf8')

DEFAULT_ADDRESS = '54 Rue Greneta Paris'

google_api_key = 'AIzaSyDV0CBU7zCJD5GZkwHMb2ww8nZt2AbgERs'  # Please use you own API key
google_places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={api_key}&location={lat},{lon}&radius={distance}&type={type}'
google_geocofing_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
google_directions_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=walking&key={api_key}'


def main():
    # Parse params
    params = {}
    for argv in sys.argv[1:]:
        data = argv.split('=')
        params[data[0]] = data[1]

    # Params
    address = params.get('address', DEFAULT_ADDRESS)
    place_type = 'restaurant'  # https://developers.google.com/places/supported_types
    distance = params.get('distance', 500)
    extra = params.get('extra', False)

    lat, lon = getLatLon(address)
    restaurants = getPlaces(lat, lon, place_type, distance)

    venues = [
        res for res in restaurants if res.get('rating') >= float(params.get('rating', 4)) and (
            res.get('opening_hours').get('open_now')
            if 'opening_hours' in res and 'open_now' in res.get('opening_hours')
            else False
        )
    ]

    possible_venues = len(venues)

    if len(venues) > 0:
        selected = random.choice(venues)
        distance, duration = getDistanceDuration(address, selected.get('vicinity'))
        pas = getPas(distance)
        print '{} ({})'.format(selected.get('name'), selected.get('rating'))
        print selected.get('vicinity')
        print '{} - {} - {} pas'.format(distance, duration, pas)
        if extra:
            print 'chosen between {} possibles venues'.format(possible_venues)
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
    res = req.json()

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
    res = req.json()

    location = res.get('results')[0].get('geometry').get('location')
    lat = location.get('lat')
    lon = location.get('lng')

    return lat, lon


def getDistanceDuration(origin, destination):
    url = google_directions_url.format(
        origin=origin,
        destination=destination,
        api_key=google_api_key
    )
    req = requests.get(url)
    res = req.json()

    data = res["routes"][0]["legs"][0]

    distance = data['distance']['text']
    duration = data['duration']['text']

    return distance, duration


def getPas(distance):
    return int(float(distance.replace('km', '')) * 1.75 * 1000)


if __name__ == '__main__':
    main()
