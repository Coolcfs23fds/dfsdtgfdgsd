import json, os, time, requests, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook, DiscordEmbed

webhookurl = os.getenv('webhook')
ping = os.getenv('webhook_ping')

webhook = DiscordWebhook(url=webhookurl, content=f"<@{ping}>")

def scrape():
  r = requests.get(f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=500&country=all&ssl=all&anonymity=all")
  proxies = []
  for proxy in r.text.split('\n'):
        proxy = proxy.strip()
        if proxy:
            proxies.append(proxy)
  return proxies

while True:
    try:
      proxy = random.choice(scrape())
      print(proxy)
      options = Options()
      options.add_argument("--disable-dev-shm-usage")
      options.add_argument("--no-sandbox")
      driver=webdriver.Chrome(options=options)
      driver.implicitly_wait(10)
      driver.get('https://rest-bf.blox.land/chat/history')
      data = driver.page_source.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', "").replace("</pre></body></html>", "")
      check = json.loads(data)['rain']
      if check['active'] == True:
          grabprize = str(check['prize'])[:-2]
          prize = (format(int(grabprize),","))
          host = check['host']
          getduration = check['duration']
          convert = (getduration/(1000*60))%60
          duration = (int(convert))
          waiting = (convert*60+10)
          sent = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(int(time.time())))
          print(f"Bloxflip Rain!\nRain amount: {prize} R$\nExpiration: {duration} minutes\nHost: {host}\nTimestamp: {sent}\n\n")
          userid = requests.get(f"https://api.roblox.com/users/get-by-username?username={host}").json()['Id']
          thumburl = (f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&height=50&width=50&format=png")
          embed = DiscordEmbed(title=f"{host} is hosting a chat rain!", url="https://bloxflip.com", color=0xFFC800)
          embed.add_embed_field(name="Rain Amount", value=f"{prize} R$")
          embed.add_embed_field(name="Expiration", value=f"{duration} minutes")
          embed.add_embed_field(name="Host", value=f"[{host}](https://www.roblox.com/users/{userid}/profile)")
          embed.set_timestamp()
          embed.set_thumbnail(url=thumburl)
          webhook.add_embed(embed)
          webhook.execute()
          webhook.remove_embed(0)
          time.sleep(waiting)
      elif check['active'] == False:
        time.sleep(30)
    except Exception as e:
      print(e)
      time.sleep(30)
