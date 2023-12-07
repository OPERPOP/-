import nextcord
from nextcord.ext import commands
import random
import asyncio
import string
from collections import OrderedDict
import aiohttp
import io

bot = commands.Bot(command_prefix="/", intents=nextcord.Intents.all())

TOKEN = "MTEzODQzNjU0MzUzNTY0ODg3OQ.GDO1gc.Sl15KMWrQozXJVPQW13Byi7ftKvwgcg_ROnxfI"
ELDOR_SERVER_ID = 1142431335512817665  # Replace with your "엘도르왕국" server's ID
NEW_WORLD_SERVER_ID = 1138038181502140436  # Replace with your "New World Community 2" server's ID

user_balances = {}
user_nicknames = {}
command_counter = {}
custom_responses = {}
mimic_responses = {}
user_states = {}
message_id_to_delete = {}
weapons = {}
custom_responses = OrderedDict()
channel_to_emoji_roles = {
    1142453799810777168: {  # 채널 ID 1에 대한 설정 , 헤브스트 대장간
        '1️⃣': {
            'remove_roles': ["1142453799810777168", "1142453830466928670"],  # 이모지 1에 해당하는 박탈할 역할 이름 목록
            'add_roles': ["1142451749400105180"]                           # 이모지 1에 해당하는 부여할 역할 이름 목록
        },
    },
    1142445272413241455: {  # 채널 ID 1에 대한 설정 , 크라운 지구
        '1️⃣': {
            'remove_roles': ["1142445272413241455", "1142445204658462891"],  # 이모지 1에 해당하는 박탈할 역할 이름 목록
            'add_roles': ["1142451749400105180"]                           # 이모지 1에 해당하는 부여할 역할 이름 목록
        },
    },
    1142451123576385578: {  # 채널 ID 2에 대한 설정 , 브라이트 지구
        '1️⃣': {
            'remove_roles': ["1142451123576385578", "1142451749400105180"],  # 이모지 3에 해당하는 박탈할 역할 이름 목록
            'add_roles': ["1142453830466928670"]                           # 이모지 3에 해당하는 부여할 역할 이름 목록 , 헤브스트 대장간-이동
        },
        '2️⃣': {
            'remove_roles': ["1142451123576385578", "1142451749400105180"],  # 이모지 4에 해당하는 박탈할 역할 이름 목록
            'add_roles': ["1142445204658462891"]                           # 이모지 4에 해당하는 부여할 역할 이름 목록 , 크라운지구-이동
        },
    }
}


@bot.event
async def on_ready():
    print(f"{bot.user.name} 준비완료!")
    print(bot.user)
    print(f"오늘도 행복한 하루 되시길 바랄게요!")
    print("=================================")


@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    channel_id = payload.channel_id
    guild_id = payload.guild_id
    member_id = payload.user_id

    # 여러 개의 타겟 메시지 ID와 타겟 역할 이름을 리스트로 설정합니다.
    target_emoji = '➡️'  # 원하는 이모지 설정

    target_data = [
        {"message_id": 1153685852518613002, "role_name": "1142453799810777168"},  # 헤브스트 대장간
        {"message_id": 1153685678383710377, "role_name": "1142451123576385578"},  # 브라이트 지구
        {"message_id": 1153685308941017129, "role_name": "1142445272413241455"},  # 크라운 지구
        # 추가적인 타겟 데이터를 필요한 만큼 여기에 추가합니다.
    ]

    if emoji == target_emoji:
        for target in target_data:
            if payload.message_id == target["message_id"]:
                print("이모지와 메시지 ID 조건이 충족됨")  # 디버깅 메시지 추가
                guild = bot.get_guild(guild_id)
                member = guild.get_member(member_id)
                role = nextcord.utils.get(guild.roles, name=target["role_name"])

                if role and member:
                    print(f"멤버 {member.name}에게 역할 {role.name} 부여 시도")
                    await member.add_roles(role)
                else:
                    print("멤버 또는 역할을 찾을 수 없음")
                break  # 다음 타겟 데이터를 확인하지 않고 종료합니다.
    else:
        print("이모지가 일치하지 않음")

    if channel_id in channel_to_emoji_roles:
        guild = bot.get_guild(guild_id)
        member = guild.get_member(member_id)

        # 해당 채널에 대한 이모지와 역할 설정 가져오기
        emoji_roles = channel_to_emoji_roles[channel_id]

        if emoji in emoji_roles:
            # 부여할 역할 이름과 박탈할 역할 이름 가져오기
            add_role_names = emoji_roles[emoji]['add_roles']
            remove_role_names = emoji_roles[emoji]['remove_roles']

            # 박탈할 역할 및 부여할 역할 찾아서 적용
            for role_name in remove_role_names:
                role = nextcord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"멤버 {member.name}에서 역할 {role.name} 박탈 시도")
                    await member.remove_roles(role)
                else:
                    print(f"멤버 {member.name}에서 역할 {role_name}을 찾을 수 없음")

            for role_name in add_role_names:
                role = nextcord.utils.get(guild.roles, name=role_name)
                if role:
                    print(f"멤버 {member.name}에게 역할 {role.name} 부여 시도")
                    await member.add_roles(role)
                else:
                    print(f"멤버 {member.name}에게 역할 {role_name}을 찾을 수 없음")

