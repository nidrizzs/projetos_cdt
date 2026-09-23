import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pygame
from datetime import datetime

# ==========================================================
# 🎵 CONFIGURAÇÃO E CONTROLE DE ÁUDIO (PYGAME)
# ==========================================================

pygame.mixer.init()

def tocar_notificacao():
    """Toca um efeito sonoro rápido ao realizar uma venda."""
    try:
        som = pygame.mixer.Sound("notificacao.mp3")
        som.play()
    except Exception:
        pass

def alternar_musica():
    """Liga ou desliga a música de fundo da sorveteria."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        btn_musica.config(text="🎵 Ligar Música")
    else:
        try:
            pygame.mixer.music.load("musica.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
            btn_musica.config(text="🔇 Parar Música")
        except Exception:
            messagebox.showwarning(
                "⚠️ Áudio não encontrado", 
                "Certifique-se de que o arquivo 'musica.mp3' está salvo na mesma pasta do seu código Python!"
            )

# ==========================================================
# 🎨 DADOS E PALETA DE CORES (AZUL E AMARELO)
# ==========================================================

CORES = {
    "fundo": "#F4F7FC",           # Azul/cinza muito claro para o fundo
    "branco": "#FFFFFF",          # Branco puro
    "azul_escuro": "#1A365D",     # Azul escuro elegante (textos e títulos)
    "azul_primario": "#0056B3",   # Azul royal (elementos principais)
    "azul_suave": "#EBF8FF",      # Azul clarinho para campos e fundos secundários
    "amarelo": "#FFC107",         # Amarelo vibrante (botões e destaques)
    "amarelo_claro": "#FFF9C4",   # Amarelo suave pastel (cards e formulários)
    "texto": "#0D253F",           # Cor de texto principal
    "cinza": "#64748B",           # Rótulos secundários
    "borda": "#CBD5E1"            # Bordas de separação
}

caixa = 500.00
vendas_dia = 0
itens_vendidos = 0

tamanhos = {
    "Pequeno (200ml)": 1.0,
    "Médio (400ml)": 1.5,
    "Grande (700ml)": 2.0
}

sabores = {
    "Chocolate": [8.00, 140, "chocolate.png"],
    "Morango": [8.00, 140, "morango.png"],
    "Baunilha": [8.00, 140, "baunilha.png"],
    "Blue Ice": [10.00, 140, "blue_ice.png"],
    "Açaí": [11.00, 140, "acai.png"],
    "Pistache": [14.00, 100, "pistache.png"],
    "Menta com Chips": [9.50, 120, "menta.png"],
    "Doce de Leite": [9.00, 130, "doce_de_leite.png"],
    "Maracujá": [8.50, 110, "maracuja.png"],
    "Cookie & Cream": [11.00, 120, "cookies.png"],
    "Frutas Vermelhas": [12.00, 90, "frutas_vermelhas.png"],
    "Ninho com Nutella": [13.00, 110, "ninho_nutella.png"],
    "Chocomint": [10.50, 100, "chocomint.png"],
    "Flocos": [8.50, 130, "flocos.png"],
    "Iogurte com Amora": [11.50, 95, "iogurte.png"]
}

opcoes_sabores = [f"{nome} - R$ {dados[0]:.2f}".replace('.', ',') for nome, dados in sabores.items()]
historico = [("Abertura", "Caixa inicial", "R$ 500,00")]

# ==========================================================
# ⚙️ FUNÇÕES AUXILIARES, NOTIFICAÇÃO E CHAT
# ==========================================================

def carregar_imagem(caminho, largura=130, altura=130):
    try:
        img = Image.open(caminho)
        img = img.resize((largura, altura), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        img = Image.new('RGB', (largura, altura), color='#E2E8F0')
        return ImageTk.PhotoImage(img)

def mostrar_notificacao(titulo, mensagem):
    """Cria um alerta pop-up personalizado no canto inferior da tela."""
    tocar_notificacao()
    
    janela.update_idletasks()
    
    notif = tk.Toplevel(janela)
    notif.overrideredirect(True)
    notif.configure(bg=CORES["amarelo"])
    notif.attributes("-topmost", True)
    
    x = janela.winfo_x() + janela.winfo_width() - 270
    y = janela.winfo_y() + janela.winfo_height() - 140
    notif.geometry(f"260x120+{x}+{y}")
    
    frame_int = tk.Frame(notif, bg=CORES["branco"], highlightbackground=CORES["azul_primario"], highlightthickness=2)
    frame_int.pack(fill="both", expand=True, padx=2, pady=2)
    
    tk.Label(frame_int, text=titulo, font=("Segoe UI", 9, "bold"), fg=CORES["azul_escuro"], bg=CORES["branco"]).pack(anchor="w", padx=8, pady=(5, 2))
    tk.Label(frame_int, text=mensagem, font=("Segoe UI", 8), fg=CORES["texto"], bg=CORES["branco"], justify="left").pack(anchor="w", padx=8)
    
    notif.after(4000, notif.destroy)

def enviar_mensagem_chat(remetente, texto):
    """Adiciona uma mensagem na área de texto do chat interno."""
    hora = datetime.now().strftime("%H:%M")
    txt_chat.config(state="normal")
    txt_chat.insert("end", f"[{hora}] {remetente}:\n{texto}\n\n")
    txt_chat.config(state="disabled")
    txt_chat.see("end")

def enviar_mensagem_usuario(event=None):
    msg = ent_chat.get().strip()
    if msg:
        enviar_mensagem_chat("Atendente", msg)
        ent_chat.delete(0, "end")

def dinheiro(valor):
    return f"R$ {valor:.2f}".replace(".", ",")

def criar_botao(parent, texto, comando):
    return tk.Button(
        parent, text=texto, command=comando, bg=CORES["amarelo"], fg=CORES["azul_escuro"],
        activebackground=CORES["azul_primario"], activeforeground="white",
        font=("Segoe UI", 9, "bold"), bd=0, relief="flat", padx=12, pady=7, cursor="hand2"
    )

def atualizar():
    lbl_caixa.config(text=dinheiro(caixa))
    lbl_vendas.config(text=str(vendas_dia))
    lbl_itens.config(text=str(itens_vendidos))

    tree_estoque.delete(*tree_estoque.get_children())
    for sabor, dados in sabores.items():
        tree_estoque.insert("", "end", values=(sabor, dados[1], dinheiro(dados[0])))

    tree_extrato.delete(*tree_extrato.get_children())
    for item in reversed(historico):
        tree_extrato.insert("", "end", values=item)

def registrar(operacao, detalhe, valor="-"):
    historico.append((operacao, detalhe, valor))
    atualizar()

def extrair_nome_sabor(texto_selecionado):
    if " - R$" in texto_selecionado:
        return texto_selecionado.split(" - R$")[0]
    return texto_selecionado

def ao_selecionar_sabor(event):
    sabor_selecionado = combo_sabor.get()
    nome_sabor = extrair_nome_sabor(sabor_selecionado)
    
    if nome_sabor in sabores:
        arquivo_imagem = sabores[nome_sabor][2]
        nova_img = carregar_imagem(arquivo_imagem, 130, 130)
        lbl_foto_sorvete.config(image=nova_img)
        lbl_foto_sorvete.image = nova_img

def vender():
    global caixa, vendas_dia, itens_vendidos

    sabor_selecionado = combo_sabor.get()
    nome_sabor = extrair_nome_sabor(sabor_selecionado)
    tamanho_nome = combo_tamanho.get()
    colher_opcao = combo_colher.get()
    tipo_pedido = combo_tipo.get()
    brinde_opcao = combo_brinde.get()
    pagamento = combo_pagamento.get()

    if not nome_sabor or not tamanho_nome or not colher_opcao or not tipo_pedido or not brinde_opcao or not pagamento:
        messagebox.showwarning("⚠️ Atenção", "Selecione todos os campos antes de finalizar.")
        return

    try:
        quantidade = int(ent_qtd.get())
        if quantidade <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("❌ Erro", "Digite uma quantidade válida.")
        return

    preco_base = sabores[nome_sabor][0]
    multiplicador = tamanhos[tamanho_nome]
    preco_unitario = preco_base * multiplicador
    estoque = sabores[nome_sabor][1]

    if quantidade > estoque:
        messagebox.showwarning("📦 Estoque insuficiente", f"Temos apenas {estoque} unidade(s) de {nome_sabor}.")
        return

    total = preco_unitario * quantidade
    sabores[nome_sabor][1] -= quantidade
    caixa += total
    vendas_dia += 1
    itens_vendidos += quantidade

    detalhe_venda = f"{quantidade}x {nome_sabor} [{tamanho_nome}] - {tipo_pedido} - Colher: {colher_opcao} - Brinde: {brinde_opcao} - {pagamento}"
    registrar("🛒 Venda", detalhe_venda, dinheiro(total))
    
    # Notificação no Chat
    msg_chat_auto = f"📦 Pedido ({tipo_pedido}): {quantidade}x {nome_sabor} ({tamanho_nome}) | {colher_opcao} | Brinde: {brinde_opcao} | Total: {dinheiro(total)} ({pagamento})"
    enviar_mensagem_chat("🤖 Sistema", msg_chat_auto)

    ent_qtd.delete(0, "end")
    ent_qtd.insert(0, "1")
    
    # Notificação flutuante
    mostrar_notificacao("🔔 Novo Pedido!", f"📍 {tipo_pedido}\n🛒 {quantidade}x {nome_sabor} ({tamanho_nome})\n🥄 {colher_opcao}\n🔑 Brinde: {brinde_opcao}\n💰 {dinheiro(total)} ({pagamento})")
    
    # Confirmação padrão
    messagebox.showinfo("✨ Venda realizada!", f"📍 Tipo: {tipo_pedido}\n🛒 {quantidade}x {nome_sabor} ({tamanho_nome})\n🥄 Colher: {colher_opcao}\n🔑 Brinde: {brinde_opcao}\n💰 Total: {dinheiro(total)}")

# ==========================================================
# 🖥️ INTERFACE GRÁFICA (TKINTER)
# ==========================================================

janela = tk.Tk()
janela.title("🍦 Sorveteria Glacê - Tema Azul & Amarelo 💛💙")
janela.geometry("660x680")
janela.configure(bg=CORES["fundo"])

header = tk.Frame(janela, bg=CORES["azul_escuro"])
header.pack(fill="x", padx=0, pady=0)

lbl_titulo = tk.Label(header, text="🍦 Sorveteria Glacê ☀️", bg=CORES["azul_escuro"], fg=CORES["amarelo"], font=("Segoe UI", 16, "bold"), padx=15, pady=10)
lbl_titulo.pack(side="left")

btn_musica = tk.Button(header, text="🎵 Ligar Música", command=alternar_musica, bg=CORES["amarelo"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold"), bd=0, relief="flat", padx=10, pady=4, cursor="hand2")
btn_musica.pack(side="right", padx=15)

dashboard = tk.Frame(janela, bg=CORES["fundo"])
dashboard.pack(fill="x", padx=12, pady=10)

def criar_card(parent, icone, titulo, valor):
    card = tk.Frame(parent, bg=CORES["amarelo_claro"], highlightbackground=CORES["amarelo"], highlightthickness=1)
    card.pack(side="left", expand=True, fill="both", padx=4)
    
    tk.Label(card, text=icone, bg=CORES["amarelo"], fg=CORES["azul_escuro"], font=("Segoe UI Emoji", 11), width=2).pack(side="left", padx=5, pady=5)
    
    info = tk.Frame(card, bg=CORES["amarelo_claro"])
    info.pack(side="left", padx=5)
    
    tk.Label(info, text=titulo, bg=CORES["amarelo_claro"], fg=CORES["cinza"], font=("Segoe UI", 7, "bold")).pack(anchor="w")
    label = tk.Label(info, text=valor, bg=CORES["amarelo_claro"], fg=CORES["azul_escuro"], font=("Segoe UI", 10, "bold"))
    label.pack(anchor="w")
    return label

lbl_caixa = criar_card(dashboard, "💰", "CAIXA", "R$ 500,00")
lbl_vendas = criar_card(dashboard, "🛒", "VENDAS", "0")
lbl_itens = criar_card(dashboard, "🍨", "ITENS", "0")

# Estilização das Abas
style = ttk.Style()
style.theme_use('default')
style.configure("TNotebook", background=CORES["fundo"], borderwidth=0)
style.configure("TNotebook.Tab", background=CORES["azul_suave"], foreground=CORES["azul_escuro"], font=("Segoe UI", 9, "bold"), padding=[12, 6])
style.map("TNotebook.Tab", background=[("selected", CORES["azul_primario"])], foreground=[("selected", "#FFFFFF")])

notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

aba_vendas = tk.Frame(notebook, bg=CORES["branco"])
aba_estoque = tk.Frame(notebook, bg=CORES["branco"])
aba_extrato = tk.Frame(notebook, bg=CORES["branco"])
aba_chat = tk.Frame(notebook, bg=CORES["branco"])

notebook.add(aba_vendas, text=" 💰 Vendas ")
notebook.add(aba_estoque, text=" 📦 Estoque ")
notebook.add(aba_extrato, text=" 📋 Extrato ")
notebook.add(aba_chat, text=" 💬 Chat ")

# --- ABA VENDAS ---
painel_vendas = tk.Frame(aba_vendas, bg=CORES["branco"])
painel_vendas.pack(fill="both", expand=True, padx=15, pady=10)

form = tk.Frame(painel_vendas, bg=CORES["azul_suave"], highlightbackground=CORES["borda"], highlightthickness=1)
form.pack(side="left", fill="both", expand=True, padx=(0, 10))

# Tipo de Pedido
tk.Label(form, text="🛍️ Tipo:", bg=CORES["azul_suave"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
combo_tipo = ttk.Combobox(form, values=["Comer no local", "Para viagem (Embalado)"], state="readonly", width=24)
combo_tipo.grid(row=0, column=1, padx=5, pady=5)
combo_tipo.set("Comer no local")

# Sabor
tk.Label(form, text="🍨 Sabor:", bg=CORES["azul_suave"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
combo_sabor = ttk.Combobox(form, values=opcoes_sabores, state="readonly", width=24)
combo_sabor.grid(row=1, column=1, padx=5, pady=5)
combo_sabor.bind("<<ComboboxSelected>>", ao_selecionar_sabor)

# Tamanho
tk.Label(form, text="🥤 Tamanho:", bg=CORES["azul_suave"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=5)
combo_tamanho = ttk.Combobox(form, values=list(tamanhos.keys()), state="readonly", width=24)
combo_tamanho.grid(row=2, column=1, padx=5, pady=5)
combo_tamanho.set("Pequeno (200ml)")

# Colher
tk.Label(form, text="🥄 Colher:", bg=CORES["azul_suave"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=5)
combo_colher = ttk.Combobox(form, values=["Com colher (Plástico)", "Com colher (Biodegradável)", "Sem colher"], state="readonly", width=24)
combo_colher.grid(row=3, column=1, padx=5, pady=5)
combo_colher.set("Com colher (Plástico)")

# Brinde (Primeira compra)
tk.Label(form, text="🎁 Brinde:", bg=CORES["azul_suave"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=5)
combo_brinde = ttk.Combobox(form, values=["Chaveiro de sorvete (1ª Compra)", "Nenhum"], state="readonly", width=24)
combo_brinde.grid(row=4, column=1, padx=5, pady=5)
combo_brinde.set("Nenhum")

# Quantidade
tk.Label(form, text="🔢 Quantidade:", bg=CORES["azul_suave"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold")).grid(row=5, column=0, sticky="w", padx=10, pady=5)
ent_qtd = tk.Entry(form, width=26, relief="solid", bd=1)
ent_qtd.insert(0, "1")
ent_qtd.grid(row=5, column=1, padx=5, pady=5, ipady=2)

# Pagamento
tk.Label(form, text="💳 Pagamento:", bg=CORES["azul_suave"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold")).grid(row=6, column=0, sticky="w", padx=10, pady=5)
combo_pagamento = ttk.Combobox(form, values=["Pix", "Cartão de Crédito", "Dinheiro"], state="readonly", width=24)
combo_pagamento.grid(row=6, column=1, padx=5, pady=5)

frame_foto = tk.Frame(painel_vendas, bg=CORES["fundo"], highlightbackground=CORES["borda"], highlightthickness=1)
frame_foto.pack(side="right", fill="both")

img_inicial = carregar_imagem("placeholder.png", 130, 130)
lbl_foto_sorvete = tk.Label(frame_foto, image=img_inicial, bg=CORES["fundo"])
lbl_foto_sorvete.image = img_inicial
lbl_foto_sorvete.pack(padx=15, pady=15)

criar_botao(aba_vendas, "Finalizar Venda 🍨", vender).pack(padx=18, pady=10, anchor="e")

# --- ABA ESTOQUE ---
tree_estoque = ttk.Treeview(aba_estoque, columns=("Sabor", "Qtd", "Preço Base"), show="headings")
tree_estoque.heading("Sabor", text="Sabor")
tree_estoque.heading("Qtd", text="Qtd")
tree_estoque.heading("Preço Base", text="Preço Base (P)")
tree_estoque.pack(fill="both", expand=True, padx=15, pady=10)

# --- ABA EXTRATO ---
tree_extrato = ttk.Treeview(aba_extrato, columns=("Operação", "Detalhe", "Valor"), show="headings")
tree_extrato.heading("Operação", text="Operação")
tree_extrato.heading("Detalhe", text="Detalhe")
tree_extrato.heading("Valor", text="Valor")
tree_extrato.pack(fill="both", expand=True, padx=15, pady=10)

# --- ABA CHAT ---
frame_chat = tk.Frame(aba_chat, bg=CORES["branco"])
frame_chat.pack(fill="both", expand=True, padx=15, pady=10)

txt_chat = tk.Text(frame_chat, wrap="word", state="disabled", font=("Segoe UI", 9), bg=CORES["fundo"], fg=CORES["texto"], bd=1, relief="solid")
txt_chat.pack(fill="both", expand=True, pady=(0, 10))

frame_envio = tk.Frame(frame_chat, bg=CORES["branco"])
frame_envio.pack(fill="x")

ent_chat = tk.Entry(frame_envio, font=("Segoe UI", 9), bd=1, relief="solid")
ent_chat.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 5))
ent_chat.bind("<Return>", enviar_mensagem_usuario)

btn_enviar = tk.Button(frame_envio, text="Enviar 💬", command=enviar_mensagem_usuario, bg=CORES["amarelo"], fg=CORES["azul_escuro"], font=("Segoe UI", 8, "bold"), bd=0, relief="flat", padx=10, pady=4, cursor="hand2")
btn_enviar.pack(side="right")

enviar_mensagem_chat("🤖 Sistema", "Chat ativado! As confirmações de pedidos serão exibidas aqui.")

atualizar()
janela.mainloop()