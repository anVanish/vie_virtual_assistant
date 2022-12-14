import os
import urllib.request as urllib2
import json
import ctypes
import win32con
import wikipedia
import requests
import webbrowser
from random import randint
from youtube_search import YoutubeSearch
from datetime import datetime
from gtts import gTTS
import playsound
import time
from package.ear import listen

#get user info
with open('asset/data/user_info.json', encoding='utf-8') as f:
    user = json.load(f)

#get stories
with open('asset/data/stories.txt', 'rt', encoding='utf-8') as f:
    stories = f.read()
stories = stories.split('--')

#set up language
language = "vi"
wikipedia.set_lang('vi') 
#save current wallpaper
ubuf = ctypes.create_unicode_buffer(512)
ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
my_wallpaper = ubuf.value

#store directories that ussually contain win app
current_dir = os.getcwd()
apps_dirs = ["C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"]
path = os.path.join('C:\\Users\\', os.getlogin(),'Desktop\\')
apps_dirs.append(path)

#boolean
IS_SILENT = True
NOT_SILENT = False

class Action:
    def act(self, ans, tag):
        status = NOT_SILENT
        if tag == "hello":
            status = self.__hello(ans, tag)
        elif tag == "time" or tag == "date":
            status =  self.__get_time(ans, tag)
        elif tag == "weather":
            status =  self.__current_weather(ans, tag)
        elif tag == "wiki":
            status =  self.__tell_me_about(ans, tag)
        elif tag == "playsong":
            status =  self.__play_song(ans, tag)
        elif tag == "open website":
            status =  self.__open_website(ans, tag)
        elif tag == "search google":
            status =  self.__open_google_and_search(ans, tag)
        elif tag == "open app":
            status =  self.__open_application(ans, tag)
        elif tag == "wallpaper":
            status =  self.__change_wallpaper(ans, tag)
        elif tag == 'me':
            status = self.__me(ans, tag)
        elif tag == 'story':
            status = self.__story(ans, tag)
        elif tag == 'sad':
            status = self.__sad(ans, tag)
        else:
            status =  self.__speak(ans, tag)

        return status

    def speak(self, ans):
        self.__speak(ans)

    def __hello(self, ans, tag):
        hour = datetime.now().hour
        if 4 <= hour <= 10:
            ans = 'Ch??o bu???i s??ng, ng??y m???i vui v??? nha'
        elif 15 < hour <= 18:
            ans = 'Candy xin ch??o, bu???i chi???u vui v???'
        elif 19 < hour <= 22:
            ans = 'Xin ch??o bu???i t???i'
        elif 22 < hour <= 24 or 0 <= hour <= 3:
            ans = 'Candy ch??o b???n, khuya r???i kh??ng n??n th???c khuya b???n nha'
        if user['name'] != '':
            name = user['name']
            ans = f'Ch??o {name} nha, th???t vui khi g???p l???i b???n'
        self.__speak(ans, tag)
        return NOT_SILENT

    def __speak(self, ans, tag='', language='vi'):
        if ans == "":
            return NOT_SILENT
        tts = gTTS(text=ans, lang=language, slow=False)
        filedir = "asset/audio/sound.mp3"
        tts.save(filedir)
        print("Candy: " + ans)
        playsound.playsound(filedir)
        os.remove(filedir)

        return NOT_SILENT

    def __check_acception(self, you):
        accepts = ['okay', 'oke', 'ok??', 'c??', 'ok', '???????c']
        for accept in accepts:
            if accept in you:
                return True
        return False
    def __story(self, ans, tag):
        count = 0
        while True:
            count += 1
            index = randint(0, len(stories) - 1)
            self.__speak(stories[index])
            time.sleep(1)
            if count == 3:
                self.__speak('Candy k??? chuy???n c?? l??m b???n vui kh??ng')
                you = listen()
                if self.__check_acception(you):
                    self.__speak('Candy r???t vui khi l??m b???n vui')
                else:
                    self.__speak('Candy bu???n v?? kh??ng l??m b???n vui ???????c')
                    return NOT_SILENT
            self.__speak('B???n c?? mu???n nghe ti???p kh??ng?')
            you = listen()
            if not self.__check_acception(you):
                self.__speak('Okay n??')
                break
        return NOT_SILENT

    def __sad(self, ans, tag):
        you = ''
        rand = randint(0, 2)
        if rand != 2:
            ans += " Candy ???? h???c h???i ???????c m???t v??i c??ch ????? v?????t qua n???i bu???n, h??y ????? Candy gi??p b???n."
        if rand == 0:
            self.__speak(ans + ' B???n c?? mu???n nghe v??i b???n nh???c kh??ng?')
            you = listen()
        elif rand == 1:
            self.__speak(ans + ' B???n c?? mu???n nghe v??i m???u truy???n vui kh??ng?')
            you = listen()
        else:
            self.__speak('B???n h??y lu??n l???c quan l??n nh??, Candy lu??n ??? b??n b???n')
        
        if self.__check_acception(you):
            if rand == 0:
                return self.__play_song('Ca kh??c nh???c bu???n t??m tr???ng', tag)
            elif rand == 1:
                return self.__story(you, tag)
        elif rand != 2:
            self.__speak('Candy hi???u r???i...')
        return NOT_SILENT         

    def __get_time(self, ans, tag):
        now = datetime.now()
        if tag == 'time':
            self.__speak('B??y gi??? l?? %d gi??? %d ph??t' % (now.hour, now.minute))
        elif tag == 'date':
            self.__speak("H??m nay l?? ng??y %d th??ng %d n??m %d" % (now.day, now.month, now.year))

        return NOT_SILENT

    def __open_website(self, ans, tag):
        #ans: website address, eg: google.com
        if ans == '':
            self.__speak('B???n mu???n m??? website n??o?')
            ans = listen()
        if ans == '':
            return IS_SILENT

        url = 'https://www.' + ans
        self.__speak(f"??ang m??? {ans}.")
        webbrowser.open(url)

        return IS_SILENT

    def __open_google_and_search(self, ans, tag):
        #ans: noun, keyword, eg: egg, how to play...
        if ans == '':
            self.__speak('B???n mu???n t??m ki???m g???')
            ans = listen()
        if ans == '':
            return IS_SILENT
        self.__speak(f"??ang t??m ki???m {ans}")
        webbrowser.open("https://www.google.com/search?q=" + ans)

        return IS_SILENT

    def __tell_me_about(self, ans, tag):
        #ans: topic you want assistant to tell you
        try:
            if ans == '':
                self.__speak("B???n mu???n nghe v??? g???")
                you = listen()
            contents = wikipedia.summary(you).split('\n')
            count = 0
            self.__speak("Theo wikipedia, ")
            while count < len(contents):
                self.__speak(contents[count])
                if count + 1 < len(contents):
                    self.__speak("B???n mu???n nghe th??m kh??ng?")
                    you = listen()
                    if 'c??' in you:
                        count += 1
                    else:
                        break
                else:
                    break
            self.__speak('Candy c???m ??n b???n ???? l???ng nghe!')
        except Exception as e:
            self.__speak("Candy kh??ng ?????nh ngh??a ???????c thu???t ng??? c???a b???n. Xin m???i b???n n??i l???i.")
        return NOT_SILENT

    def __play_song(self, ans, tag):
        #ans: name of song
        if ans == '':
            self.__speak('M???i b???n ch???n t??n b??i h??t')
            ans = listen()
        if ans == '':
            return IS_SILENT
        self.__speak('H??y ch??? Candy trong gi??y l??t')
        while True:
            result = YoutubeSearch(ans, max_results=10).to_dict()
            if result:
                break
        url = 'https://www.youtube.com' + result[0]['url_suffix']
        self.__speak("Candy ???? m??? b??i h??t. Ch??c b???n nghe nh???c vui v???")
        webbrowser.open(url)

        return IS_SILENT
    
    def __find_app_dir(self, string, directory):
        if string == "":
            return string
        is_finded = False

        #get list of applications in directory
        app_dir = directory
        os.chdir(directory)
        app_list = os.listdir()

        #find app match with string
        for app in app_list:
            if is_finded:
                break
            if '.' in app:
                if string.lower() in app.lower() and '.lnk' in app:
                    app_dir += app
                    is_finded = True
            else:
                temp_dir = app_dir + app + '\\'
                os.chdir(temp_dir)
                temp_list = os.listdir()

                for temp in temp_list:
                    if '.lnk' in temp and string.lower() in temp.lower():
                        temp_dir += temp
                        app_dir = temp_dir
                        is_finded = True
                        break

        #if can't find it
        if is_finded == False:
            app_dir = ''

        os.chdir(current_dir)
        return app_dir
    def __open_application(self, ans, tag):
        #ans: name of your application
        if ans == "":
            self.__speak("B???n mu???n m??? ???ng d???ng n??o?")
            ans = listen()
            ans = ans.lower()
        if ans == '':
            return IS_SILENT

        for app_dir in apps_dirs:
            app_dir = self.__find_app_dir(ans, app_dir)
            if app_dir:
                break
        #app_dir is the directory of your application

        if app_dir:
            self.__speak('Candy ??ang m??? ' + ans.title() + ". Ch??? Candy trong gi??y l??t nha")
            os.startfile(app_dir)
        else:
            self.__speak('Candy kh??ng th??? t??m th???y ???ng d???ng c???a b???n')
            return NOT_SILENT
        
        return IS_SILENT

    def __change_wallpaper(self, ans, tag):
        api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key
        self.__speak('Okay lu??n, ch??? Candy x??u nha')
        while True:
            f = urllib2.urlopen(url)
            json_string = f.read()
            f.close()
            parsed_json = json.loads(json_string)
            photo = parsed_json['urls']['full']
            img_dir = os.path.dirname(__file__) + "\\..\\asset\\img\\a.png"
            urllib2.urlretrieve(photo, img_dir)
            image = os.path.join(img_dir)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
            self.__speak('H??nh n???n m??y t??nh v???a ???????c thay ?????i')
            self.__speak('B???n c?? mu???n ?????i ti???p h??nh n???n kh??c kh??ng')
            # you = input('you: ')
            you = listen()
            if "c??" in you:
                pass
            elif "c??" in you or 'c???a t??i' in you or '?????i l???i' in you:
                image = os.path.join(my_wallpaper)
                ctypes.windll.user32.SystemParametersInfoW(20,0,my_wallpaper,3)
                self.__speak('H??nh n???n m??y t??nh ???? ???????c ????a v??? nh?? c??')
                break
            else:
                self.__speak("???? r??")
                break
        return NOT_SILENT

    def __current_weather(self, ans, tag):
        #ans: your city
        if ans == '':
            self.__speak("B???n mu???n xem th???i ti???t ??? ????u?")
            # city = input("you: ")
            ans = listen()
        if not ans:
            return IS_SILENT
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key = "fe8d8c65cf345889139d8e545f57819a"
        call_url = ow_url + "appid=" + api_key + "&q=" + ans + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            weather_description = wthr[0]["description"]
            now = datetime.now()
            content = f"""
            {ans.title()} h??m nay l?? ng??y {now.day} th??ng {now.month} n??m {now.year}
            M???t tr???i m???c v??o {sunrise.hour} gi??? {sunrise.minute} ph??t
            M???t tr???i l???n v??o {sunset.hour} gi??? {sunset.minute} ph??t
            Nhi???t ????? trung b??nh l?? {current_temperature} ????? C
            ??p su???t kh??ng kh?? l?? {current_pressure} Hectopascal
            ????? ???m l?? {current_humidity}%
            Tr???i h??m nay quang m??y. D??? b??o m??a r???i r??c ??? m???t s??? n??i."""
            self.__speak(content)
            time.sleep(2)
        else:
            self.__speak("Kh??ng t??m th???y ?????a ch??? b???n y??u c???u")

        return NOT_SILENT

    def __me(self, ans, tag):
        name = user['name']
        if name == '':
            self.__speak("Candy ch??a bi???t t??n b???n, b???n cho t??i bi???t ???????c ch????")
            name = listen()
            self.__speak("T??n b???n l?? " + name + ". B???n c?? mu???n t??i g???i b???n l?? " + name + " kh??ng?")
            you = listen()
            if 'c??' in you or 'okay' in you or '???????c' in you:
                user['name'] = name
                self.__speak('Candy s??? nh??? t??n ' + name)
                with open('asset/data/user_info.json', 'w', encoding='utf-8') as f:
                    json.dump(user, f)
            else:
                self.__speak('V???y th??i')
        else:
            self.__speak('Candy v???n nh??? t??n b???n l?? ' + name)

                
