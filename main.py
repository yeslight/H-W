# -*- coding: utf-8 -*-
# https://github.com/mybdye 🌟

import base64
import os
import ssl
import time
import urllib
import requests
import subprocess
import undetected_chromedriver as uc

from helium import *
from selenium.webdriver.common.by import By

# 关闭证书验证
ssl._create_default_https_context = ssl._create_unverified_context

try:
    URL_BASE = os.environ['URL_BASE']
except:
    # 本地调试用， please type here the website address without any 'https://' or '/'
    URL_BASE = ''

try:
    USER_ID = os.environ['USER_ID']
except:
    # 本地调试用
    USER_ID = ''

try:
    PASS_WD = os.environ['PASS_WD']
except:
    # 本地调试用
    PASS_WD = ''

try:
    BARK_KEY = os.environ['BARK_KEY']
except:
    # 本地调试用
    BARK_KEY = ''

try:
    TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
except:
    # 本地调试用
    TG_BOT_TOKEN = ''

try:
    TG_USER_ID = os.environ['TG_USER_ID']
except:
    # 本地调试用
    TG_USER_ID = ''


def urlDecode(s):
    return str(base64.b64decode(s + '=' * (4 - len(s) % 4))).split('\'')[1]

def mp3ToWave():
    print('- Func mp3 to wave...')
    subprocess.call(['ffmpeg', '-i', os.getcwd() + audioFile, os.getcwd() + waveFile, '-loglevel', 'quiet', '-y'])
    print('- Func mp3 to wave done!')


def speechToText():
    mp3ToWave()
    response = ''
    i = 0
    while ' -' not in response:
        print('- Func SpeechToText')
        driver.tab_new(urlSpeech)
        delay(2)
        driver.switch_to.window(driver.window_handles[1])
        print('- Switched to window SpeechToText')
        wait_until(Text('Speech to text').exists)
        scroll_down(num_pixels=1200)
        i = i + 1
        if i > 3:
            print('*** speechToText issue! ***')
            break
        #attach_file(os.getcwd() + audioFile, to=S('#uploadbtn'))
        driver.find_element(By.ID, 'fileinput').send_keys(os.getcwd() + waveFile)
        print('- waiting for transcribe')
        delay(10)
        try:
            driver.switch_to.alert()
            Alert.accept()
            print('- Alert accept')
        except:
            pass
        textlist = find_all(S('#speechout'))
        response = [key.web_element.text for key in textlist][0]
        print('- response:', response)
        text = response.split('-'*80)[1].split('\n')[1].replace('. ', '.')
        print('- text:', text)
    driver.close()
    return text


def getAudioLink():
    global block, body
    print('- audio file link searching...')
    if Text('Alternatively, download audio as MP3').exists() or Text('或者以 MP3 格式下载音频').exists():
        block = False
        try:
            src = Link('Alternatively, download audio as MP3').href
        except:
            src = Link('或者以 MP3 格式下载音频').href
        print('- get src:', src)
        # 下载音频文件
        try:
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)
        except Exception as e:
            print('*** 💣 getAudioLink function Error: %s \n try again' % e)
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)
        delay(4)
        text = speechToText()
        print('- waiting for switch to first window')
        driver.switch_to.window(driver.window_handles[0])
        # delay(3)
        set_driver(driver)
        wait_until(S('#audio-response').exists)
        print('- fill audio response')
        write(text, into=S('#audio-response'))
        # delay(3)
        wait_until(S('#recaptcha-verify-button').exists)
        print('- click recaptcha-verify-button')
        click(S('#recaptcha-verify-button'))
        delay(3)
        if Text('Multiple correct solutions required - please solve more.').exists() or Text(
                '需要提供多个正确答案 - 请回答更多问题。').exists():
            print('*** Multiple correct solutions required - please solve more. ***')
            print('- click recaptcha-reload-button')
            click(S('#recaptcha-reload-button'))
            getAudioLink()
        delay(1)

    elif Text('Try again later').exists() or Text('稍后重试').exists():
        textblock = S('.rc-doscaptcha-body-text').web_element.text
        #print(textblock)
        body = ' *** 💣 Possibly blocked by google! ***\n' + textblock
        block = True

    elif not CheckBox('I\'m not a robot').is_checked() or CheckBox('我不是机器人').is_checked():
        print('*** checkbox issue ***')
        reCAPTCHA()

    else:
        print('*** audio download element not found, stop running ***')
        # screenshot() # debug


