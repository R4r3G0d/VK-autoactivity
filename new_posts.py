import requests
import time
import random

#комменты и лайки только на новые посты

access_token = '' #vk token
group_id = '' #айди сообщества
COMMENTS = [] #массив комментов

# Получаем информацию о первой не закрепленной записи

offset = 1 #есть закреп = 1, нет закрепа 0
counter = 0 #просто счетчик для статистики
commentId= 0 #если хочешь по порядку массив комментов, иначе можно удалить и раскоментить рандом
response = requests.get('https://api.vk.com/method/wall.get', params={
    'owner_id': '-' + group_id,
    'offset': offset,
    'count': 1,
    'access_token': access_token,
    'v': '5.131'
}).json()
old_post = response['response']['items'][0]

while True:

    time.sleep(5) # Ждем 5 секунд между проверками

    # Получаем информацию о новой записи
    response = requests.get('https://api.vk.com/method/wall.get', params={
        'owner_id': '-' + group_id,
        'offset': offset,
        'count': 1,
        'access_token': access_token,
        'v': '5.131'
    }).json()
    new_post = response['response']['items'][0]
    # Сравниваем новую запись со старой по параметрам
    if new_post['id'] == old_post['id']:
        print('Новых записей нет')
        print(random.random())
        continue
    
    # Если есть новая запись, выполняем действия
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Найдена новая запись!', new_post['text'])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~')
    time.sleep(40)
    post_id = new_post['id']
    owner_id = new_post['owner_id']
    requests.post('https://api.vk.com/method/likes.add', params={
        'type': 'post',
        'owner_id': str(owner_id),
        'item_id': str(post_id),
        'access_token': access_token,
        'v': '5.131'
    })
    comment = COMMENTS[commentId] #по счетчику
    #comment = random.choice(COMMENTS) #рандом
    requests.post('https://api.vk.com/method/wall.createComment', params={
        'owner_id': str(owner_id),
        'post_id': str(post_id),
        'message': comment,
        'access_token': access_token,
        'v': '5.131'
    })
    counter = counter + 1 #статисткиа
    commentId = commentId + 1 #шаг коммента
    if commentId == len(COMMENTS):
        commentId = 0
    print(comment,'\n(+)коммент айди: ', commentId, ' Лайк и комментарий добавлены!\n', 'длина массива:', len(COMMENTS))

    # Запоминаем новую запись
    old_post = new_post

