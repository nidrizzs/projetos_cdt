import tkinter as tk
from tkinter import ttk, messagebox
import re

# ==========================================================
# 🍦 Sorveteria Glacê 🎀
# ==========================================================

CORES = {
    "fundo": "#F4F8FC",
    "branco": "#FFFFFF",
    "azul": "#C75FB4",
    "azul_claro": "#F795D3",
    "azul_medio": "#EF91E2",
    "escuro": "#173B57",
    "texto": "#180D8F",
    "cinza": "#718096",
    "verde": "#35B86B",
    "vermelho": "#E85D5D",
    "borda": "#DCE7F0"
}


# ==========================================================
# 💰 DADOS
# ==========================================================

caixa = 500.00
vendas_dia = 0
itens_vendidos = 0
pedido_chat = None

sabores = {
    "Chocolate": [8.00, 140],
    "Morango": [8.00, 140],
    "Baunilha": [8.00, 140],
    "Coco": [9.00, 140],
    "Limão": [8.50, 140],
    "Blue Ice": [10.00, 140],
    "Flocos": [9.00, 140],
    "Brigadeiro": [10.00, 140],
    "Beijinho": [10.00, 140],
    "Nutella": [12.00, 140],
    "Oreo": [11.00, 140],
    "Açaí": [11.00, 140],
    "Leite Ninho": [11.00, 140],
    "Paçoca": [10.00, 140],
    "Pistache": [13.00, 140]
}

historico = [
    ("Abertura", "Caixa inicial", "R$ 500,00")
]


# ==========================================================
# 💵 DINHEIRO
# ==========================================================

def dinheiro(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


# ==========================================================
# 🔘 BOTÕES
# ==========================================================

def criar_botao(parent, texto, comando, cor=None):

    if cor is None:
        cor = CORES["azul_medio"]

    botao = tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=cor,
        fg="white",
        activebackground=CORES["escuro"],
        activeforeground="white",
        font=("Segoe UI", 8, "bold"),
        bd=0,
        relief="flat",
        padx=10,
        pady=6,
        cursor="hand2"
    )

    botao.bind(
        "<Enter>",
        lambda e: botao.config(
            bg=CORES["escuro"]
        )
    )

    botao.bind(
        "<Leave>",
        lambda e: botao.config(
            bg=cor
        )
    )

    return botao


# ==========================================================
# 🔄 ATUALIZAR
# ==========================================================

def atualizar():

    lbl_caixa.config(
        text=dinheiro(caixa)
    )

    lbl_vendas.config(
        text=str(vendas_dia)
    )

    lbl_itens.config(
        text=str(itens_vendidos)
    )

    baixos = sum(
        1
        for dados in sabores.values()
        if 0 < dados[1] <= 5
    )

    lbl_baixo.config(
        text=str(baixos)
    )

    # ESTOQUE

    tree_estoque.delete(
        *tree_estoque.get_children()
    )

    for sabor, dados in sabores.items():

        preco = dados[0]
        quantidade = dados[1]

        if quantidade == 0:
            status = "❌ Esgotado"

        elif quantidade <= 5:
            status = "⚠️ Baixo"

        else:
            status = "✓ Normal"

        tree_estoque.insert(
            "",
            "end",
            values=(
                sabor,
                quantidade,
                dinheiro(preco),
                status
            )
        )

    # EXTRATO

    tree_extrato.delete(
        *tree_extrato.get_children()
    )

    for item in reversed(historico):

        tree_extrato.insert(
            "",
            "end",
            values=item
        )


# ==========================================================
# 📋 HISTÓRICO
# ==========================================================

def registrar(
    operacao,
    detalhe,
    valor="-"
):

    historico.append(
        (operacao, detalhe, valor)
    )

    atualizar()


# ==========================================================
# 💰 VENDA
# ==========================================================

def mudar_pagamento(event=None):

    if combo_pagamento.get() == "Dinheiro":

        lbl_pago.grid()
        ent_pago.grid()

    else:

        lbl_pago.grid_remove()
        ent_pago.grid_remove()


