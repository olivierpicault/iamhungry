# iamhungry

Check all restaurants around you and select a currently open one with a rating above 4 (by default) stars randomly

### Usage

```python
# basic usage
python iamhungry.py
```

```python
# advanced usage
python iamhungry.py address="48 rené clair paris" distance=1000 rating=4.2
```

Available params:
- distance (int): The distance between you and the place to eat
- rating (float): The minimum rating on Google
- address (string): The address you want to find a place to eat nearby


### Google API Key
The one given in this piece of code as a low qota limit. To get your own one go [here](https://console.developers.google.com/apis/library) and enable the following services / API:
- Google Maps Geocoding API
- Google Places API Web Service
- Google Maps Directions API
