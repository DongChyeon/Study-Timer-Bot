import discord
import asyncio
import config

from timer import Timer
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
timer = Timer()

@bot.event
async def on_ready():
    print('공부 타이머 봇 실행 중 : ', bot.user.id)

@bot.command(name="도움말")
async def help(ctx):
    embed = discord.Embed(title="도움말", description="봇이 실행할 수 있는 명령어 목록들이야\n타이머는 무조건 하나만 설정 가능해!")
    embed.add_field(name="!시작 공부시간(분) 쉬는시간(분)", value="현재 시간으로부터 공부시간과 쉬는시간을 설정해서 그때마다 알람을 울려줘요", inline=False)
    embed.add_field(name="!재시작", value="취소한 타이머를 재시작해줘요", inline=False)
    embed.add_field(name="!취소", value="현재 설정되어 있는 타이머를 제거해줘요", inline=False)
    embed.set_footer(text="당신은 지체할 수 있지만 시간은 지체하지 않는다.  -벤자민 프랭클린-")
    await ctx.send(embed=embed)

@bot.command("시작")
async def start(ctx, study_time: int, rest_time: int):
    global timer

    if timer.running():
        await ctx.send("타이머가 이미 작동하고 있습니다. !취소 를 입력하고 다시 실행해주세요.")
        return
    
    voice_channel = ctx.author.voice.channel if ctx.author.voice is not None else None
    
    if voice_channel is None:
        await ctx.send("사용자가 음성 채널에 들어가 있어야 사용이 가능합니다. 음성 채널에 먼저 들어가주세요.")
        return
    
    # 봇을 음성 채널에 연결
    voice_channel = await voice_channel.connect()
    
    await ctx.send("타이머를 시작할게요.")
    timer.start(ctx, voice_channel, study_time, rest_time)
    
@bot.command("재시작")
async def restart(ctx):
    global timer

    if timer.running():
        await ctx.send("타이머가 이미 작동하고 있습니다. !취소 를 입력하고 다시 실행해주세요.")
        return

    voice_channel = ctx.author.voice.channel if ctx.author.voice is not None else None
    
    if voice_channel is None:
        await ctx.send("사용자가 음성 채널에 들어가 있어야 사용이 가능합니다. 음성 채널에 먼저 들어가주세요.")
        return

    # 봇을 음성 채널에 연결
    voice_channel = await voice_channel.connect()
    
    await ctx.send("타이머를 재시작할게요.")
    timer.restart(voice_channel)
    
@bot.command("취소")
async def cancel(ctx):
    global timer
    
    if not timer.running():
        await ctx.send("설정되어 있는 타이머가 없습니다.")
        return

    if not bot.voice_clients:
        await ctx.send("봇이 해당 음성 채널에 이미 없습니다.")
        return
    await bot.voice_clients[0].disconnect()
    
    timer.stop()
    await ctx.send("타이머를 취소할게요.")

# 봇의 토큰 값을 넣어 사용    
bot.run(config.CONFIG["TOKEN"])
