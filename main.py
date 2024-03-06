import time
from smsactivate.api import SMSActivateAPI
import pyautogui
import os
from argparse import ArgumentParser
parser = ArgumentParser(description='Бот для регистрации с помощью виртуального номера.')
parser.add_argument('-t', '--token', type=str, help='Токен SMSActivateAPI.')
if not args.token:
    parser.error('Аргумент токена является обязательным. (-t TOKEN или --token TOKEN), --help для дополнительной информации.')

API_KEY = args.token
sa = SMSActivateAPI(API_KEY)
os.system("paplay /usr/share/sounds/freedesktop/stereo/power-plug.oga")
timer_clock = 120
country = 6
service = "tg"

def clicker(number): # кликер для получения sms
    number_write = pyautogui.locateCenterOnScreen('gfx/number_write.png')
    pyautogui.moveTo(number_write)
    pyautogui.click()

    pyautogui.keyDown('backspace')
    time.sleep(3)
    pyautogui.keyUp('backspace')

    pyautogui.write(str(number))
    pyautogui.press('enter')
    time.sleep(3)
    try:
        if pyautogui.locateCenterOnScreen('gfx/block_number.png'):
            ok = pyautogui.locateCenterOnScreen('gfx/block_number_ok.png')
            pyautogui.moveTo(ok)
            pyautogui.click()
            out = "block"
            return out
    except:
        pass
    try:
        send_sms = pyautogui.locateCenterOnScreen('gfx/send_sms.png')
    except:
        print("Кнопки send_sms не обнаружено. Выход из скрипта через 2 минуты.")
        time.sleep(timer_clock)
        del_number = sa.setStatus(id=r_id, status=8)
        exit()
    pyautogui.moveTo(send_sms)
    pyautogui.click()
    out = "no_block"
    return out

def get_number(): # получение номера
    get_numbers = sa.getNumbersStatus(country=6)
    while True:
        try:
            number = sa.getNumber(service=service, country=country, verification="false")
            break
        except KeyError as e:
            if str(e) == "'There are no free numbers for receiving SMS from the current service'":
                print("В данный момент нет доступных номеров для указанного сервиса. Повторный запрос через 10 секунд...")
                time.sleep(10)
            else:
                print("Произошла ошибка:", str(e))
    try:
        out_number = number['phone'] # полученный номер
        out_id = number['activation_id'] # полученный ID
        print("Number", out_number)
        print("ID", out_id)
        return out_number, out_id
    except KeyError:
        print(number['message'])

while True:
    r_number, r_id = get_number()
    click = clicker(r_number)
    if click == "block":
        print("Номер заблокирован, обновляем через 2 минуты.")
        time.sleep(timer_clock)
        while True:
            try:
                del_number = sa.setStatus(id=r_id, status=8)
                break
            except:
                print(del_number['message'])
                pass
    if click == "no_block":
        break

start_time = time.time()

while True:
    if time.time() - start_time > timer_clock:
        print("Прошло 2 минуты... СМС не было получено. Повторный запрос.")
        back = pyautogui.locateCenterOnScreen('gfx/back.png')
        pyautogui.moveTo(back)
        pyautogui.click()
        time.sleep(1)
        while True:
            try:
                del_number = sa.setStatus(id=r_id, status=8)
                break
            except:
                print(del_number['message'])
                pass
        while True:
            r_number, r_id = get_number()
            click = clicker(r_number)
            if click == "block":
                print("Номер заблокирован, обновляем через 2 минуты.")
                time.sleep(timer_clock)
                while True:
                    try:
                        del_number = sa.setStatus(id=r_id, status=8)
                        break
                    except:
                        print(del_number['message'])
                        pass
            if click == "no_block":
                break
        start_time = time.time()
    status = sa.getStatus(id=r_id)
    if status == "STATUS_WAIT_CODE":
        remaining_time = int(timer_clock - (time.time() - start_time))
        print("Ожидание СМС... Осталось", remaining_time, "секунд")
        time.sleep(10)
    if status == "STATUS_OK":
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga")
        print("СМС получено. Попытка вывести смс на экран...")
        try:
            get_sms = sa.getRentStatus(r_id)
            print("SMS", status['values']['0']['text'])
            break
        except:
            print(status['message'])
            print("СМС не удалось вывести...")
            break