def vender():

    global caixa
    global vendas_dia
    global itens_vendidos

    sabor = combo_sabor.get()
    pagamento = combo_pagamento.get()

    if not sabor:

        messagebox.showwarning(
            "⚠️ Atenção",
            "Selecione um sabor."
        )

        return

    if not pagamento:

        messagebox.showwarning(
            "⚠️ Atenção",
            "Selecione uma forma de pagamento."
        )

        return

    try:

        quantidade = int(
            ent_qtd.get()
        )

    except ValueError:

        messagebox.showerror(
            "❌ Erro",
            "Digite uma quantidade válida."
        )

        return

    if quantidade <= 0:

        messagebox.showwarning(
            "⚠️ Atenção",
            "A quantidade deve ser maior que zero."
        )

        return

    preco = sabores[sabor][0]
    estoque = sabores[sabor][1]

    if quantidade > estoque:

        messagebox.showwarning(
            "📦 Estoque insuficiente",
            f"Temos apenas {estoque} unidade(s)."
        )

        return

    total = preco * quantidade
    troco = 0

    if pagamento == "Dinheiro":

        try:

            valor_pago = float(
                ent_pago.get().replace(",", ".")
            )

        except ValueError:

            messagebox.showerror(
                "❌ Erro",
                "Digite o valor entregue."
            )

            return

        if valor_pago < total:

            messagebox.showwarning(
                "💵 Valor insuficiente",
                "O valor entregue é menor que o total."
            )

            return

        troco = valor_pago - total

    sabores[sabor][1] -= quantidade

    caixa += total
    vendas_dia += 1
    itens_vendidos += quantidade

    registrar(
        "🛒 Venda",
        f"{quantidade}x {sabor} - {pagamento}",
        dinheiro(total)
    )

    ent_qtd.delete(
        0,
        "end"
    )

    ent_pago.delete(
        0,
        "end"
    )

    mensagem = (
        f"🍦 {quantidade}x {sabor}\n"
        f"💳 Pagamento: {pagamento}\n"
        f"💰 Total: {dinheiro(total)}"
    )

    if pagamento == "Dinheiro":

        mensagem += (
            f"\n💵 Troco: {dinheiro(troco)}"
        )

    messagebox.showinfo(
        "✨ Venda realizada!",
        mensagem
    )


# ==========================================================
# 📦 REPOSIÇÃO
# ==========================================================

def repor_estoque():

    sabor = combo_estoque.get()

    if not sabor:

        messagebox.showwarning(
            "⚠️ Atenção",
            "Selecione um sabor."
        )

        return

    try:

        quantidade = int(
            ent_estoque.get()
        )

    except ValueError:

        messagebox.showerror(
            "❌ Erro",
            "Digite uma quantidade válida."
        )

        return

    if quantidade <= 0:

        messagebox.showwarning(
            "⚠️ Atenção",
            "Digite uma quantidade maior que zero."
        )

        return

    sabores[sabor][1] += quantidade

    registrar(
        "📦 Reposição",
        f"+{quantidade} unidades de {sabor}"
    )

    ent_estoque.delete(
        0,
        "end"
    )

    messagebox.showinfo(
        "✨ Estoque atualizado",
        f"{sabor} recebeu +{quantidade} unidades."
    )


# ==========================================================
# 💬 CHATBOX INTERATIVO
# ==========================================================

def chat_msg(remetente, texto):

    chat.config(
        state="normal"
    )

    chat.insert(
        "end",
        remetente + "\n",
        "nome"
    )

    chat.insert(
        "end",
        texto + "\n\n",
        "mensagem"
    )

    chat.see(
        "end"
    )

    chat.config(
        state="disabled"
    )


def mostrar_botoes_iniciais():

    botoes_opcoes.pack(
        fill="x",
        padx=8,
        pady=5
    )


def esconder_botoes():

    botoes_opcoes.pack_forget()
    botoes_pagamento.pack_forget()


# ==========================================================
# 🍨 PEDIDO PELO CHAT
# ==========================================================

