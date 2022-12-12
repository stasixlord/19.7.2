import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0



def test_post_new_friends(name='Patrik', animal_type='star', age='2', pet_photo='images/Patrik.jpg'):
    """Проверяем что можно добавить питомца с корректными данными (по кличке)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_friends(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_post_new_friends_2(name='Patrik', animal_type='star', age='2', pet_photo='images/Patrik.jpg'):
    """Проверяем что можно добавить питомца с корректными данными (по типу)"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_friends(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == animal_type

def test_post_new_friends_3(name='Patrik', animal_type='star', age='2', pet_photo='images/Patrik.jpg'):
    """Проверяем что можно добавить питомца с корректными данными (по возрасту)"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_friends(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age

def test_post_new_friends_4(name='Patrik', animal_type='star', age='2', pet_photo='images/Patrik.jpg'):
    """Проверяем что можно добавить питомца с корректными данными (по фото)"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_friends(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] != pet_photo

def test_delete_pet():
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять
    # запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_new_friends(auth_key, "Snuppy", "dog", "5", "images/korgi.jpg")
        # pf.post_new_friends(auth_key, name='Snuppy', animal_type='dog', age='5', pet_photo='images/korgi.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_delete_pet_2(name='Patrik', animal_type='star', age='2'):
    """Проверяем возможность удаления клички питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.put_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert name not in pet_id


def test_delete_pet_3(name='Patrik', animal_type='star', age='2'):
    """Проверяем возможность удаления type питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.put_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert animal_type not in pet_id


def test_put_self_pet_info(name='PatrikStar', animal_type='star', age='2'):
    """Проверяем возможность обновления информации о кличке питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.put_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_put_self_pet_info_2(name='Patrik', animal_type='baby star', age='2'):
    """Проверяем возможность обновления информации о виде питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.put_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)
    assert status == 200
    assert result['animal_type'] == animal_type


def test_put_self_pet_info_3(name='Patrik', animal_type='star', age='700'):
    """Проверяем возможность обновления информации о возрасте питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.put_pet_info(auth_key, my_pets['pets'][2]['id'], name, animal_type, age)
    assert status == 200
    assert result['age'] == age
