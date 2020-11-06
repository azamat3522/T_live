import csv
import time
# from bs4 import BeautifulSoup
import openpyxl
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import csv



with open('fb_profile.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(["Ссылка", "Имя", "кол-во постов", "дата последнего поста", "фото профиля", "размер фото",
                     "Работа", "ВУЗ", "Школа", "Адрес", "Контакты", "Сайты и соцсети", "Осн инфо", "Дата рождения",
                     "Язык", "Статус", "Семья", "О пользователе", "Произношение имени", "Другие имена", "Цитаты", "Кол-во фоток", "кол-во нравится", "Отметки нравится", "Кол-во друзей", "Друзья"])

profile_info = []


def parse_info(xpath):
    infos = []
    objects = driver.find_elements_by_xpath(xpath)
    for object in objects:
        print(object.text)
        infos.append(object.text)
    profile_info.append(infos)


def scroll_to_down(divs, time_plus):
    time_wait = 2
    retry = 0
    while True:
        p_height = driver.execute_script("return document.body.scrollHeight;")
        print(p_height)
        driver.execute_script(f"window.scrollTo(0, (document.body.scrollHeight)/2);")
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(time_wait)
        new_p_height = driver.execute_script("return document.body.scrollHeight;")
        print(new_p_height)
        print(p_height == new_p_height)
        objects = driver.find_elements_by_xpath(divs)
        print(len(objects))
        if len(objects) > 500:
            time_wait = 5 + time_plus
        elif len(objects) > 1000:
            time_wait = 7 + time_plus
        elif len(objects) > 1500:
            time_wait = 10 +time_plus
        if p_height == new_p_height:
            if retry < 3:
                retry += 1
                print('retryyyyyyy')
                pass
            else:
                print('end')
                break
        else:
            retry = 0
    profile_info.append(len(objects))



option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--headless")
option.add_argument("--window-size=1325x744")
option.add_argument("--remote-debugging-port=9222")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(chrome_options=option)
# driver.maximize_window(driver.window_handles)
# driver.window_handles
print('Захожу на фб')
driver.get("https://www.facebook.com")
driver.implicitly_wait(10)
# time.sleep(2)

print('Жму на закрытие окоша модалки')
# WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-cookiebanner="accept_button"]'))).click()
#
# driver.implicitly_wait(10)
# time.sleep(2)

print("Логинюсь")
driver.find_element_by_name('email').send_keys('akyl.aydarbekov@gmail.com')
driver.find_element_by_name('pass').send_keys('sprite05')
print("Отправляю форму")
driver.find_element_by_css_selector('button[type="submit"]').click()

driver.implicitly_wait(10)
time.sleep(2)
print("Захожу на профиль")
profile_link = "https://www.facebook.com/profile.php?id=100008299473734"
profile_info.append(profile_link)
driver.get(profile_link)
# https://www.facebook.com/profile.php?id=100003996247530
driver.implicitly_wait(10)
time.sleep(7)



# id_prof = profile_link.split('id=')
# print(id_prof[1])

name_h1 = driver.find_element_by_tag_name('h1')
print(name_h1.text)
profile_info.append(name_h1.text)


# парсинг постов
print("Парсю посты")
post_divs = "//div[@class='rq0escxv l9j0dhe7 du4w35lb d2edcug0 hpfvmrgz gile2uim buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5']/div"
scroll_to_down(post_divs, 2)

last_post = driver.find_element_by_xpath("//div[@class='rq0escxv l9j0dhe7 du4w35lb d2edcug0 hpfvmrgz gile2uim buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5']/div[last()]")
time_post = last_post.find_element_by_css_selector('a[class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"]')

hover = ActionChains(driver).move_to_element(time_post)
hover.perform()
time.sleep(1)
try:
    time_full = driver.find_element_by_css_selector('span[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 tia6h79c fe6kdd0r mau55g9w c8b282yb iv3no6db e9vueds3 j5wam9gi knj5qynh oo9gr5id hzawbc8m"]')
except:
    try:
        time_icon = last_post.find_element_by_css_selector('span[class="tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41"]')
        prelast_post = driver.find_element_by_xpath("//div[@class='rq0escxv l9j0dhe7 du4w35lb d2edcug0 hpfvmrgz gile2uim buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5']/div[last()-1]")
        time_post = prelast_post.find_element_by_css_selector(
        'a[class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"]')
        hover = ActionChains(driver).move_to_element(time_post)
        hover.perform()
        time.sleep(1)
        time_full = driver.find_element_by_css_selector(
            'span[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 tia6h79c fe6kdd0r mau55g9w c8b282yb iv3no6db e9vueds3 j5wam9gi knj5qynh oo9gr5id hzawbc8m"]')
    except:
        print('some error')
    # hover = ActionChains(driver).move_to_element(time_icon)
    # hover.perform()
    # time.sleep(1)
    # time_full = driver.find_element_by_css_selector('span[class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 tia6h79c fe6kdd0r mau55g9w c8b282yb iv3no6db e9vueds3 j5wam9gi knj5qynh oo9gr5id hzawbc8m"]')

