import asyncio
import discord
import config

class Timer():
    def __init__(self):
        self.study_time = -1
        self.rest_time = -1
        self.task = None
    
    def running(self):
        return not (self.task is None or self.task.done())
    
    def start(self, ctx, voice_channel, st, rt):
        self.ctx = ctx
        self.study_time = st * 60
        self.rest_time = rt * 60
        self.voice_channel = voice_channel
        self.task = asyncio.create_task(self.run_timer())
        
        print("타이머 시작")
    
    def stop(self):
        self.task.cancel()
        
        print("타이머 중단")
        
    def restart(self, voice_channel):
        self.task = asyncio.create_task(self.run_timer())
        self.voice_channel = voice_channel
        
        print("타이머 재시작")        
            
    async def run_timer(self):
        await self.ctx.send("수업시간 : {} 분 / 쉬는 시간 : {} 분".format(self.study_time // 60, self.rest_time // 60))
        
        while True:
            await self.ctx.send("공부 시간이야!")
            print("공부 시간")
            # executable에 ffmpeg.exe의 경로를 넣어 사용
            self.voice_channel.play(discord.FFmpegPCMAudio(executable=config.CONFIG["FFMPEG_PATH"], source="sounds/start.mp3"))
            await asyncio.sleep(self.study_time)
            await self.ctx.send("쉬는 시간이야!")
            print("쉬는 시간")
            # executable에 ffmpeg.exe의 경로를 넣어 사용
            self.voice_channel.play(discord.FFmpegPCMAudio(executable=config.CONFIG["FFMPEG_PATH"], source="sounds/finish.mp3"))
            await asyncio.sleep(self.rest_time)
