import pytest
from settings import valid_email, valid_password
import os
from api import pf


# Authorisation testing


@pytest.mark.api
@pytest.mark.auth
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Check if api key request returns status 200 and result has 'key' word """

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


@pytest.mark.api
@pytest.mark.auth
def test_get_api_key_with_empty_email_and_password():
    """Check if api key request with empty email and password returns 403 error"""
    status, result = pf.get_api_key()
    print(result)
    assert status == 403
    assert "This user wasn't found in database" in result


@pytest.mark.api
@pytest.mark.auth
def test_get_api_key_with_correct_email_and_empty_password(email=valid_email):
    """Check if api key request with correct email and empty password returns 403 error"""
    status, result = pf.get_api_key(email)
    print(result)
    assert status == 403
    assert "This user wasn't found in database" in result


@pytest.mark.api
@pytest.mark.auth
def test_get_api_key_with_empty_email_correct_password(password=valid_password):
    """Check if api key request with empty email and correct password returns 403 error"""
    status, result = pf.get_api_key(password=password)
    print(result)
    assert status == 403
    assert "This user wasn't found in database" in result


# List of pets

@pytest.mark.api
@pytest.mark.pet_list
def test_get_all_pets_with_valid_key(get_key, filter=""):
    """Check if pet_list request returns not an empty list. Available value for filter - 'my_pets' or '' """

    pf.status, result = pf.get_pet_list(pf.key, filter)
    assert pf.status == 200
    assert len(result['pets']) > 0


@pytest.mark.api
@pytest.mark.pet_list
def test_get_all_pets_with_invalid_key(get_incorrect_key, filter=""):
    """Check if status of pet_list request with invalid authorisation key is 403 """

    pf.status, result = pf.get_pet_list(pf.key, filter)
    assert "Please provide 'auth_key'" in result


@pytest.mark.api
@pytest.mark.pet_list
def test_get_all_pets_with_valid_key_and_invalid_filter(get_key, filter="filter"):
    """Check if status of pet_list request with invalid filter is 500. Available value for filter - 'my_pets' or '' """

    pf.status, result = pf.get_pet_list(pf.key, filter)
    assert pf.status == 500
    assert "Filter value is incorrect" in result


# Add new pet with photo

@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_with_valid_data(get_key, name='Давай', animal_type='Работай', age='3', pet_photo='images/cat1.jpg'):
    """Check possibility to add new pet with correct data"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(pf.key, name, animal_type, age, pet_photo)
    assert pf.status == 200
    assert result['name'] == name


@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_with_invalid_key(get_incorrect_key, name='Давай', animal_type='Работай', age='3',
                                      pet_photo='images/cat1.jpg'):
    """Check if add_new_pet request with invalid authorisation key returns status - 403 and result with
    the help message - "Please provide 'auth_key'" """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(pf.key, name, animal_type, age, pet_photo)
    assert "Please provide 'auth_key'" in result


@pytest.mark.skip(reason="There is a bag")
@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_with_valid_key_and_empty_info_fields(get_key, name='', animal_type='', age='',
                                                          pet_photo='images/cat1.jpg'):
    """Check if add_new_pet request with empty fields(name, animal_type, age) returns status code 400 """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(pf.key, name, animal_type, age, pet_photo)
    assert pf.status == 400


@pytest.mark.skip(reason="There is a bag")
@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_with_valid_key_and_invalid_data_in_info_fields(get_key, name='Давай' * 1000,
                                            animal_type='??<>=!@#$%^&*()', age='-3.7', pet_photo='images/cat1.jpg'):
    """Check if add_new_pet requests with invalid data(too long name, special symbols in animal_type, negative and float
    number in age) returns status code 400 - data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(pf.key, name, animal_type, age, pet_photo)
    assert pf.status == 400


@pytest.mark.skip(reason="There is a bag")
@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_with_valid_key_and_invalid_age_field(get_key, name='Давай', animal_type='Работай', age='age',
                                                          pet_photo='images/cat1.jpg'):
    """Check if add_new_pet requests with invalid data(letters in age field instead of numbers)
    returns status code 400 - data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(pf.key, name, animal_type, age, pet_photo)
    assert pf.status == 400


@pytest.mark.skip(reason="There is a bag - system does not check image format")
@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_with_unsupported_image_format(get_key, name='Давай', animal_type='Работай', age='3',
                                                   pet_photo='images/GIF.gif'):
    """Check if add_new_pet requests with unsupported image format returns status code 400 - data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.status, result = pf.add_new_pet(pf.key, name, animal_type, age, pet_photo)
    assert pf.status == 400


# Add new pet without photo

@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_without_photo_with_valid_data(get_key, name='Имя', animal_type='Тип', age='4'):
    """Check possibility to add new pet without photo with correct data"""

    pf.status, result = pf.add_new_pet_without_photo(pf.key, name, animal_type, age)
    assert pf.status == 200
    assert result['name'] == name


@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_without_photo_with_invalid_key(get_incorrect_key, name='Имя', animal_type='Тип', age='4'):
    """Check if add_new_pet_without_photo request with invalid authorisation key returns status code 403"""

    pf.status, result = pf.add_new_pet_without_photo(pf.key, name, animal_type, age)


@pytest.mark.skip(reason="There is a bag")
@pytest.mark.api
@pytest.mark.new_pet
def test_add_new_pet_without_photo_with_invalid_data(get_key, name='', animal_type='type?<>!@#$' * 1000, age='-4age'):
    """Check if add_new_pet_without_photo requests with invalid data(empty name, too long animal_type with special
    symbols, negative age with letters) returns status code 400 - data is incorrect"""

    status, result = pf.add_new_pet_without_photo(pf.key, name, animal_type, age)
    assert status == 400


# Add photo
@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.set_photo
def test_set_photo_of_pet_with_valid_data(get_key, pet_photo='images/cat1.jpg'):
    """Check possibility to add photo of existing pet"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(pf.key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(pf.key, "my_pets")

        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)

    assert pf.status == 200
    assert result['pet_photo']


