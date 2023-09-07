import requests
import time
import random
#шлепает комменты без остановки по постам
access_token = '' #vk token
group_id = '' #айди сообщества
COMMENTS = [] #массив комментов

offset = 1
counter = 0

while True:
    print('===========================================================')
    time.sleep(3) # Ждем между проверками
    offset = offset + 1
    
    # Получаем информацию о  записи
    response = requests.get('https://api.vk.com/method/wall.get', params={
        'owner_id': '-' + group_id,
        'offset': offset,
        'count': 1,
        'access_token': access_token,
        'v': '5.131'
    }).json()
    new_post = response['response']['items'][0]
    print(new_post['text'])

    time.sleep(30)
    post_id = new_post['id']
    owner_id = new_post['owner_id']
    requests.post('https://api.vk.com/method/likes.add', params={
        'type': 'post',
        'owner_id': str(owner_id),
        'item_id': str(post_id),
        'access_token': access_token,
        'v': '5.131'
    })
    comment = random.choice(COMMENTS)
    requests.post('https://api.vk.com/method/wall.createComment', params={
        'owner_id': str(owner_id),
        'post_id': str(post_id),
        'message': comment,
        'access_token': access_token,
        'v': '5.131'
    })
    counter = counter + 1
    print('(+)Количество постов пролайкано: ', counter, ' Лайк и комментарий добавлены!\n')
    if counter == 100:
        exit()

