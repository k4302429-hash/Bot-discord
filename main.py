# ───── MANTER BOT LIGADO ─────
from flask import Flask
import threading
app = Flask('')
@app.route('/')
def home(): return "✅ BOT LOJA ONLINE! 🎉"
def manter_ligado(): app.run(host='0.0.0.0', port=10000)
threading.Thread(target=manter_ligado, daemon=True).start()
# ──────────────────────────────

import discord
from discord import app_commands, Embed, Interaction, ButtonStyle
from discord.ui import View, Button

TOKEN = "COLA_SEU_TOKEN_AQUI"

SERVIDOR_ID = 1543047860520489020
CATEGORIA_TICKET_ID = 1543048380387827832

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
arvore = app_commands.CommandTree(bot)

loja = {
    "nome": "🏆 Filas Premium Store",
    "pix": "b78e5162-fba6-4310-8d7e-bc36ae179556",
    "qr_url": "",
    "tempo_expira": "15 minutos"
}

produtos = {}
contador = 0


@arvore.command(name="configurar", description="⚙️ Configurar Loja", guild=discord.Object(id=SERVIDOR_ID))
async def configurar(interaction: Interaction, nome: str, chave_pix: str, link_qr: str = "", tempo_expira: str = "15 minutos"):
    await interaction.response.defer(ephemeral=True)
    loja["nome"] = nome
    loja["pix"] = chave_pix
    loja["qr_url"] = link_qr
    loja["tempo_expira"] = tempo_expira
    await interaction.followup.send("✅ Loja configurada!", ephemeral=True)


@arvore.command(name="adicionar", description="➕ Adicionar produto", guild=discord.Object(id=SERVIDOR_ID))
@app_commands.choices(entrega=[
    app_commands.Choice(name="🤖 Automática", value="auto"),
    app_commands.Choice(name="👤 Manual", value="manual")
])
async def adicionar(interaction: Interaction, nome: str, preco: float, estoque: str, entrega: app_commands.Choice[str], descricao: str = ""):
    await interaction.response.defer(ephemeral=True)
    global contador
    qtd = 999999 if estoque.lower() == "infinito" else int(estoque)
    produtos[str(contador)] = {"nome": nome, "preco": preco, "estoque": qtd, "entrega": entrega.value, "descricao": descricao}
    await interaction.followup.send(f"✅ Salvo! ID: `{contador}`", ephemeral=True)
    contador += 1


@arvore.command(name="loja", description="🛒 Ver Loja", guild=discord.Object(id=SERVIDOR_ID))
async def loja_cmd(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    if not produtos: return await interaction.followup.send("📭 Vazia!", ephemeral=True)
    v = View(timeout=None)
    emb = Embed(title=f"🏆 {loja['nome']}", color=0xffd700)
    emb.set_footer(text="👇 Clique no botão VERDE!")
    for pid, p in produtos.items():
        emb.add_field(name=p['nome'], value=f"💰 R$ {p['preco']:.2f}", inline=False)
        v.add_item(Button(style=ButtonStyle.green, label=f"✅ Comprar — R$ {p['preco']:.2f}", custom_id=f"compra_{pid}"))
    await interaction.followup.send(embed=emb, view=v, ephemeral=False)


@bot.event
async def on_interaction(inter: Interaction):
    if not inter.data: return
    cid = inter.data.get("custom_id","")
    if not cid.startswith("compra_"): return
    await inter.response.defer(ephemeral=True)
    pid = cid[7:]
    if pid not in produtos: return await inter.followup.send("❌ Erro!", ephemeral=True)
    p = produtos[pid]
    cat = inter.guild.get_channel(CATEGORIA_TICKET_ID)
    if not cat: return await inter.followup.send("❌ Pasta não encontrada!", ephemeral=True)
    canal = await inter.guild.create_text_channel(
        f"compra-{inter.user.name[:5]}", category=cat,
        overwrites={inter.guild.default_role: discord.PermissionOverwrite(view_channel=False), inter.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
    )
    emb = Embed(title="🧾 PAGAMENTO", color=0x2ecc71)
    emb.add_field(name="📦 Produto", value=p['nome'], inline=False)
    emb.add_field(name="💰 Valor", value=f"R$ {p['preco']:.2f}", inline=False)
    emb.add_field(name="⏱️ Expira em", value=loja['tempo_expira'], inline=False)
    emb.add_field(name="🔑 PIX", value=f"`{loja['pix']}`", inline=False)
    await canal.send(inter.user.mention, embed=emb)
    await inter.followup.send(f"✅ Acesse: {canal.mention}", ephemeral=True)


@bot.event
async def on_ready():
    await arvore.sync(guild=discord.Object(id=SERVIDOR_ID))
    print(f"✅ ONLINE: {bot.user}")


bot.run()
  
