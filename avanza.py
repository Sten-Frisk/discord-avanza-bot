import json
import requests
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def aktie(ctx, *, stock: str):
    try:
        find_stock = json.loads(requests.get("https://www.avanza.se/ab/component/orderbook_search/?query=" + stock).text)
        id = find_stock[0]["id"]
    except IndexError:
        await ctx.send("Hittade inget!")
        return

    data = json.loads(requests.get("https://www.avanza.se/_mobile/market/orderbooklist/" + id).text)

    stock_name = data[0]["name"]
    last_price = data[0]["lastPrice"]
    currency = data[0]["currency"]
    price_three_months_ago = data[0]["priceThreeMonthsAgo"]
    
    try:
        highest_price = data[0]["highestPrice"]
    except:
        highest_price = "N/A"
        
    try:
        lowest_price = data[0]["lowestPrice"]
    except:
        lowest_price = "N/A"

    change_in_number = data[0]["change"]
    change_in_percent = data[0]["changePercent"]

    change_in_months = round((float(last_price) - float(price_three_months_ago))/float(price_three_months_ago)*100,1)

    total_volume_traded = data[0]["totalVolumeTraded"]

    await ctx.send(f'{stock_name} | {last_price} {currency} | Idag: {change_in_percent} ({change_in_number} {currency}) | 3 mån: {change_in_months} ({price_three_months_ago} {currency}) | Volla: {lowest_price} - {highest_price} {currency} | Volym: {total_volume_traded}')

bot.run('YOUR_TOKEN_HERE')
