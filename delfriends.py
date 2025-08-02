import time
import vk_api

settings = {
    'login': '+ ',
    'password': ' ',
    'shutdown_time': 10,        
    'delay_between_deletes': 0.3  
}

def auth(login, password):
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    return vk_session.get_api()

def get_all_friends(vk):
    user_id = vk.account.getProfileInfo()['id']
    friends = vk.friends.get(user_id=user_id)
    return friends['items']

def delete_everyone(vk):
    all_ids = get_all_friends(vk)
    print(f'Всего друзей для удаления: {len(all_ids)}')
    
    for uid in all_ids:
        try:
            result = vk.friends.delete(user_id=uid)
            print(f'Удалён: https://vk.com/id{uid} → {result}')
            time.sleep(settings['delay_between_deletes'])
        except vk_api.exceptions.ApiError as e:
            print(f'Ошибка при удалении id{uid}: {e}')
    
    print(f'Удаление завершено. Выключение через {settings["shutdown_time"]} секунд')
    time.sleep(settings['shutdown_time'])

# запуск
if __name__ == '__main__':
    vk = auth(settings['login'], settings['password'])
    delete_everyone(vk)
