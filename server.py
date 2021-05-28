# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:36:57 2020

@author: Tarun Arora
"""


import socket
import requests
from nsetools import Nse

def getNSE(stock_code):
    nse = Nse() 

    quote = nse.get_quote(stock_code) 
    string1 = "\n"+ " Company's name:"
    string1 =string1 +  quote['companyName']
    
    string1 = string1 + '\n' + "Last price of the stock : " + str(quote['lastPrice'])
    return string1

def getNews(): 
       
    main_url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=4378fd31bef44b3f8893922e71f69dea"

    open_news_page = requests.get(main_url).json() 
  
    article = open_news_page["articles"] 
   
    results = [] 
      
    for ar in article: 
        results.append(ar["title"]) 

    news_msg = " \n These are the top news headlines: \n"
          
    for i in range(len(results)): 
          
        # printing all trending news 
        news_msg = news_msg + str(i + 1) +"\t" + results[i] + '\n' 
  
    #to read the news out loud for us
    return news_msg
    from win32com.client import Dispatch 
    speak = Dispatch("SAPI.Spvoice") 
    speak.Speak(results)

def getWeather(city_name):
    
    api_key = "481e183128380c2e76c0532d344a199b"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    response = requests.get(complete_url) 
  
    x = response.json() 
  

    if x["cod"] != "404":  
        y = x["main"] 
  
        current_temperature = y["temp"]   
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
        weather_msg = "\n The weather details are as follows: \n"
        weather_msg = (" Temperature (in kelvin unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description)) 
        return weather_msg
    
    else: 
        return ("\n City Not Found \n")

host = 'local host'
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(('', port)) 
s.listen(1)
c, addr = s.accept() 

print("CONNECTION FROM:", str(addr)) 

code, city = [(i) for i in c.recv(2048).decode().split('\n')]

str1 = getNSE(code)

str2 = getWeather(city)

str3 = getNews()

f_msg = str1 + str2 + str3


c.send(f_msg.encode())

from win32com.client import Dispatch 
speak = Dispatch("SAPI.Spvoice") 
speak.Speak(f_msg)

c.close()