def iniciar_pedido(sabor, quantidade):

    global pedido_chat

    estoque = sabores[sabor][1]
    preco = sabores[sabor][0]

    if quantidade > estoque:

        chat_msg(
            "🍦 Sorveteria Glacê 🎀",
            f"❌ Temos apenas {estoque} unidade(s) de {sabor}."
        )

        return

    pedido_chat = {
        "sabor": sabor,
        "quantidade": quantidade
    }

    botoes_opcoes.pack_forget()

    botoes_pagamento.pack(
        fill="x",
        padx=8,
        pady=5
    )

    total = preco * quantidade

    chat_msg(
        "🍦 Sorveteria Glacê 🎀",
        f"Seu pedido ficou:\n\n"
        f"🍨 {quantidade}x {sabor}\n"
        f"💰 Total: {dinheiro(total)}\n\n"
        "Escolha a forma de pagamento abaixo:"
    )


# ==========================================================
# 💳 PAGAMENTO PELO CHAT
# ==========================================================

def pagamento_chat(forma):

    global caixa
    global vendas_dia
    global itens_vendidos
    global pedido_chat

    if pedido_chat is None:
        return

    botoes_pagamento.pack_forget()

    sabor = pedido_chat["sabor"]
    quantidade = pedido_chat["quantidade"]

    estoque = sabores[sabor][1]
    preco = sabores[sabor][0]

    if quantidade > estoque:

        chat_msg(
            "🍦 Sorveteria Glacê 🎀",
            "❌ O estoque mudou e essa quantidade não está mais disponível."
        )

        pedido_chat = None

        return

    total = preco * quantidade

    sabores[sabor][1] -= quantidade

    caixa += total
    vendas_dia += 1
    itens_vendidos += quantidade

    registrar(
        "💬 Venda pelo Chat",
        f"{quantidade}x {sabor} - {forma}",
        dinheiro(total)
    )

    chat_msg(
        "👤 Você",
        f"Pagamento: {forma}"
    )

    chat_msg(
        "🍦 Sorveteria Glacê 🎀",
        f"✨ Pedido confirmed!\n\n"
        f"🍨 {quantidade}x {sabor}\n"
        f"💳 {forma}\n"
        f"💰 Total: {dinheiro(total)}\n\n"
        "Obrigada pela preferência! 🎀🍦"
    )

    pedido_chat = None

    mostrar_botoes_iniciais()


# ==========================================================
# 🤖 PROCESSAR MENSAGEM
# ==========================================================

def processar_chat(texto):

    texto = texto.lower().strip()

    # ---------------- SAUDAÇÃO ----------------

    if any(
        palavra in texto
        for palavra in [
            "oi",
            "olá",
            "ola",
            "bom dia",
            "boa tarde",
            "boa noite"
        ]
    ):

        chat_msg(
            "🍦 Sorveteria Glacê 🎀",
            "Olá! 🎀😊\n\n"
            "Posso ajudar com seu pedido ou suporte."
        )

        mostrar_botoes_iniciais()

        return

    # ---------------- CARDÁPIO ----------------

    if any(
        palavra in texto
        for palavra in [
            "cardápio",
            "cardapio",
            "sabores",
            "preços",
            "precos"
        ]
    ):

        lista = "\n".join(
            f"🍨 {sabor} — {dinheiro(dados[0])}"
            for sabor, dados in sabores.items()
        )

        chat_msg(
            "🍦 Sorveteria Glacê 🎀",
            "Nosso cardápio é:\n\n" + lista
        )

        return

    # ---------------- SUPORTE ----------------

    if any(
        palavra in texto
        for palavra in [
            "suporte",
            "problema",
            "reclamação",
            "reclamacao",
            "ajuda"
        ]
    ):

        chat_msg(
            "🍦 Sorveteria Glacê 🎀",
            "Claro! 😊\n\n"
            "Digite sua dúvida ou descreva o problema."
        )

        return

    # ---------------- PEDIDO ----------------

    sabor_encontrado = None

    for sabor in sabores:

        if sabor.lower() in texto:

            sabor_encontrado = sabor
            break

    if sabor_encontrado:

        numeros = re.findall(
            r"\d+",
            texto
        )

        quantidade = (
            int(numeros[0])
            if numeros
            else 1
        )

        iniciar_pedido(
            sabor_encontrado,
            quantidade
        )

        return

    # ---------------- AGRADECIMENTO ----------------

    if any(
        palavra in texto
        for palavra in [
            "obrigado",
            "obrigada",
            "valeu",
            "thanks"
        ]
    ):

        chat_msg(
            "🍦 Sorveteria Glacê 🎀",
            "Por nada! 🎀🍦"
        )

        return

    # ---------------- RESPOSTA PADRÃO ----------------

    chat_msg(
        "🍦 Sorveteria Glacê 🎀",
        "Não consegui entender. 😅\n\n"
        "Você pode escrever:\n"
        "• Cardápio\n"
        "• Quero 2 Chocolate\n"
        "• Suporte\n"
        "• Preços"
    )


