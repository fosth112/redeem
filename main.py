import os
import discord
from discord.ext import commands
from discord import ui
from myserver import server_on

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.message_content = True  # ✅ เปิดให้บอทอ่านข้อความได้
intents.guilds = True
intents.members = True  # ✅ เปิดให้บอทจัดการสมาชิกได้ (ให้ Role)

bot = commands.Bot(command_prefix=".", intents=intents)

# ใส่ Role ID ที่ต้องการให้ (ต้องเป็น int)
CUSTOMER_ROLE_ID = 1279035218430263327  

# เมื่อบอทออนไลน์ให้พิมพ์ข้อความใน Terminal และส่งข้อความไปที่ Discord
@bot.event
async def on_ready():
    print("✅ Bot is online and ready!")  # แสดงข้อความใน Terminal
    channel = bot.get_channel(1279036071619072082)
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:  # เลือกแชนแนลที่ส่งได้
                await channel.send("✅ Bot is now online and ready to use! Type `.send_redeem` to start.")
                return

# คำสั่งให้บอทส่ง Embed พร้อมปุ่ม Claim Role
@bot.command()
async def send_redeem(ctx):
    embed = discord.Embed(title="REDEEM KEY",
                          description="👉 ใส่คีย์ของคุณเพื่อรับยศ",
                          color=discord.Color.blue())
    embed.set_footer(text="Developed by 11111")

    view = ClaimRoleView()
    await ctx.send(embed=embed, view=view)

# ปุ่ม Claim Role
class ClaimRoleView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ClaimRoleButton())

class ClaimRoleButton(ui.Button):
    def __init__(self):
        super().__init__(label="🔑 Claim Role", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        modal = RedeemForm()
        await interaction.response.send_modal(modal)

# ฟอร์ม Modal สำหรับให้ผู้ใช้กรอกข้อมูล
class RedeemForm(ui.Modal, title="Claim Your License"):
    invoice_id = ui.TextInput(label="KEY", placeholder="ใส่คีย์", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        key = self.invoice_id.value.strip()  # รับค่าจากฟอร์มและตัดช่องว่าง
        role = interaction.guild.get_role(CUSTOMER_ROLE_ID)

        # ตรวจสอบว่าคีย์มี 10 ตัวอักษรขึ้นไปหรือไม่
        if len(key) >= 10:
            if role:
                await user.add_roles(role)
                await interaction.response.send_message(f"✅ **Success!** {user.mention}, คุณได้รับยศแล้ว **buyer Role โหลดโปรได้เลย ที่ https://discord.com/channels/923167904629928005/1346807138416328714**.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ **Error:** Role not found. Please contact an admin.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ **Invalid Key:** คีย์ไม่ถูกต้อง **...** กรุณาลองใหม่!", ephemeral=True)
server_on()

# รันบอท
bot.run(os.getenv('TOKEN'))