@bot.event
async def on_member_join(member):
    tutorial_category = nextcord.utils.get(member.guild.categories, name='백색의 공간')
    if tutorial_category:
        tutorial_channel = nextcord.utils.get(tutorial_category.text_channels, name='튜토리얼')

        if tutorial_channel:
            b_role = nextcord.utils.get(member.guild.roles, name='b')
            a_role = nextcord.utils.get(member.guild.roles, name='a')

            if b_role and a_role:
                await member.add_roles(b_role)  # 'b' 역할 부여

                # Set up permissions for the tutorial channel
                await tutorial_channel.set_permissions(member.guild.default_role, read_messages=False, read_message_history=False)
                await tutorial_channel.set_permissions(b_role, read_messages=True)
                await tutorial_channel.set_permissions(member.guild.me, read_messages=True)  # Allow the bot to read messages

                async def delayed_message():
                    await asyncio.sleep(3)
                    await tutorial_channel.send(f"어서오세요! 반가워요! 저는 히마와리라고 해요! 시작하기에 앞서 당신의 이름을 알려주실수있을까요?\n"
                                                "\n"
                                                "```'히마와리 나의 이름은 [플레이어 이름]'\n"
                                                "'/' , 's!' 를 사용하지 않습니다 작성하신 [플레이어 이름]은, 정보창 생성에 활용되니 주의해주세요.```\n"
                                                "\n"
                                                "**`[주의사항]\n"
                                                "첫째, 튜토리얼 에서는 최대한 히마와리를 이용한 명령어를 사용하지 말아주십쇼. 오류가 일어날 경우에는 책임져 드릴수 없습니다.\n"
                                                "둘째, 최대한 튜토리얼 공간은 신속하게 이용해주시길 바랍니다.`**")
                    print(f'{member.display_name} 님이 튜토리얼 채널로 안내 메시지를 받았습니다.')

                bot.loop.create_task(delayed_message())

                def check_response(m):
                    return m.author == member and m.channel == tutorial_channel

                first_response = True  # 첫 번째 응답 여부를 나타내는 변수
                try:
                    while True:
                        response = await bot.wait_for('message', check=check_response)
                        if response.content.startswith("히마와리 나의 이름은 "):
                            new_nickname = response.content[len("히마와리 나의 이름은 "):].rstrip("!").rstrip("라고해").rstrip("라고해!").rstrip("이야").rstrip("이야!").rstrip("이라고해").rstrip("이라고해!").rstrip("야!").rstrip("야").rstrip(" ")
                            if new_nickname:
                                await asyncio.sleep(3)
                                await tutorial_channel.send("헤헤, 잠시만 기다려주세요~ 이름을 기록하고 있어요 . .")
                                await asyncio.sleep(3)
                                await tutorial_channel.send("기록되었어요! 앞으로도 잘부탁드려요!\n"
                                                            "\n"
                                                            "`곧, 채널을 이동합니다`")
                                await asyncio.sleep(3)

                                random_role_name = ''.join(random.choices(string.digits, k=13))
                                random_role = await member.guild.create_role(name=random_role_name)
                                await member.add_roles(a_role, random_role)  # 'a' 역할과 랜덤 역할 부여

                                await member.remove_roles(b_role)  # 'b' 역할 박탈

                                player_info_category = nextcord.utils.get(member.guild.categories, name='플레이어 정보창')  # '플레이어 정보창' 카테고리 가져오기
                                if player_info_category:
                                    overwrites = {
                                        member.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                                        random_role: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                                    }

                                    channel = await player_info_category.create_text_channel(name=f'{new_nickname}_정보창', overwrites=overwrites)
                                    await channel.send(f"어서오세요, {new_nickname}씨! 새로운 정보창이 생성되었어요!")
                                    await channel.send(f"여기서는 {new_nickname}씨의 정보를 관리 할수있는 나만의 공간이에요! 편하게 있어주세요! ^^")

                                    print(f'{new_nickname} 씨의 튜토리얼 과정이 완료되었어요!')
                                    break  # 튜토리얼 과정이 끝났으므로 루프 종료
                                else:
                                    print("'플레이어 정보창' 카테고리를 찿을수 없어요!")
                                    break  # 튜토리얼 과정이 끝났으므로 루프 종료
                            else:
                                await tutorial_channel.send("이름을 올바른 형식으로 입력해주세요!\n"
                                                           "`히마와리 나의 이름은 [플레이어 이름]`")
                        elif response.author == member and response.channel == tutorial_channel and first_response:
                            await tutorial_channel.send("..! 이름을 등록하지 않으시면 다음 단계로 갈 수 없어요..!\n"
                                                        "혹시, 등록하시는 방법을 알지 못하시는건가요 ?\n"
                                                        "아래의 방법을 활용해서 이름을 알려주세요 !"
                                                "```'히마와리 나의 이름은 [플레이어 이름]'\n"
                                                "'/' , 's!' 를 사용하지 않습니다 작성하신 [플레이어 이름]은, 정보창 생성에 활용되니 주의해주세요.```\n"
                                                "\n"
                                                "**`[주의사항]\n"
                                                "첫째, 튜토리얼 에서는 최대한 히마와리를 이용한 명령어를 사용하지 말아주세요. 오류가 일어날 경우에는 책임져 드릴수 없습니다.\n"
                                                "둘째, 최대한 튜토리얼 공간은 신속하게 이용해주시길 바랍니다.`**")  
                            first_response = False  # 첫 번째 응답이 처리되었으므로 False로 설정
                except asyncio.TimeoutError:
                    await tutorial_channel.send("앗, 시간이 초과 되었어요!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None:
        return

    if message.guild.id == ELDOR_SERVER_ID:
        await handle_eldor_server_message(message)
    elif message.guild.id == NEW_WORLD_SERVER_ID:
        await handle_new_world_server_message(message)

# ==================================================================================================================================
    if message.content.startswith("/채팅청소하기"):
        await handle_chat_clear_command(message)
# ==================================================================================================================================
    elif message.content.startswith("/주사위") or message.content.startswith("/r"):
        content_parts = message.content.split()

        if len(content_parts) == 2:
            expression = content_parts[1]
            result_message = handle_roll_dice_command(expression)

            if result_message:
                await message.channel.send(result_message)
            else:
                await message.channel.send("주사위 표현이 올바르지 않아요! 다시 굴려주세요!")
        else:
            await message.channel.send("주사위 표현이 올바르지 않아요! 다시 굴려주세요!")

# ==================================================================================================================================
    elif message.content == "/명령어":
        await handle_command_list_command(message)

    await bot.process_commands(message)
# ==================================================================================================================================


async def handle_eldor_server_message(message):
    # Handle messages for "엘도르왕국" server
    if message.content.startswith("엘도르왕국 명령어"):
        await message.channel.send("엘도르왕국에 맞는 명령어 처리")
    if message.author == bot.user:
        return

    print(f"(엘도르왕국)메시지 감지: {message.content} | 작성자: {message.author}")

    if message.content.startswith("히마와리 말해 "):
        if message.author.guild_permissions.manage_messages:
            text_to_say = message.content[len("히마와리 말해 "):]
            await message.delete()  # 이전 메시지 삭제
            await message.channel.send(text_to_say)
        else:
            pass

    await bot.process_commands(message)  # 명령어 처리를 위해 필요한 부분

    if message.content == '히마와리 이동':
        await message.delete()
        channel_id = message.channel.id
        if channel_id in channel_to_emoji_roles:
            response_msg = await message.channel.send('어디로 이동하시겠나요?')
            emoji_roles = channel_to_emoji_roles[channel_id]
            emojis = list(emoji_roles.keys())
            for emoji in emojis:
                await response_msg.add_reaction(emoji)
                
            try:
                await bot.wait_for('reaction_add', timeout=10, check=lambda r, u: u == message.author and r.message.id == response_msg.id)
                await response_msg.delete()
                await response_msg.delete()
            except asyncio.TimeoutError:
                await response_msg.delete()
                await message.channel.send('시간이 초과되었어요. 다시 한번 시도해주세요!', delete_after=5)
    else:
        await bot.process_commands(message)

    if message.author == bot.user:
        return  # 봇 자신의 메시지는 무시

    content = message.content.lower()  # 메시지 내용을 소문자로 변경
    if content.startswith('히마와리 무기'):
        command_args = content.split()
        if len(command_args) < 3:
            await message.channel.send("명령어가 올바르지 않습니다.")
            return

        command = command_args[2]
        author = message.author
        weapon_name = ' '.join(command_args[3:])

        if command == '목록':
            weapon_list = "\n".join(weapons.keys())
            await message.channel.send(f'현재 무기 목록:\n{weapon_list}')
        elif command == '만들기':
            if weapon_name not in weapons:
                weapons[weapon_name] = {
                    '데미지': None,
                    '속성': None,
                    '범위': None,
                    '자격': None,
                    '내구도': None
                }
                await message.channel.send(f'{weapon_name} 무기가 생성되었습니다.')
            else:
                await message.channel.send(f'{weapon_name} 무기는 이미 존재합니다.')
        elif command == '데미지설정':
            if len(command_args) == 5:
                weapon_name = command_args[3]
                damage_value = command_args[4]
                # 데미지 값이 숫자로만 구성되어 있는지 검사
                if damage_value.isdigit():
                    if weapon_name in weapons:
                        weapons[weapon_name]['데미지'] = int(damage_value)
                        await message.channel.send(f'{weapon_name} 무기의 데미지가 {damage_value}로 설정되었습니다.')
                    else:
                        await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
                else:
                    await message.channel.send("데미지 값은 숫자로만 입력해야 합니다.")
            else:
                await message.channel.send("데미지 설정 명령어의 형식이 올바르지 않습니다.")
        elif command == '속성설정':
            if len(command_args) == 5:
                weapon_name = command_args[3]
                element_value = command_args[4]
                if weapon_name in weapons:
                    weapons[weapon_name]['속성'] = element_value
                    await message.channel.send(f'{weapon_name} 무기의 속성이 {element_value}로 설정되었습니다.')
                else:
                    await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
            else:
                await message.channel.send("속성설정 명령어의 형식이 올바르지 않습니다.")
        elif command == '범위설정':
            if len(command_args) == 5:
                weapon_name = command_args[3]
                range_value = command_args[4]
                if weapon_name in weapons:
                    if range_value.isdigit():
                        weapons[weapon_name]['범위'] = int(range_value)
                        await message.channel.send(f'{weapon_name} 무기의 범위가 {range_value}로 설정되었습니다.')
                    else:
                        await message.channel.send("범위 값은 숫자로 입력해야 합니다.")
                else:
                    await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
            else:
                await message.channel.send("범위설정 명령어의 형식이 올바르지 않습니다.")
        elif command == '자격설정':
            if len(command_args) >= 4:
                weapon_name = command_args[3]
                role_name = ' '.join(command_args[4:])
                if weapon_name in weapons:
                    weapons[weapon_name]['자격'] = role_name
                    await message.channel.send(f'{weapon_name} 무기의 자격이 {role_name}으로 설정되었습니다.')
                else:
                    await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
            else:
                await message.channel.send("자격 설정 명령어의 형식이 올바르지 않습니다.")
        elif command == '정보보기':
            if weapon_name in weapons:
                weapon_info = weapons[weapon_name]
                info_message = f'**{weapon_name} 무기 정보**\n'

                if weapon_info["데미지"] is not None:
                    info_message += f'데미지: {weapon_info["데미지"]}\n'

                if weapon_info["속성"]:
                    info_message += f'속성: {weapon_info["속성"]}\n'

                if weapon_info["범위"] is not None:
                    info_message += f'범위: {weapon_info["범위"]}\n'

                if weapon_info["자격"]:
                    info_message += f'자격: {weapon_info["자격"]}\n'

                if weapon_info["내구도"] is not None:
                    info_message += f'내구도: {weapon_info["내구도"]}\n'

                if '능력' in weapon_info:
                    abilities = weapon_info['능력']
                    info_message += f'능력: {abilities}\n'

                if '설명' in weapon_info:
                    description = weapon_info['설명']
                    info_message += f'설명: {description}\n'

                image_url = weapon_info.get("이미지")  # 이미지 URL 가져오기
                if image_url:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(image_url) as resp:
                            if resp.status == 200:
                                # 이미지 다운로드 및 Discord에 파일로 첨부
                                image_bytes = await resp.read()
                                image_file = nextcord.File(io.BytesIO(image_bytes), filename="image.png")
                                await message.channel.send(info_message, file=image_file)
                            else:
                                await message.channel.send("이미지를 다운로드할 수 없습니다.")
                else:
                    await message.channel.send(info_message)
            else:
                await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
                        
        # 이미지설정 명령어 추가
        elif command == '이미지설정':
            if len(command_args) >= 4:
                weapon_name = command_args[3]
                
                # 이미지 파일 첨부 확인
                if len(message.attachments) > 0:
                    image_url = message.attachments[0].url
                    if weapon_name in weapons:
                        weapons[weapon_name]['이미지'] = image_url
                        await message.channel.send(f'{weapon_name} 무기의 이미지가 설정되었습니다.')
                    else:
                        await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
                else:
                    await message.channel.send("이미지를 첨부해야 합니다.")
            else:
                await message.channel.send("이미지설정 명령어의 형식이 올바르지 않습니다.")
        elif command == '능력설정':
            if len(command_args) >= 4:
                weapon_name = command_args[3]
                abilities = ' '.join(command_args[4:])
                if weapon_name in weapons:
                    weapons[weapon_name]['능력'] = abilities
                    await message.channel.send(f'{weapon_name} 무기의 능력이 설정되었습니다.')
                else:
                    await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
            else:
                await message.channel.send("능력 설정 명령어의 형식이 올바르지 않습니다.")
        elif command == '설명':
            if len(command_args) >= 4:
                weapon_name = command_args[3]
                description = ' '.join(command_args[4:])
                if weapon_name in weapons:
                    weapons[weapon_name]['설명'] = description
                    await message.channel.send(f'{weapon_name} 무기에 설명이 추가되었습니다.')
                else:
                    await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
            else:
                await message.channel.send("무기설명 명령어의 형식이 올바르지 않습니다.")
        elif command == '내구도설정':
            if len(command_args) == 5:
                weapon_name = command_args[3]
                durability_value = command_args[4]
                if weapon_name in weapons:
                    if durability_value.isdigit():
                        weapons[weapon_name]['내구도'] = int(durability_value)
                        await message.channel.send(f'{weapon_name} 무기의 내구도가 {durability_value}로 설정되었습니다.')
                    else:
                        await message.channel.send("내구도 값은 숫자로만 입력해야 합니다.")
                else:
                    await message.channel.send(f'{weapon_name} 무기를 찾을 수 없습니다.')
            else:
                await message.channel.send("내구도설정 명령어의 형식이 올바르지 않습니다.")

#==================================================================================================================================
# 재화 시스템 공간
#==================================================================================================================================

async def handle_new_world_server_message(message):
    # Handle messages for "New World Community 2" server
    if message.author == bot.user:
        return

    print(f"(New World Community 2)메시지 감지: {message.content} | 작성자: {message.author}")

    if message.content.startswith("히마와리 나의 이름은 "):
        new_nickname = message.content[len("히마와리 나의 이름은 "):].rstrip("!").rstrip("라고해").rstrip("라고해!").rstrip("이야").rstrip("이야!").rstrip("이라고해").rstrip("이라고해!").rstrip("야!").rstrip("야").rstrip(" ")
        user_nicknames[message.author.id] = {"name": new_nickname, "greeted": False}
        await message.channel.send(f"이름이 {new_nickname} 맞으신가요? 예쁜 이름이네요! 잊지 않을게요! ^^")
        return

    elif message.content.startswith("히마와리 안녕"):
        if message.author.id in user_nicknames:
            nickname = user_nicknames[message.author.id]["name"]
            if not user_nicknames[message.author.id]["greeted"]:
                await message.channel.send(f"안녕하세요! {nickname}씨! 오늘도 바쁜하루네요! ^^")
                user_nicknames[message.author.id]["greeted"] = True
            else:
                responses = [
                    "오늘은 날씨가 좋네요! ... 사실 날씨가 어떤지는 잘모르지만요 (웃음)",
                    "응..? 안녕하세요! 말 친구가 필요하신가요? ^^",
                    "앗 죄송해요! 거기 있는지 몰랐어요!\n"
                    "\n"
                    "`히마와리는 놀란듯한 표정을 지으며 입가에 손을 가져갔다`"
                ]
                await message.channel.send(random.choice(responses))
        else:
            command = "히마와리 안녕"
            if message.author.id in command_counter:
                command_counter[message.author.id][command] += 1
            else:
                command_counter[message.author.id] = {command: 1}
                
            count = command_counter[message.author.id][command]
            if count >= 5:
                await message.channel.send(
                    "... ...\n"
                    "`히마와리의 따끔한 시선이 느껴진다`\n"
                    "`더이상 히마와리는 대답해줄 생각이 없어보인다`"
                )
            elif count >= 4:
                await message.channel.send(
                    "..?\n"
                    "`히마와리는 갸웃하며 당신의 얼굴을 바라보았다`"
                )
            elif count >= 3:
                await message.channel.send(
                    "..자고 일어나면 왜인지는 잘모르겠지만 모두의 이름이 잘 기억이 안나요..\n"
                    "`히마와리는 침울한 표정으로 말했다`\n"
                    "\n"
                    "```[INFO]\n"
                    "\n"
                    "서버의 시스템 점검이 있는 경우에 등록되어있는 이름이 초기화 될수있습니다 불편을 끼쳐드려 죄송합니다```"
                )
            elif count == 2:
                await message.channel.send(
                    "아, 혹시 저가 까먹은건가요..? 앗! 죄송해요!\n"
                    "괜찮으시다면 저에게 다시한번 이름을 알려주실수있을까요? ..\n"
                    "\n"
                    "`히마와리가 미안한듯한 표정으로 당신에게 사과하며 말했다`"
                )
            else:
                await message.channel.send(
                    "아직 이름을 만드시지 않으셨나보네요? 이름을 등록해주신후에 다시 말을 걸어주세요!\n"
                    "\n"
                    "```'히마와리 나의 이름은 [플레이어 이름]'\n"
                    "'/' , 's!' 를 사용하지 않습니다.```"
                )

    if message.content == "등록된 반응 보기":
        if message.author.guild_permissions.administrator:
            response = "**```ansi\n"
            response += "[0;32m등록된 반응 리스트[0m```**\n"
            for keyword, data in custom_responses.items():
                if isinstance(data, dict):  # 값이 딕셔너리인 경우
                    response_text = data["response_text"]
                    input_user_id = data.get("input_user_id", message.author.id)  # 사용자 ID 가져오기
                    user_nickname = user_nicknames.get(input_user_id, {"name": "플레이어"})["name"]
                    author_id = input_user_id  # 반응을 입력한 사용자의 ID
                else:  # 값이 문자열인 경우
                    response_text = data
                    user_nickname = user_nicknames.get(message.author.id, {"name": "플레이어"})["name"]
                    author_id = message.author.id  # 반응을 입력한 사용자의 ID

                response += f"**`반응해야하는 말 : {keyword} - 히마와리가 대답하는 말 : {response_text} / 작성자: {user_nicknames.get(author_id, {'name': '알 수 없음'})['name']}`**\n"

            await message.author.send(response)  # 개인 메시지로 전송
        else:
            await message.channel.send("등록된 반응을 관리할 수 있는 권한이 없어요!")  # 권한 없음 메시지 출력

    if message.content.startswith("히마와리 따라해봐"):
        if message.author.id in user_nicknames:
            if message.author.id not in command_counter or command_counter[message.author.id].get("히마와리 따라해봐", 0) < 1:
                if message.author.id in command_counter:
                    if "히마와리 따라해봐" in command_counter[message.author.id]:
                        command_counter[message.author.id]["히마와리 따라해봐"] += 1
                    else:
                        command_counter[message.author.id]["히마와리 따라해봐"] = 1
                else:
                    command_counter[message.author.id] = {"히마와리 따라해봐": 1}

                await message.channel.send("앗!, 새로운 말을 알려주시는 건가요? 알려주세요!\n"
                                           "어느 상황에서 사용하는게 좋을까요?\n"
                                           "\n"
                                           "`히마와리가 반응해야하는 말을 적어주세요! ex) 히마와리 귀여워!`\n"
                                           "```css\n"
                                           "사용 가능 횟수 (1/0)```\n"
                                           "`한번만 사용가능하니 신중하게 작성해주시길 바랍니다.`\n"
                                           "`이미 학습한 말인 경우에는 취소 될수 있습니다.`")
                def check_reaction(m):
                    return m.author == message.author and m.channel == message.channel

                try:
                    reaction = await bot.wait_for('message', check=check_reaction, timeout=30)
                    reaction_input = reaction.content
                    if reaction_input in custom_responses:
                        await message.channel.purge(limit=1)
                        await message.channel.send(" 앗, 죄송해요 이미 학습한 말이에요!\n"
                                                   "\n"
                                                   "`히마와리가 미안한듯한 표정을 짓는다.`")
                    else:
                        author_id = message.author.id
                        if author_id not in user_nicknames:
                            user_nicknames[author_id] = {"name": "플레이어", "greeted": False}
                        await message.channel.send("뭐라고 대답하는게 좋을까요?\n"
                                                   "\n"
                                                   "`히마와리에게 말해주었으면 하는 대사를 적어주세요! ex) 감사해요!`")
                        try:
                            response = await bot.wait_for('message', check=check_reaction, timeout=300)
                            response_input = response.content
                            # Add to the ordered dictionary
                            custom_responses[reaction_input] = {"response_text": response_input, "input_user_id": author_id,}
                            response_text = custom_responses[reaction_input]["response_text"]
                            nickname = user_nicknames[author_id]['name']
                            await message.channel.send(f"앗 알겠어요! 가르쳐주셔서 감사해요! 다음에 {nickname} 씨가 가르쳐주신 대로 말해볼게요...!")

                            while True:
                                try:
                                    response = await bot.wait_for('message', check=check_reaction, timeout=300)
                                    response_input = response.content
                                    if response_input in custom_responses:
                                       await message.channel.purge(limit=1)
                                       await message.channel.send(custom_responses[response_input]["response_text"])
                                    else:
                                        await message.channel.send()
                                except Exception as e:
                                    pass
                        except asyncio.TimeoutError:
                            await message.channel.send("앗, 죄송해요 다시한번 말씀해주시겠어요? [시간 초과]")
                except asyncio.TimeoutError:
                    await message.channel.send("앗, 죄송해요 다시한번 말씀해주시겠어요? [시간 초과]")
            else:
                await message.channel.send("```css\n"
                                           "'히마와리 따라해봐' 사용 횟수 (1/1) 더이상 불가능해요!``` ")
        else:
            command = "히마와리 따라해봐"
            if message.author.id in command_counter:
                command_counter[message.author.id][command] += 1
            else:
                command_counter[message.author.id] = {command: 1}
            count = command_counter[message.author.id][command]
            if count >= 5:
                await message.channel.send("`히마와리는 당신을 경계합니다.`")
            elif count >= 4:
                await message.channel.send(".. 저에게 이상한 말을 가르치시려는거죠..!"
                                           "\n"
                                           "`히마와리는 당신을 경계하며 소리쳤습니다`")
            elif count >= 3:
                await message.channel.send("... 에..? "
                                           "\n"
                                           "`히마와리가 당신을 바라보며 고개를 갸웃합니다`")
            elif count == 2:
                await message.channel.send("엣, 이름을 모르겠어요..! 이상하다.. 말씀해주셧으면 잊었을리 없을텐데..")
            else:
                await message.channel.send("앗, '히마와리 따라해봐' 명령어를 더 이상 실행할수 없게되었어요..!\n"
                                           "\n"
                                           "`가급적 히마와리 명령어를 튜토리얼에서 사용하지 말아주십쇼.`")

    elif message.content in custom_responses:
        await message.channel.send(custom_responses[message.content])

    await bot.process_commands(message)

    if message.content == "플레이어 이름 리스트":
        if user_nicknames:
            name_list = "\n".join([f"{member_name['name']}" for member_id, member_name in user_nicknames.items()])
            await message.channel.send(f"등록된 플레이어 이름 리스트:\n{name_list}")
        else:
            await message.channel.send("아직 등록된 플레이어 이름이 없어요!")

    if message.content.startswith("히마와리 말해 "):
        text_to_say = message.content[len("히마와리 말해 "):]
        await message.delete()  # 이전 메시지 삭제
        await message.channel.send(text_to_say)

    await bot.process_commands(message)  # 명령어 처리를 위해 필요한 부분

async def reset_greetings():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(86400)  # 24 hours in seconds
        for user_id in user_nicknames:
            user_nicknames[user_id]["greeted"] = False

#==================================================================================================================================
# /채팅청소하기 (갯수) 명령어
async def handle_chat_clear_command(message):
    if message.guild and (message.guild.id == NEW_WORLD_SERVER_ID or message.guild.id == ELDOR_SERVER_ID):
        if message.author.guild_permissions.manage_messages:
            content_parts = message.content.split()
            if len(content_parts) == 2 and content_parts[1].isdigit():
                amount = int(content_parts[1])
                deleted_messages = await message.channel.purge(limit=amount + 1)
                
                # 봇의 응답 메시지 보내기
                response_message = await message.channel.send(f'슥삭..! 슥삭..! {amount} 개의 채팅 청소가 완료되었어요..!')
                
                # 일정 시간이 지난 후 메시지 삭제
                await asyncio.sleep(5)
                
                # 봇의 응답 메시지 삭제
                await response_message.delete()
                
                # 사용자의 명령어 메시지 삭제
                await message.delete()
            else:
                await message.channel.send("명령어 형식이 잘못되었어요. `/채팅청소하기 (지울갯수)`와 같이 입력해주세요.")
        else:
            await message.channel.send("앗, 죄송해요! 모르는 분의 말은 듣지 말라고 들어서..")
#==================================================================================================================================
# 주사위 명령어 
import random

def handle_roll_dice_command(expression):
    try:
        results = []
        total = 0
        bonus = 0
        operator = None
        notation_type = None

        # 주사위 표기에 따라 분기 처리
        if 'd' in expression:
            if '+' in expression or '-' in expression:
                operators = ['+', '-']
                operator = next((op for op in operators if op in expression), None)
                dice_notations = expression.split(operator)
                if len(dice_notations) > 1 and 'd' in dice_notations[1]:
                    notation_type = "B"
                else:
                    notation_type = "C"

                for dice_notation in dice_notations:
                    if 'd' in dice_notation:
                        rolls, limit = map(int, dice_notation.split('d'))
                        result = [random.randint(1, limit) for _ in range(rolls)]
                        results.append(result)

                result_message = (f"**```css\n"
                                  "주사위 명령\n"
                                  f"[{expression}]\n")

                if notation_type == "C" and len(results) > 0:
                    bonus_adjustment = int(expression.split(operator)[1])  # 사용자가 입력한 보정치 추출
                    result_message += f"주사위 결과: [{', '.join(map(str, results[0]))}] = {sum(results[0])}\n"
                    bonus_string = ', '.join(map(str, [bonus_adjustment]))  # 보정치를 보정치 리스트로 만들어서 출력
                    result_message += f"보정치: [{bonus_string}]\n"

                    if operator == '+':
                        total = sum(results[0]) + bonus_adjustment  # 보정치를 더해주기
                    elif operator == '-':
                        total = sum(results[0]) - bonus_adjustment  # 보정치를 빼주기

                    result_message += f"총 결과 : {total}\n```**"
                else:
                    for i, result in enumerate(results):
                        result_message += f"주사위{i+1} 결과: [{', '.join(map(str, result))}] = {sum(result)}\n"
                    if len(results) > 1:
                        if operator == '+':
                            total = sum(sum(result) for result in results)
                            bonus = sum(results[1])
                        elif operator == '-':
                            total = sum(results[0]) - sum(results[1])
                            bonus = sum(results[1])
                        result_message += f"총 결과: {total}\n```**"
            else:
                rolls, limit = map(int, expression.split('d'))
                result = [random.randint(1, limit) for _ in range(rolls)]
                total = sum(result)
                notation_type = "A"
                result_message = (f"**```css\n"
                                  "주사위 명령\n"
                                  f"[{expression}]\n")
                result_message += f"주사위 결과: [{', '.join(map(str, result))}] = {total}\n```**"

        return result_message
    except Exception as e:
        print(f"주사위 명령어 실행 중 오류 발생: {e}")
        return None  # 오류가 발생하면 None을 반환하여 오류 메시지를 출력하도록 합니다.

expressions = ["2d6+2d6", "2d6-2d6", "2d6", "2d6+2", "2d6-2"]
for expression in expressions:
    result_message = handle_roll_dice_command(expression)
    if result_message:
        print(result_message)
#==================================================================================================================================
#/명령어 command_list 
async def handle_command_list_command(message):
    if message.guild and (message.guild.id == NEW_WORLD_SERVER_ID or message.guild.id == ELDOR_SERVER_ID):
        if message.author.guild_permissions.administrator:
            command_names = [command.name for command in bot.commands]
            command_list = ', '.join(command_names)
            await message.author.send(f'```등록된 명령어 : {command_list}```')
            await message.channel.send('`명령어 목록을 개인 메시지로 전달해드렸어요..!`')
        else:
            await message.channel.send('응..? 명령어에 접근할 수 있는 권한이 없으신 것 같아요..!')
#==================================================================================================================================
bot.loop.create_task(reset_greetings())
bot.run(TOKEN)

# code 저장 식별번호 : 06-히마와리