# ==========================================================
# 📤 ENVIAR MENSAGEM
# ==========================================================

def enviar():

    texto = entrada_chat.get().strip()

    if texto == "":
        return

    chat_msg(
        "👤 Você",
        texto
    )

    entrada_chat.delete(
        0,
        "end"
    )

    janela.after(
        200,
        lambda: processar_chat(texto)
    )


# ==========================================================
# 🖥️ JANELA PRINCIPAL
# ==========================================================

janela = tk.Tk()

janela.title(
    "🍦 Sorveteria Glacê 🎀"
)

janela.geometry(
    "600x480"
)

janela.minsize(
    560,
    440
)

janela.configure(
    bg=CORES["fundo"]
)


# ==========================================================
# 🎨 ESTILO
# ==========================================================

style = ttk.Style()

style.theme_use(
    "clam"
)

style.configure(
    "TNotebook",
    background=CORES["fundo"],
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background="#E4EEF6",
    foreground=CORES["escuro"],
    padding=(10, 6),
    font=("Segoe UI", 8, "bold")
)

style.map(
    "TNotebook.Tab",
    background=[
        ("selected", CORES["azul_medio"])
    ],
    foreground=[
        ("selected", "white")
    ]
)

style.configure(
    "TCombobox",
    fieldbackground="white",
    background="white",
    foreground=CORES["texto"],
    padding=4
)

style.configure(
    "Treeview",
    background="white",
    foreground=CORES["texto"],
    fieldbackground="white",
    rowheight=27,
    font=("Segoe UI", 8)
)

style.configure(
    "Treeview.Heading",
    background=CORES["azul_claro"],
    foreground=CORES["escuro"],
    font=("Segoe UI", 8, "bold"),
    padding=5
)


# ==========================================================
# 🍦 CABEÇALHO
# ==========================================================

header = tk.Frame(
    janela,
    bg=CORES["fundo"]
)

header.pack(
    fill="x",
    padx=15,
    pady=(8, 3)
)

tk.Label(
    header,
    text="🍦",
    bg=CORES["fundo"],
    font=("Segoe UI Emoji", 21)
).pack(
    side="left",
    padx=(0, 6)
)

titulo_frame = tk.Frame(
    header,
    bg=CORES["fundo"]
)

titulo_frame.pack(
    side="left"
)

tk.Label(
    titulo_frame,
    text="Sorveteria Glacê 🎀",
    bg=CORES["fundo"],
    fg=CORES["escuro"],
    font=("Segoe UI", 15, "bold")
).pack(
    anchor="w"
)

tk.Label(
    titulo_frame,
    text="Gestão da sorveteria 🎀",
    bg=CORES["fundo"],
    fg=CORES["cinza"],
    font=("Segoe UI", 7)
).pack(
    anchor="w"
)


# ==========================================================
# 📊 CARDS
# ==========================================================

dashboard = tk.Frame(
    janela,
    bg=CORES["fundo"]
)

dashboard.pack(
    fill="x",
    padx=12,
    pady=3
)


def criar_card(
    parent,
    icone,
    titulo,
    valor
):

    card = tk.Frame(
        parent,
        bg=CORES["branco"],
        highlightbackground=CORES["borda"],
        highlightthickness=1
    )

    card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=2
    )

    tk.Label(
        card,
        text=icone,
        bg=CORES["azul_claro"],
        font=("Segoe UI Emoji", 10),
        width=2
    ).pack(
        side="left",
        padx=4,
        pady=4
    )

    info = tk.Frame(
        card,
        bg=CORES["branco"]
    )

    info.pack(
        side="left"
    )

    tk.Label(
        info,
        text=titulo,
        bg=CORES["branco"],
        fg=CORES["cinza"],
        font=("Segoe UI", 6, "bold")
    ).pack(
        anchor="w"
    )

    label = tk.Label(
        info,
        text=valor,
        bg=CORES["branco"],
        fg=CORES["escuro"],
        font=("Segoe UI", 9, "bold")
    )

    label.pack(
        anchor="w"
    )

    return label


