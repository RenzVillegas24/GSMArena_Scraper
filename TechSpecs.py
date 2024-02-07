import requests


'''
SCRAP THE IDEA OF USING THIS API, IT IS NOT FREE
20 requests per day
'''



url = "https://api.techspecs.io/v4/product/detail?productId=641c42d2f82d4186aad7a5cd"

headers = {
    "accept": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImN1c19QUG5xWlV3UW15WnZ6cSIsIm1vZXNpZlByaWNpbmdJZCI6InByaWNlXzFNUXF5dkJESWxQbVVQcE1SWUVWdnlLZSIsImlhdCI6MTcwNTgzMjc4OX0.BETbBJQMD3hFzAeDz3PdsKZ46rZ27dQqF27Y1JyXRm4"
}

response = requests.get(url, headers=headers)

print(response.text)




class TechSpecs:
    def __init__(self):
        self._API_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImN1c19QUG5xWlV3UW15WnZ6cSIsIm1vZXNpZlByaWNpbmdJZCI6InByaWNlXzFNUXF5dkJESWxQbVVQcE1SWUVWdnlLZSIsImlhdCI6MTcwNTgzMjc4OX0.BETbBJQMD3hFzAeDz3PdsKZ46rZ27dQqF27Y1JyXRm4"
        self._BASE_URL = "https://api.techspecs.io/v4/product/detail?productId="