print(time_full.text)
profile_info.append(time_full.text)
# time.sleep(2)

# Парсинг фото профиля

profile_photo = driver.find_element_by_css_selector('a[class="oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l oo9gr5id"]')
profile_photo_full =  profile_photo.get_attribute('href')
driver.get(profile_photo_full)
driver.implicitly_wait(10)
time.sleep(1)
img = driver.find_element_by_css_selector('img[class="gitj76qy r9f5tntg d2edcug0"]')
width = driver.execute_script("return document.getElementsByClassName('gitj76qy r9f5tntg d2edcug0')[0].naturalWidth")
height = driver.execute_script("return document.getElementsByClassName('gitj76qy r9f5tntg d2edcug0')[0].naturalHeight")
print(img.get_attribute('src'))
profile_info.append(img.get_attribute('src'))
print(width)
print(height)
profile_info.append(str(width) + ' x ' + str(height))
driver.back()
time.sleep(2)


# Парсинг инфо

infoblock = driver.find_element_by_xpath("//div[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr']/div[@class='tojvnm2t a6sixzi8 k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y l9j0dhe7 iyyx5f41 a8s20v7p']/div[@class='cb02d2ww ni8dbmo4 stjgntxs l9j0dhe7 k4urcfbm du4w35lb lzcic4wl']/div[@class='soycq5t1 l9j0dhe7']/div[@class='i09qtzwb rq0escxv n7fi1qx3 pmk7jnqg j9ispegn kr520xx4']/a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 pq6dq46d p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l dwo3fsh8 ow4ym5g4 auili1gw mf7ej076 gmql0nx0 tkr6xdv7 bzsjyuwj cb02d2ww j1lvzwm4'][2]/div[@class='bp9cbjyn rq0escxv j83agx80 pfnyh3mw frgo5egb l9j0dhe7 cb02d2ww hv4rvrfc dati1w0a']")
infoblock.click()

informations = driver.find_element_by_css_selector("div[class='ls2amcm3 pcp91wgn ihqw7lf3 p8fzw8mz discj3wi pfnyh3mw rq0escxv maa8sdkg'")
infos = informations.find_elements_by_css_selector('div[class="bi6gxh9e"]')
infos[1].click()
time.sleep(1)

# jobs
parse_info("//div[@class='tu1s4ah4'][1]/div[position()>1]")
# ihes
parse_info("//div[@class='tu1s4ah4'][2]/div[position()>1]")
# schools
parse_info("//div[@class='dati1w0a tu1s4ah4 f7vcsfb0 discj3wi']/div[3]/div[position()>1]")

infos[2].click()
time.sleep(1)

# addresses
parse_info("//div[@class='dati1w0a tu1s4ah4 f7vcsfb0 discj3wi']/div/div[position()>1]")

infos[3].click()
time.sleep(1)

# contacts
parse_info("//div[@class='tu1s4ah4'][1]/div[@class='oygrvhab']")
# websites
parse_info("//div[@class='tu1s4ah4'][2]/div[@class='oygrvhab']")
# main_info
parse_info("//div[@class='c9zspvje'][1]")
# birthday_dates
parse_info("//div[@class='c9zspvje'][2]")
# languages
parse_info("//div[3]/div[@class='oygrvhab']")

infos[4].click()
time.sleep(1)

# statuses
parse_info("//div[1]/div[@class='oygrvhab']")
# families
parse_info("//div[2]/div[@class='oygrvhab']")

infos[5].click()
time.sleep(1)

# about_list
parse_info("//div[1]/div[@class='oygrvhab']")
# names
parse_info("//div[2]/div[@class='oygrvhab']")
# other_names
parse_info("//div[3]/div[@class='oygrvhab']")
# quotes
parse_info("//div[4]/div[@class='oygrvhab']")



# time.sleep(1)

# Парсинг кол-во фото
try:
    print('Ищу Фото')
    fotoblock = driver.find_element_by_xpath("//div[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr']/div[@class='tojvnm2t a6sixzi8 k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y l9j0dhe7 iyyx5f41 a8s20v7p']/div[@class='cb02d2ww ni8dbmo4 stjgntxs l9j0dhe7 k4urcfbm du4w35lb lzcic4wl']/div[@class='soycq5t1 l9j0dhe7']/div[@class='i09qtzwb rq0escxv n7fi1qx3 pmk7jnqg j9ispegn kr520xx4']/a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 pq6dq46d p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l dwo3fsh8 ow4ym5g4 auili1gw mf7ej076 gmql0nx0 tkr6xdv7 bzsjyuwj cb02d2ww j1lvzwm4'][4]/div[@class='bp9cbjyn rq0escxv j83agx80 pfnyh3mw frgo5egb l9j0dhe7 cb02d2ww hv4rvrfc dati1w0a']")
    fotoblock.click()