lbl_caixa = criar_card(
    dashboard,
    "💰",
    "CAIXA",
    "R$ 500,00"
)

lbl_vendas = criar_card(
    dashboard,
    "🛒",
    "VENDAS",
    "0"
)

lbl_itens = criar_card(
    dashboard,
    "🍨",
    "ITENS",
    "0"
)

lbl_baixo = criar_card(
    dashboard,
    "⚠️",
    "ESTOQUE",
    "0"
)


# ==========================================================
# 📑 ABAS
# ==========================================================

notebook = ttk.Notebook(
    janela
)

notebook.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


aba_vendas = tk.Frame(
    notebook,
    bg=CORES["branco"]
)

aba_estoque = tk.Frame(
    notebook,
    bg=CORES["branco"]
)

aba_extrato = tk.Frame(
    notebook,
    bg=CORES["branco"]
)

aba_chat = tk.Frame(
    notebook,
    bg=CORES["branco"]
)


notebook.add(
    aba_vendas,
    text=" 💰 Vendas "
)

notebook.add(
    aba_estoque,
    text=" 📦 Estoque "
)

notebook.add(
    aba_extrato,
    text=" 📋 Extrato "
)

notebook.add(
    aba_chat,
    text=" 💬 Chat "
)


# ==========================================================
# 💰 VENDAS
# ==========================================================

tk.Label(
    aba_vendas,
    text="🛒 Nova Venda",
    bg=CORES["branco"],
    fg=CORES["escuro"],
    font=("Segoe UI", 12, "bold")
).pack(
    anchor="w",
    padx=18,
    pady=(12, 5)
)


form = tk.Frame(
    aba_vendas,
    bg=CORES["azul_claro"],
    highlightbackground=CORES["borda"],
    highlightthickness=1
)

form.pack(
    fill="x",
    padx=18,
    pady=5
)


def criar_label(
    texto,
    linha
):

    tk.Label(
        form,
        text=texto,
        bg=CORES["azul_claro"],
        fg=CORES["escuro"],
        font=("Segoe UI", 8, "bold")
    ).grid(
        row=linha,
        column=0,
        sticky="w",
        padx=12,
        pady=6
    )


criar_label(
    "🍨 Sabor:",
    0
)

combo_sabor = ttk.Combobox(
    form,
    values=list(sabores.keys()),
    state="readonly",
    width=25
)

combo_sabor.grid(
    row=0,
    column=1,
    padx=5,
    pady=6
)


criar_label(
    "🔢 Quantidade:",
    1
)

ent_qtd = tk.Entry(
    form,
    width=28,
    relief="solid",
    bd=1
)

ent_qtd.grid(
    row=1,
    column=1,
    padx=5,
    pady=6,
    ipady=3
)


criar_label(
    "💳 Pagamento:",
    2
)

combo_pagamento = ttk.Combobox(
    form,
    values=[
        "Pix",
        "Cartão de Crédito",
        "Cartão de Débito",
        "Dinheiro"
    ],
    state="readonly",
    width=25
)

combo_pagamento.grid(
    row=2,
    column=1,
    padx=5,
    pady=6
)

combo_pagamento.bind(
    "<<ComboboxSelected>>",
    mudar_pagamento
)


lbl_pago = tk.Label(
    form,
    text="💵 Valor entregue:",
    bg=CORES["azul_claro"],
    fg=CORES["escuro"],
    font=("Segoe UI", 8, "bold")
)

lbl_pago.grid(
    row=3,
    column=0,
    padx=12,
    pady=6
)

ent_pago = tk.Entry(
    form,
    width=28,
    relief="solid",
    bd=1
)

ent_pago.grid(
    row=3,
    column=1,
    padx=5,
    pady=6,
    ipady=3
)

