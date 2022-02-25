from discord import Webhook, RequestsWebhookAdapter
import discord

def ping_discord(price, image, threshold):
    with open(file=image, mode='rb') as f:
        my_file = discord.File(f)

    webhook = Webhook.from_url("https://discord.com/api/webhooks/946189381482463302/9svEN_y6TeHErHyhh52rOzro-M-cEsRuTT8LovcR8mTdaC1i6tjBBTH-hlyKgAdPlr7Q", adapter=RequestsWebhookAdapter())
    webhook.send(username="SHADY MERCHANT", avatar_url="https://i.imgur.com/a/jIokIO2", file=my_file, content="<@&946199864767836190> LOWEST PRICE FOUND @ {0} | THRESHOLD @ {1}".format(price, threshold))

    print("Message has been sent to discord!")