def reCAPTCHA():
    global block
    print('- click checkbox')
    click(S('.recaptcha-checkbox-borderAnimation'))
    # screenshot() # debug
    delay(4)
    if S('#recaptcha-audio-button').exists():
        print('- audio button found')
        click(S('#recaptcha-audio-button'))
        # screenshot() # debug
        delay(4)
        getAudioLink()
        return block


def cloudflareDT():
    try:
        i = 0
        while Text('Checking your browser before accessing').exists():
            i = i + 1
            print('*** cloudflare 5s detection *** ', i)
            time.sleep(1)
        if i > 0:
            print('*** cloudflare 5s detection finish! ***')
    except Exception as e:
        print('*** 💣 CFDT Error:', e)


def login():
    delay(1)
    if Text('Checking').exists():
        print('- Security Checking...')
        delay(10)

    print('- login')
    #cloudflareDT()
    scroll_down(num_pixels=1000)
    print('- fill user id')
    if USER_ID == '':
        print('*** USER_ID is empty ***')
        kill_browser()
    else:
        write(USER_ID, into=S('@username'))
    print('- fill password')
    if PASS_WD == '':
        print('*** PASS_WD is empty ***')
        kill_browser()
    else:
        write(PASS_WD, into=S('@password'))
    delay(5)
    if Text('reCAPTCHA').exists() or Text('Recaptcha').exists():
    # if Text('I\'m not a robot').exists() or Text('我不是机器人').exists():
        print('- reCAPTCHA found!')
        block = reCAPTCHA()
        if not block:
            submit()

    else:
        print('- reCAPTCHA not found!')
        submit()


def submit():
    global body
    print('- submit')
    try:
        click('Submit')
        print('- submit clicked')
        delay(2)
    except Exception as e:
        print('*** 💣 some error in func submit!, stop running ***\nError:', e)

    #cloudflareDT()
    scroll_down(num_pixels=600)
    try:
        wait_until(Text('Please correct your captcha!.').exists)
        print('*** Network issue maybe, reCAPTCHA load fail! ***')
    except:
        pass
    try:
        wait_until(Text('Invalid').exists)
        print('*** Invalid Username / Password ! ***')
    except:
        pass
    try:
        wait_until(Text('VPS Information').exists)
        print('- VPS Information found!')
        textList = find_all(S('.col-sm-7'))
        status = [key.web_element.text for key in textList][1]
        print('- Status: ', status)
        go_to(urlRenew)
        renewVPS()
    except Exception as e:
        print('*** 💣 submit Error:', e)
        screenshot()  # debug
        body = e

def delay(i):
    time.sleep(i)


def screenshot():  # debug
    driver = get_driver()
    driver.get_screenshot_as_file(os.getcwd() + imgFile)
    print('- screenshot done')
    start_chrome()
    driver = get_driver()
    go_to('http://imgur.com/upload')
    #driver.execute_script('''window.open('http://imgur.com/upload',"_blank")''')
    #switch_to('Imgur')
    time.sleep(5)
    driver.find_element(By.ID, 'file-input').send_keys(os.getcwd() + imgFile)
    time.sleep(5)
    wait_until(Text('POST').exists)
    print('- img uploaded and the 📷 capture src is:', driver.current_url)
    driver.close()