lbl_pago.grid_remove()
ent_pago.grid_remove()


criar_botao(
    form,
    "✓ CONFIRMAR VENDA",
    vender,
    CORES["verde"]
).grid(
    row=4,
    column=0,
    columnspan=2,
    pady=8
)


# ==========================================================
# 📦 ESTOQUE
# ==========================================================

tk.Label(
    aba_estoque,
    text="📦 Estoque",
    bg=CORES["branco"],
    fg=CORES["escuro"],
    font=("Segoe UI", 12, "bold")
).pack(
    anchor="w",
    padx=15,
    pady=(10, 3)
)


tree_estoque = ttk.Treeview(
    aba_estoque,
    columns=(
        "sabor",
        "qtd",
        "preco",
        "status"
    ),
    show="headings"
)

tree_estoque.heading(
    "sabor",
    text="🍨 Sabor"
)

tree_estoque.heading(
    "qtd",
    text="Qtd."
)

tree_estoque.heading(
    "preco",
    text="Preço"
)

tree_estoque.heading(
    "status",
    text="Status"
)

tree_estoque.column(
    "sabor",
    width=180
)

tree_estoque.column(
    "qtd",
    width=70,
    anchor="center"
)

tree_estoque.column(
    "preco",
    width=90,
    anchor="center"
)

tree_estoque.column(
    "status",
    width=110,
    anchor="center"
)

tree_estoque.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


frame_repor = tk.Frame(
    aba_estoque,
    bg=CORES["azul_claro"]
)

frame_repor.pack(
    fill="x",
    padx=15,
    pady=7,
    ipady=4
)

tk.Label(
    frame_repor,
    text="Repor:",
    bg=CORES["azul_claro"],
    fg=CORES["escuro"],
    font=("Segoe UI", 8, "bold")
).pack(
    side="left",
    padx=6
)

combo_estoque = ttk.Combobox(
    frame_repor,
    values=list(sabores.keys()),
    state="readonly",
    width=14
)

combo_estoque.pack(
    side="left",
    padx=3
)

ent_estoque = tk.Entry(
    frame_repor,
    width=6
)

ent_estoque.pack(
    side="left",
    padx=3
)

criar_botao(
    frame_repor,
    "+ Adicionar",
    repor_estoque,
    CORES["azul_medio"]
).pack(
    side="left",
    padx=3
)


# ==========================================================
# 📋 EXTRATO
# ==========================================================

tk.Label(
    aba_extrato,
    text="📋 Extrato",
    bg=CORES["branco"],
    fg=CORES["escuro"],
    font=("Segoe UI", 12, "bold")
).pack(
    anchor="w",
    padx=15,
    pady=(10, 3)
)


tree_extrato = ttk.Treeview(
    aba_extrato,
    columns=(
        "op",
        "detalhes",
        "valor"
    ),
    show="headings"
)

tree_extrato.heading(
    "op",
    text="Operação"
)

tree_extrato.heading(
    "detalhes",
    text="Detalhes"
)

tree_extrato.heading(
    "valor",
    text="Valor"
)

tree_extrato.column(
    "op",
    width=130
)

tree_extrato.column(
    "detalhes",
    width=290
)

tree_extrato.column(
    "valor",
    width=100,
    anchor="e"
)

tree_extrato.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


# ==========================================================
# 💬 CHATBOX
# ==========================================================

tk.Label(
    aba_chat,
    text="💬 Atendimento",
    bg=CORES["branco"],
    fg=CORES["escuro"],
    font=("Segoe UI", 12, "bold")
).pack(
    anchor="w",
    padx=12,
    pady=(7, 0)
)


tk.Label(
    aba_chat,
    text="Converse com a Sorveteria Glacê 🎀",
    bg=CORES["branco"],
    fg=CORES["cinza"],
    font=("Segoe UI", 7)
).pack(
    anchor="w",
    padx=12
)


# ==========================================================
# 🟦 CHATBOX PRINCIPAL
# ==========================================================

chat_frame = tk.Frame(
    aba_chat,
    bg="#EAF7FF",
    highlightbackground=CORES["borda"],
    highlightthickness=1
)

