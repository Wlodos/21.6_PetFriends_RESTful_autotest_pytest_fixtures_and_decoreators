import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from tests.decorators import loger


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'
        self.headers = None
        self.path = None
        self.query = None
        self.request_body = None

    @loger
    def get_api_key(self, email: str = "", password: str = "") -> json:
        """Method makes a request to API and returns status of the request and result in JSON with
        unique user's key, found with email and password"""

        headers = self.headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)

        return res

    @loger
    def get_pet_list(self, auth_key: json, filter: str = "") -> json:
        """Method makes a request to API server and returns status of request and result in
        JSON with list of pets by filter. Filter can be empty - get list of all pets, or
        could be 'my_pets' - get list of own pets"""

        headers = self.headers = {'auth_key': auth_key['key']}
        filter = self.query = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)

        return res

    @loger
    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Method sends data about new pet to the server, returns status and result in JSON
         with added pet's data """

        data = self.request_body = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = self.headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)

        return res

    @loger
    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str,
                                  age: str) -> json:
        """Method sends data about new pet to the server, returns status and result in JSON
         with added pet's data"""

        data = self.request_body = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        )
        headers = self.headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        return res

    @loger
    def set_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Method sends photo to add to pet by pet_id"""

        data = self.request_body = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = self.headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        self.path = pet_id
        res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, data=data)

        return res

    @loger
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Method makes a request to delete pet by ID, returns status of request
        and result in JSON (for now result is empty string)"""

        headers = self.headers = {'auth_key': auth_key['key']}
        self.path = pet_id
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)

        return res

    @loger
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: str) -> json:
        """Method makes a request to update pet data by ID, returns status and result in JSON
        with new pet data"""

        data = self.request_body = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        )

        headers = self.headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        self.path = pet_id
        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)

        return res


pf = PetFriends()














