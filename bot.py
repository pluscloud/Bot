import discord
from discord.ext import commands
import docker
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)
client = docker.from_env()

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.command()
async def create(ctx):
    user_id = ctx.author.id
    container_name = f"vps_{user_id}"

    # Tạo container nếu chưa tồn tại
    try:
        container = client.containers.run(
            image="vps-image",
            name=container_name,
            detach=True,
            tty=True
        )
        await ctx.send(f"✅ VPS được tạo cho <@{user_id}>! Sử dụng `/connect` để lấy SSH.")
    except docker.errors.APIError as e:
        if "Conflict" in str(e):
            await ctx.send("⚠️ VPS đã chạy. Sử dụng `/connect`.")
        else:
            await ctx.send(f"❌ Error: {e}")

@bot.command()
async def connect(ctx):
    user_id = ctx.author.id
    container_name = f"vps_{user_id}"

    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            container.start()

        # lấy SSH dòng từ logs
        logs = container.logs().decode()
        ssh_lines = [line for line in logs.split('\n') if 'ssh' in line]
        if ssh_lines:
            ssh_link = ssh_lines[-1]
            await ctx.send(f"🔗 SSH For <@{user_id}>: `{ssh_link}`")
        else:
            await ctx.send("⏳ Vui lòng đợi vài giây, sau đó thử lại `/connect`.")
    except docker.errors.NotFound:
        await ctx.send("❌Không tìm thấy VPS. Sử dụng `/create` trước.")

bot.run(TOKEN)