chat_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=6
)


# ==========================================================
# 💬 ÁREA DAS MENSAGENS
# ==========================================================

chat = tk.Text(
    chat_frame,
    bg="#F9FCFF",
    fg=CORES["texto"],
    font=("Segoe UI", 8),
    wrap="word",
    bd=0,
    padx=10,
    pady=8,
    state="disabled"
)

chat.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


chat.tag_configure(
    "nome",
    foreground=CORES["azul_medio"],
    font=("Segoe UI", 8, "bold")
)

chat.tag_configure(
    "mensagem",
    foreground=CORES["texto"],
    font=("Segoe UI", 8)
)


# ==========================================================
# 🔘 BOTÕES INICIAIS
# ==========================================================

botoes_opcoes = tk.Frame(
    chat_frame,
    bg="#EAF7FF"
)


criar_botao(
    botoes_opcoes,
    "🍦 Fazer pedido",
    lambda: opcao_a(),
    CORES["azul_medio"]
).pack(
    side="left",
    expand=True,
    fill="x",
    padx=3
)


criar_botao(
    botoes_opcoes,
    "⚠️ Suporte",
    lambda: opcao_b(),
    CORES["vermelho"]
).pack(
    side="left",
    expand=True,
    fill="x",
    padx=3
)


# ==========================================================
# 💳 BOTÕES DE PAGAMENTO
# ==========================================================

botoes_pagamento = tk.Frame(
    chat_frame,
    bg="#EAF7FF"
)


for texto, forma in [
    ("📱 Pix", "Pix"),
    ("💳 Crédito", "Cartão de Crédito"),
    ("💳 Débito", "Cartão de Débito"),
    ("💵 Dinheiro", "Dinheiro")
]:

    criar_botao(
        botoes_pagamento,
        texto,
        lambda f=forma: pagamento_chat(f),
        CORES["escuro"]
    ).pack(
        side="left",
        expand=True,
        fill="x",
        padx=2
    )


# ==========================================================
# ✏️ CAMPO PARA DIGITAR
# ==========================================================

entrada_frame = tk.Frame(
    chat_frame,
    bg="#EAF7FF"
)

entrada_frame.pack(
    fill="x",
    padx=5,
    pady=5
)


entrada_chat = tk.Entry(
    entrada_frame,
    bg="white",
    fg=CORES["texto"],
    font=("Segoe UI", 8),
    relief="solid",
    bd=1
)

entrada_chat.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5),
    ipady=6
)


criar_botao(
    entrada_frame,
    "Enviar ➤",
    enviar,
    CORES["azul_medio"]
).pack(
    side="right"
)


# ==========================================================
# ⌨️ ENTER ENVIA A MENSAGEM
# ==========================================================

entrada_chat.bind(
    "<Return>",
    lambda evento: enviar()
)


# ==========================================================
# 🔵 FUNÇÕES DOS BOTÕES
# ==========================================================

def opcao_a():

    botoes_opcoes.pack_forget()

    chat_msg(
        "👤 Você",
        "Quero fazer um pedido."
    )

    chat_msg(
        "🍦 Sorveteria Glacê 🎀",
        "Claro! 🎀\n\n"
        "Digite o sabor e a quantidade.\n\n"
        "Exemplo:\n"
        "👉 Quero 2 Chocolate\n\n"
        "Você também pode digitar 'cardápio' para ver todos os sabores."
    )


def opcao_b():

    botoes_opcoes.pack_forget()

    chat_msg(
        "👤 Você",
        "Preciso de suporte."
    )

    chat_msg(
        "🍦 Sorveteria Glacê 🎀",
        "Claro! 😊\n\n"
        "Digite sua dúvida ou problema."
    )


# ==========================================================
# 🚀 MENSAGEM INICIAL
# ==========================================================

chat_msg(
    "🍦 Sorveteria Glacê 🎀",
    "Olá! Seja bem-vindo(a)! 🎀\n\n"
    "Eu sou o atendimento automático da Glacê.\n"
    "Como posso ajudar?"
)

mostrar_botoes_iniciais()

atualizar()


# ==========================================================
# ▶️ EXECUTAR
# ==========================================================

janela.mainloop()