def renewVPS():
    global body
    print('- renew VPS')
    #go_to(urlRenew)
    delay(1)
    cloudflareDT()
    delay(1)
    if S('#web_address').exists():
        print('- fill web address')
        write(URL_BASE, into=S('#web_address'))
        # 过 CAPTCHA
        captcha = funcCAPTCHA()
        print('- fill captcha result')
        write(captcha, into=S('@captcha'))
        print('- check agreement')
        click(S('@agreement'))
        delay(1)
        click('Renew VPS')
        body = extendResult()
        #print('- result:', body)
    else:
        print(' *** 💣 some error in func renew!, stop running ***')
        # screenshot()

def renewCheck():
    global renew, body
    #print('- body now:', body)
    if 'Robot verification failed' in body:
        while renew < 10:
            renew = renew + 1
            print('*** %s %d ***' % (body, renew))
            refresh()
            renewVPS()
            if 'renewed' in body:
                body = '🎉 ' + body
                break
    elif 'renewed' in body:
        body = '🎉 ' + body
        #print(body)

def extendResult():
    global body
    print('- waiting for extend result response')
    delay(15)
    scroll_down(num_pixels=600)
    try:
        textList = find_all(S('#response'))
        body = str([key.web_element.text for key in textList][0])
        #print('extendResult:', result)
        delay(1)
        return body
    except Exception as e:
        print('*** 💣 extendResult Error:', e)
        screenshot()


def push(body):
    print('- body: %s \n- waiting for push result' % body)
    # bark push
    if BARK_KEY == '':
        print('*** No BARK_KEY ***')
    else:
        barkurl = 'https://api.day.app/' + BARK_KEY
        title = URL_BASE
        rq_bark = requests.get(url=f'{barkurl}/{title}/{body}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')
        else:
            print('*** bark push fail! ***', rq_bark.content.decode('utf-8'))
    # tg push
    if TG_BOT_TOKEN == '' or TG_USER_ID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        body = URL_BASE + '\n\n' + body
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + TG_BOT_TOKEN + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': TG_USER_ID, 'text': body}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print('*** tg push fail! ***', rq_tg.content.decode('utf-8'))

    print('- finish!')
    # kill_browser()


def funcCAPTCHA():
    print('- do CAPTCHA')
    divList = find_all(S('.col-sm-3'))
    # 取计算方法
    method = [key.web_element.text for key in divList][0][0]
    # Helium 下没有好的方法拿到两个小图片的 src，切换到 selenium
    # driver = get_driver()
    number1 = int(
        driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][
            0])
    number2 = int(
        driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][
            0])

    if method == '+':
        captcha_result = number1 + number2
    elif method == '-':
        # 应该没有 但还是写了
        captcha_result = number1 - number2
    elif method == 'X':
        captcha_result = number1 * number2
    elif method == '/':
        # 应该没有 但还是写了
        captcha_result = number1 / number2
    print('- captcha result: %d %s %d = %s' % (number1, method, number2, captcha_result))
    return captcha_result

##
audioFile = '/' + URL_BASE + '.mp3'
waveFile = '/' + URL_BASE + '.wav'
imgFile = '/' + URL_BASE + '.png'
##
urlLogin = 'https://' + URL_BASE + '/login'
urlRenew = 'https://' + URL_BASE + '/vps-renew'
##
urlSpeech = urlDecode('aHR0cHM6Ly9henVyZS5taWNyb3NvZnQuY29tL2VuLXVzL3Byb2R1Y3RzL2NvZ25pdGl2ZS1zZXJ2aWNlcy9zcGVlY2gtdG8tdGV4dC8jZmVhdHVyZXM==')
##
block = False
renew = 0
body = ''
##

print('- loading...')
if URL_BASE != '' and '/' not in URL_BASE:
    driver = uc.Chrome(use_subprocess=True)
    driver.set_window_size(785, 627)
    driver.set_page_load_timeout(30)
    set_driver(driver)
    go_to(urlLogin)
    delay(1)
    login()
    renewCheck()
    push(body)
else:
    print('*** [URL_BASE] is missing or wrong! ***')

