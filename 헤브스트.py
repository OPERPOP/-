import nextcord
from nextcord.ext import commands

# 봇 토큰을 여기에 입력합니다.
TOKEN = 'MTE0OTM3OTM4ODk5MTg3NzEzMA.G96V6S.SZ3LzviKQ9VhqM7u2mMEfEWGgQjpNCnNj2dfwg'

# 클라이언트 생성
intents = nextcord.Intents.default()  # 기본 인텐트 설정
intents.message_content = True  # 메시지 내용 감지를 활성화합니다.
bot = commands.Bot(command_prefix='/', intents=intents)  # 봇의 접두사를 변경할 수 있습니다.

# 봇이 준비될 때 실행되는 이벤트 핸들러
@bot.event
async def on_ready():
    print(f"{bot.user.name} 준비완료.")
    print(bot.user)
    print(f"오늘도 뜨거운 날이 되겠구만.")
    print("=================================")
    
    # 봇을 온라인 상태로 설정합니다.
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game("헤브스트의 대장간"))  # 상태와 활동 메시지를 원하는 대로 수정할 수 있습니다.

# 봇이 메시지를 수신할 때 실행되는 이벤트 핸들러
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"(엘도르왕국)메시지 감지: {message.content} | 작성자: {message.author}")

    # "헤브스트 말해" 명령어를 처리합니다.
    if message.content.startswith('헤브스트 말해'):
        if message.author.guild_permissions.manage_messages:
            text_to_say = message.content[len('헤브스트 말해 '):]
            await message.delete()  # 이전 메시지 삭제
            await message.channel.send(text_to_say)
        else:
            pass

    await bot.process_commands(message)  # 명령어 처리를 위해 필요한 부분

# 봇 실행
bot.run(TOKEN)
# code 저장 식별번호 : 01-헤브스트