@pytest.mark.api
@pytest.mark.set_photo
def test_set_photo_of_pet_with_invalid_key(get_key, pet_photo='images/cat1.jpg'):
    """Check if set_pet_photo request with invalid authorisation key returns status code 403"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pf.add_new_pet_without_photo(pf.key, name='Имя', animal_type='Тип', age='4')  # add new pet without photo
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")  # list of my_pets

    pf.key['key'] = "invalid_key"
    pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)


@pytest.mark.skip(reason="Incorrect status code comes with respond")
@pytest.mark.api
@pytest.mark.set_photo
def test_set_photo_of_pet_with_valid_key_and_invalid_pet_id(get_key, pet_photo='images/cat1.jpg'):
    """Check if set_pet_photo request with invalid pet_id returns status code 400 - provided data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        my_pets['pets'][0]['id'] = ""
        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(pf.key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(pf.key, "my_pets")
        my_pets['pets'][0]['id'] = ""

        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)

    assert pf.status == 400


@pytest.mark.skip(reason="There is a bag - system does not check image format")
@pytest.mark.api
@pytest.mark.set_photo
def test_set_photo_of_pet_with_valid_key_and_unsupported_image_format(get_key, pet_photo='images/GIF.gif'):
    """Check if set_pet_photo request with unsupported image format returns status code 400 - provided
    data is incorrect"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(pf.key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(pf.key, "my_pets")

        pf.status, result = pf.set_pet_photo(pf.key, my_pets['pets'][0]['id'], pet_photo)

    assert pf.status == 400


# Delete pet
@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.delete_pet
def test_delete_pet_with_valid_data(get_key):
    """Check possibility to delete pet with correct data"""
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")
    if len(my_pets['pets']) > 0:
        pf.status, result = pf.delete_pet(pf.key, my_pets['pets'][0]['id'])
        assert pf.status == 200
    else:
        raise Exception("There is not my pets")


@pytest.mark.api
@pytest.mark.delete_pet
def test_delete_pet_with_invalid_key(get_key):
    """Check if delete_pet request with invalid authorisation key and correct pet_id returns status code 403"""

    _, my_pets = pf.get_pet_list(pf.key, "my_pets")
    pf.key['key'] = 'invalid_key'
    if len(my_pets['pets']) > 0:
        pf.status, result = pf.delete_pet(pf.key, my_pets['pets'][0]['id'])
        assert pf.status == 403
        assert "Please provide 'auth_key'" in result
    else:
        raise Exception("There is not my pets")


@pytest.mark.skip(reason="Incorrect status code comes with respond")
@pytest.mark.api
@pytest.mark.delete_pet
def test_delete_pet_with_incorrect_pet_id(get_key):
    """Check if delete_pet request with invalid pet_id returns status code 400"""
    _, my_pets = pf.get_pet_list(pf.key, "my_pets")
    if len(my_pets['pets']) > 0:
        my_pets['pets'][0]['id'] = "incorrect_id"
        pf.status, result = pf.delete_pet(pf.key, my_pets['pets'][0]['id'])
        assert pf.status == 400
    else:
        raise Exception("There is not my pets")


# Update_pet_info
@pytest.mark.xfail(raises=RuntimeError)
@pytest.mark.api
@pytest.mark.update_pet_info
def test_update_pet_info_with_valid_data(get_key, name='New name', animal_type='type8', age='5'):
    """Check if update_pet_info request changes pet data"""

    _, my_pets = pf.get_pet_list(pf.key, "my_pets")
    if len(my_pets['pets']) > 0:
        pf.status, result = pf.update_pet_info(pf.key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert pf.status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


@pytest.mark.api
@pytest.mark.update_pet_info
def test_update_pet_info_with_invalid_key(get_key, name='New name', animal_type='type8', age='5'):
    """Check if update_pet_info request with incorrect authorisation key returns status code 403"""

    _, my_pets = pf.get_pet_list(pf.key, "my_pets")
    pf.key['key'] = 'invalid_key'
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(pf.key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 403
    else:
        raise Exception("There is no my pets")


@pytest.mark.api
@pytest.mark.skip
@pytest.mark.update_pet_info
def test_update_pet_info_with_valid_key_and_invalid_data(get_key, name='><!@#$$%^&' * 1000, animal_type='',
                                                         age='-5qwe'):
    """Check if update_pet_info request with incorrect data(too long name with special symbols, empty animal_type,
    negative age with letters) returns status code 400 - provided data is incorrect"""

    _, my_pets = pf.get_pet_list(pf.key, "my_pets")
    if len(my_pets['pets']) > 0:
        pf.status, result = pf.update_pet_info(pf.key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert pf.status == 400
    else:
        raise Exception("There is no my pets")