except:
    print('Не нашел, Ищу в Ещё')
    driver.find_element_by_xpath(".//*[contains(text(), 'Ещё')]").click()
    time.sleep(1)
    fotoblock2 = driver.find_element_by_xpath("//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 oi9244e8 oygrvhab h676nmdw pybr56ya dflh9lhu f10w8fjw scb9dxdr i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l bp9cbjyn dwo3fsh8 btwxx1t3 pfnyh3mw du4w35lb'][1]")
    print('Нашел. Жму')
    fotoblock2.click()

time.sleep(1)
print('Ищу Альбомы')
alboms = driver.find_element_by_xpath("//div[@class='rq0escxv l9j0dhe7 du4w35lb gderk4og hpfvmrgz dxtxif39 buofh1pr g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5']/div[1]//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 pq6dq46d p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l dwo3fsh8 ow4ym5g4 auili1gw mf7ej076 gmql0nx0 tkr6xdv7 bzsjyuwj cb02d2ww j1lvzwm4'][last()]")
alboms.click()
time.sleep(1)
counts = driver.find_elements_by_xpath("//div[@class='rq0escxv rj1gh0hx buofh1pr ni8dbmo4 stjgntxs l9j0dhe7']/div[@class='l9j0dhe7']//div[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t buofh1pr tgvbjcpo sv5sfqaa obtkqiv7']//div[@class='qzhwtbm6 knvmm38d'][2]")
a = 0
for count in counts:
    ads = (count.text).split(' ')
    a += int(ads[0])
    print(ads[0])
print('Нашел кол-во фото')

print(a)
profile_info.append(a)
# time.sleep(2)


# отметки нравится
#//*[contains(text(), 'Альбомы')]
driver.find_element_by_xpath(".//*[contains(text(), 'Ещё')]").click()
time.sleep(2)
driver.find_element_by_xpath(".//*[contains(text(), 'Отметки \"Нравится\"')]").click()
time.sleep(1)
likes = "//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 a8c37x1j p7hjln8o kvgmc6g5 cxmmr5t8 sjgh65i0 hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8']"
scroll_to_down(likes, 0)
likes_sel = driver.find_elements_by_xpath(likes)
likes_list = []
for like in likes_sel:
    print(like.get_attribute('href'))
    like_name = like.find_element_by_xpath(".//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i jq4qci2q a3bd9o3v lrazzd5p oo9gr5id hzawbc8m']")
    print(like_name.text)
    likes_list.append(like_name.text + "----" + like.get_attribute('href'))
profile_info.append(likes_list)

# Парсинг друзей
# time.sleep(3)
profiles_friends = []
print('Ищу кнопку друзей')
friends_btn = driver.find_element_by_xpath("//div[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t g5gj957u d2edcug0 hpfvmrgz rj1gh0hx buofh1pr']/div[@class='tojvnm2t a6sixzi8 k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y l9j0dhe7 iyyx5f41 a8s20v7p']/div[@class='cb02d2ww ni8dbmo4 stjgntxs l9j0dhe7 k4urcfbm du4w35lb lzcic4wl']/div[@class='soycq5t1 l9j0dhe7']/div[@class='i09qtzwb rq0escxv n7fi1qx3 pmk7jnqg j9ispegn kr520xx4']/a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 pq6dq46d p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l dwo3fsh8 ow4ym5g4 auili1gw mf7ej076 gmql0nx0 tkr6xdv7 bzsjyuwj cb02d2ww j1lvzwm4'][3]")
print('Нашел кликаю друзей')
time.sleep(1)
friends_btn.click()

try:
    driver.find_element_by_xpath(".//*[contains(text(), 'Все друзья')]")
    friends = "//div[@class='sjgh65i0'][1]/div/div/div/div[@class='j83agx80 btwxx1t3 lhclo0ds i1fnvgqd']/div[@class='bp9cbjyn ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi n1f8r23x rq0escxv j83agx80 bi6gxh9e discj3wi hv4rvrfc ihqw7lf3 dati1w0a gfomwglr']/div[@class='buofh1pr hv4rvrfc']/div[1]/a"
    scroll_to_down(friends, 0)
    friends = driver.find_elements_by_xpath("//div[@class='sjgh65i0'][1]/div/div/div/div[@class='j83agx80 btwxx1t3 lhclo0ds i1fnvgqd']/div[@class='bp9cbjyn ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi n1f8r23x rq0escxv j83agx80 bi6gxh9e discj3wi hv4rvrfc ihqw7lf3 dati1w0a gfomwglr']/div[@class='buofh1pr hv4rvrfc']/div[1]/a")
    for friend in friends:
        print(friend.get_attribute('href'))
        print(friend.text)
        profiles_friends.append(friend.text + "-----" + friend.get_attribute('href'))
except:
    print('скрытый профиль походу')

profile_info.append(profiles_friends)
print(profile_info)

with open('fb_profile.csv', 'a+', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(profile_info)
