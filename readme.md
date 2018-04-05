# iamhungry

Check all restaurants around you and select a currently open one with a rating above 4 (by default) stars randomly

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