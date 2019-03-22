import socket
import os
import time
import sys
import subprocess
import re
obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def grep(x, y):
  try:
    x = x.decode("utf-8")
  except:
    pass
  try:
    y = y.decode("utf-8")
  except:
    pass
  x = x.split("\n")
  for i in x:
    if y in i:
      return i
  return False

def kirim():
  ip = input("IP (Wajib): ")
  port = input("Port (Tidak Wajib): ")
  print("Mengecek Koneksivitas dengan penerima...")
  try:
   obj.connect((ip, port))
   obj.close()
  except:
    print("""Penerima Tidak Dapat Dihubungi
          Pastikan:
           1. Penerima Sudah siap menerima
           2. jika ada permintaan firewall, klik Allow
           3. Jika Pakai Router, pastikan sudah port forward
           4. Jalankan Ulang Program dengan hak akses Administrator

           Maaf """)
    return
  file = []
  filerb = []
  while (True):
    berkas = input("Alamat File (Kalau Sudah Enter Aja): ")
    if (berkas==None):
      break
    if (not os.access(berkas, os.R_OK)):
      print("file %s tidak dapat diakses" %(berkas))
      continue
    file.append(berkas)
  print("Memproses...")
  for i in file:
    with open(i, "rb") as baca:
      filerb.append([os.path.basename(i), baca.read()])
  angka=0
  #memulai
  obj.connect((ip, port))
  obj.send("mulai".encode("utf-8"))
  obj.close()
  for i in filerb:
    obj.connect((ip, port))
    #ke string trus ke bin
    print("Mengirim %s ..." %(os.path.basename(file[angka])))
    a = str(i).encode("utf-8")
    obj.send(a)
    obj.close()
    del a
    a+=1
    print("Selsai\n")
  #tutup
  obj.connect((ip, port))
  obj.send("Selsai".encode("utf-8"))
  obj.close()
  
def terima():
  try:
    def auto():
     print("Mendapatkan IP Address...\n")
     temp = grep(subprocess.check_output("ipconfig"), "IPv4 Address")
     angka = 3
     ipp = temp.split(":")[1]
     print("Ip mu: %s\nsampaikan ini ke pengirim" %(ipp))
     time.sleep(1)
     return [ipp, 21]
    def manual():
      ip = input("IP Address mu: ")
      port = int(input("Port (Tidak Wajib): "))
      return [ip, port]
    mode1 = [auto, manual]
    menu1 = """Untuk Menerima File, anda harus tahu IP Address Komputer mu
               Untuk Mengetahuinya, ada 2 cara
               1. otomatis (80% akurat. kalau gagal, coba pakai manual)
               2. manual"""
    print(menu1)
    ip, port = mode1[int(input("Pilihan Mu: "))-1]()
    print(ip, port)
  except Exception as error:
    print(error)
mode = [ kirim, terima]
menu = """
SHARE THAT V 0.1
KEVIN AGUSTO

1.kirim
2.terima



masukkan nomor yang tersedia

"""
print(menu)
try:
 mode[int(input("Pilihan mu: "))-1]()
except:
  print("Maaf, saya tidak mengerti")
input("\nTekan Enter")
