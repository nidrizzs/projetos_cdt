"""
🍦 SORVETERIA DA LIS
Sistema com interface moderna em Tkinter + Atendimento Guiado no Chat + Formas de Pagamento
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re

# ==================================================
# PALETA DE CORES MODERNA
# ==================================================

COR_AZUL_ESCURO = "#0A2540"      # Azul corporativo profundo
COR_AZUL_MEDIO  = "#1F618D"      # Destaque de botões e seleção
COR_AZUL_BEBE   = "#E8F4FC"      # Fundo suave para cards e balões
COR_AZUL_BOTAO  = "#3498DB"      # Botões de ação primária
COR_BRANCO      = "#FFFFFF"      # Fundo limpo
COR_CINZA_TEXTO = "#4A5568"      # Texto de apoio legível
COR_CINZA_LINHA = "#E2E8F0"      # Bordas suaves

# ==================================================
# DADOS DA LOJA
# ==================================================

caixa = 500.00
forma_pagamento_chat_pendente = None

sabores = {
    "Chocolate": {"preco": 8.00, "estoque": 140},
    "Morango": {"preco": 8.00, "estoque": 140},
    "Baunilha": {"preco": 8.00, "estoque": 140},
    "Coco": {"preco": 9.00, "estoque": 140},
    "Limão": {"preco": 8.50, "estoque": 140},
    "Blue Ice": {"preco": 10.00, "estoque": 140},
    "Flocos": {"preco": 9.00, "estoque": 140},
    "Brigadeiro": {"preco": 10.00, "estoque": 140},
    "Beijinho": {"preco": 10.00, "estoque": 140},
    "Nutella": {"preco": 12.00, "estoque": 140},
    "Oreo": {"preco": 11.00, "estoque": 140},
    "Açaí": {"preco": 11.00, "estoque": 140},
    "Leite Ninho": {"preco": 11.00, "estoque":140},
    "Paçoca": {"preco": 10.00, "estoque": 140},
    "Pistache": {"preco": 13.00, "estoque":140 },
}

historico = [
    ("Abertura de Caixa", "Sistema iniciado com valor inicial", "R$ 500,00")
]

# ==================================================
# FUNÇÕES DE FORMATAR E ATUALIZAR INTERFACE
# ==================================================

def formatar_dinheiro(valor):
    return f"R$ {valor:.2f}".replace(".", ",")

def atualizar_interface():
    # Atualiza o valor do caixa
    lbl_caixa.config(text=formatar_dinheiro(caixa))

    # Atualiza o extrato (Treeview)
    for item in tree_extrato.get_children():
        tree_extrato.delete(item)
        
    for operacao, desc, valor in reversed(historico):
        tree_extrato.insert("", tk.END, values=(operacao, desc, valor))

    # Atualiza o estoque (Treeview)
    for item in tree_estoque.get_children():
        tree_estoque.delete(item)

    for sabor, dados in sabores.items():
        status = "🟢 OK" if dados['estoque'] > 5 else ("🟡 Baixo" if dados['estoque'] > 0 else "🔴 Esgotado")
        tree_estoque.insert("", tk.END, values=(sabor, dados['estoque'], formatar_dinheiro(dados['preco']), status))

# ==================================================
# REGRAS DE NEGÓCIO DA LOJA
# ==================================================

def ao_mudar_pagamento(event=None):
    if combo_pagamento.get() == "Dinheiro":
        lbl_valor_pago.grid(row=3, column=0, sticky="w", pady=10)
        ent_valor_pago.grid(row=3, column=1, padx=10, pady=10)
    else:
        lbl_valor_pago.grid_remove()
        ent_valor_pago.grid_remove()

def vender_sorvete():
    global caixa
    sabor = combo_sabores.get()
    forma_pagto = combo_pagamento.get()

    if not sabor:
        messagebox.showwarning("Aviso", "Por favor, selecione um sabor.")
        return

    if not forma_pagto:
        messagebox.showwarning("Aviso", "Por favor, selecione a forma de pagamento.")
        return

    try:
        qtd = int(ent_quantidade.get())
        if qtd <= 0:
            messagebox.showwarning("Aviso", "Informe uma quantidade válida superior a 0.")
            return

        if qtd > sabores[sabor]["estoque"]:
            messagebox.showwarning("Estoque Insuficiente", f"Temos apenas {sabores[sabor]['estoque']} unidades de {sabor} disponível(is).")
            return

        valor_total = sabores[sabor]["preco"] * qtd
        mensagem_sucesso = f"Venda de {qtd}x {sabor} registrada!\nTotal: {formatar_dinheiro(valor_total)}\nPagamento: {forma_pagto}"

        # Trata o troco se for Dinheiro
        if forma_pagto == "Dinheiro":
            try:
                valor_pago = float(ent_valor_pago.get().replace(",", "."))
                if valor_pago < valor_total:
                    messagebox.showwarning("Valor Insuficiente", f"O valor pago ({formatar_dinheiro(valor_pago)}) é inferior ao total ({formatar_dinheiro(valor_total)}).")
                    return
                troco = valor_pago - valor_total
                mensagem_sucesso += f"\nValor Pago: {formatar_dinheiro(valor_pago)}\nTroco: {formatar_dinheiro(troco)}"
            except ValueError:
                messagebox.showerror("Erro", "Digite um valor pago válido.")
                return

        sabores[sabor]["estoque"] -= qtd
        caixa += valor_total

        historico.append(("Venda Balcão", f"{qtd}x {sabor} ({forma_pagto})", formatar_dinheiro(valor_total)))
        atualizar_interface()

        ent_quantidade.delete(0, tk.END)
        ent_valor_pago.delete(0, tk.END)
        messagebox.showinfo("Venda Concluída", mensagem_sucesso)

    except ValueError:
        messagebox.showerror("Erro", "Digite um número inteiro válido na quantidade.")

def adicionar_estoque():
    sabor = combo_estoque.get()

    if not sabor:
        messagebox.showwarning("Aviso", "Selecione um sabor para repor.")
        return

    try:
        qtd = int(ent_estoque.get())
        if qtd <= 0:
            messagebox.showwarning("Aviso", "Digite um valor de reposição válido.")
            return

        sabores[sabor]["estoque"] += qtd
        historico.append(("Reposição Estoque", f"+{qtd} un. {sabor}", "-"))
        atualizar_interface()

        ent_estoque.delete(0, tk.END)
        messagebox.showinfo("Sucesso", f"Estoque de {sabor} atualizado com sucesso!")

    except ValueError:
        messagebox.showerror("Erro", "Digite um número inteiro válido para o estoque.")

# ==================================================
# CHATBOX E ATENDIMENTO GUIADO
# ==================================================

def adicionar_chat(remetente, mensagem):
    chat.config(state="normal")
    chat.insert(tk.END, f"{remetente}\n", "remetente")
    chat.insert(tk.END, f"{mensagem}\n\n", "texto")
    chat.see(tk.END)
    chat.config(state="disabled")

def mostrar_menu_opcoes():
    msg = (
        "Como podemos te ajudar hoje? Digite a opção ou clique nos botões abaixo:\n\n"
        "👉 [A] Fazer um Pedido / Ver Sabores 🍦\n"
        "👉 [B] Suporte, Reclamações ou Ajuda ⚠️"
    )
    adicionar_chat("🍦 Atendimento Lis", msg)
    frame_botoes_opcoes.pack(fill="x", padx=15, pady=(0, 10))

def selecionar_opcao_a():
    frame_botoes_opcoes.pack_forget()
    adicionar_chat("👤 Cliente", "Opção A: Fazer um Pedido / Ver Sabores")
    
    lista_sabores = "\n".join([f"• {sabor}: {formatar_dinheiro(dados['preco'])}" for sabor, dados in sabores.items()])
    resposta = (
        "Excelente escolha! 😋 Aqui está nosso cardápio atualizado:\n\n"
        f"{lista_sabores}\n\n"
        "💡 Como pedir: Digite o sabor e a quantidade que deseja.\n"
        "Exemplo: 'Quero 2 sorvetes de Nutella'"
    )
    adicionar_chat("🍦 Atendimento Lis", resposta)

def selecionar_opcao_b():
    frame_botoes_opcoes.pack_forget()
    adicionar_chat("👤 Cliente", "Opção B: Suporte / Reclamações / Ajuda")
    resposta = (
        "Estamos aqui para resolver qualquer imprevisto! 💙\n\n"
        "Por favor, descreva em detalhes o seu problema ou sua reclamação. "
        "Nossa equipe registrará sua mensagem para atendimento prioritário."
    )
    adicionar_chat("🍦 Atendimento Lis", resposta)

def solicitar_pagamento_chat(sabor, qtd):
    global forma_pagamento_chat_pendente
    forma_pagamento_chat_pendente = {"sabor": sabor, "qtd": qtd}
    
    msg = (
        f"Ótimo! Seu pedido é: {qtd}x {sabor}.\n"
        f"Qual será a forma de pagamento?\n\n"
        "💳 Escolha uma das opções abaixo:\n"
        "• Pix\n• Cartão de Crédito\n• Cartão de Débito\n• Dinheiro"
    )
    adicionar_chat("🍦 Atendimento Lis", msg)
    frame_botoes_pagto.pack(fill="x", padx=15, pady=(0, 10))

def selecionar_pagamento_chat(forma):
    global caixa, forma_pagamento_chat_pendente
    frame_botoes_pagto.pack_forget()

    if not forma_pagamento_chat_pendente:
        return

    sabor = forma_pagamento_chat_pendente["sabor"]
    qtd = forma_pagamento_chat_pendente["qtd"]
    valor_total = sabores[sabor]["preco"] * qtd

    sabores[sabor]["estoque"] -= qtd
    caixa += valor_total

    historico.append(("Venda Chatbot", f"{qtd}x {sabor} ({forma})", formatar_dinheiro(valor_total)))
    atualizar_interface()

    adicionar_chat("👤 Cliente", f"Forma de pagamento: {forma}")
    adicionar_chat(
        "🍦 Atendimento Lis",
        f"Pedido Confirmado! 🎉\n\n"
        f"🛒 Produto: {qtd}x {sabor}\n"
        f"💳 Pagamento: {forma}\n"
        f"💰 Total: {formatar_dinheiro(valor_total)}\n\n"
        f"Seu pedido foi registrado no sistema! Muito obrigado! 🍦💙"
    )

    forma_pagamento_chat_pendente = None

def processar_mensagem_chat(mensagem):
    global forma_pagamento_chat_pendente
    mensagem_lower = mensagem.lower().strip()

    # Se estiver aguardando forma de pagamento
    if forma_pagamento_chat_pendente:
        if "pix" in mensagem_lower:
            selecionar_pagamento_chat("Pix")
            return
        elif "crédito" in mensagem_lower or "credito" in mensagem_lower:
            selecionar_pagamento_chat("Cartão de Crédito")
            return
        elif "débito" in mensagem_lower or "debito" in mensagem_lower:
            selecionar_pagamento_chat("Cartão de Débito")
            return
        elif "dinheiro" in mensagem_lower:
            selecionar_pagamento_chat("Dinheiro")
            return

    # Atalhos A ou B por texto
    if mensagem_lower in ["a", "opcao a", "opção a"]:
        selecionar_opcao_a()
        return
    if mensagem_lower in ["b", "opcao b", "opção b"]:
        selecionar_opcao_b()
        return

    # Busca sabor e quantidade
    sabor_encontrado = None
    for s in sabores:
        if s.lower() in mensagem_lower:
            sabor_encontrado = s
            break

    numeros = re.findall(r"\d+", mensagem)
    qtd = int(numeros[0]) if numeros else 1

    # Intenções de Pedido
    palavras_pedido = ["quero", "pedido", "comprar", "gostaria", "me ve", "me vê", "trazer", "pedir"]
    if any(p in mensagem_lower for p in palavras_pedido) or sabor_encontrado:
        if sabor_encontrado:
            if qtd > sabores[sabor_encontrado]["estoque"]:
                adicionar_chat(
                    "🍦 Atendimento Lis",
                    f"Poxa, no momento não temos {qtd}x {sabor_encontrado} em estoque. "
                    f"Temos apenas {sabores[sabor_encontrado]['estoque']} unidades disponíveis."
                )
            else:
                solicitar_pagamento_chat(sabor_encontrado, qtd)
        else:
            adicionar_chat("🍦 Atendimento Lis", "Não consegui identificar o sabor na sua mensagem. Por favor escolha um sabor válido do nosso menu!")
        return

    # Reclamações e Suporte
    palavras_reclamacao = ["reclamacao", "reclamação", "reclamar", "errado", "problema", "atrasado", "ruim", "pessimo", "péssimo"]
    if any(p in mensagem_lower for p in palavras_reclamacao):
        historico.append(("Reclamação Chat", mensagem[:30] + "...", "-"))
        atualizar_interface()
        adicionar_chat(
            "🍦 Atendimento Lis",
            "Lamentamos muito por essa experiência! 😔\n"
            "Registramos sua mensagem com prioridade. Nossa gerência analisará o ocorrido para te dar o suporte necessário."
        )
        return

    # Saudações gerais
    if any(c in mensagem_lower for c in ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]):
        mostrar_menu_opcoes()
        return

    # Resposta padrão
    adicionar_chat(
        "🍦 Atendimento Lis",
        "Desculpe, não entendi bem. Por favor escolha uma das opções:\n"
        "Digite 'A' para ver o cardápio e fazer pedidos, ou 'B' para suporte e reclamações."
    )

def enviar_mensagem():
    mensagem = entrada_chat.get().strip()
    if not mensagem:
        return

    adicionar_chat("👤 Cliente", mensagem)
    entrada_chat.delete(0, tk.END)
    janela.after(400, lambda: processar_mensagem_chat(mensagem))

# ==================================================
# CONSTRUÇÃO DA JANELA PRINCIPAL (UI MODERNA)
# ==================================================

janela = tk.Tk()
janela.title("Sorveteria da Lis - Sistema de Gestão e Atendimento")
janela.geometry("900x720")
janela.configure(bg=COR_AZUL_ESCURO)

# Estilização TTK Global
style = ttk.Style()
style.theme_use("clam")

# Estilo das Abas (Notebook)
style.configure("TNotebook", background=COR_AZUL_ESCURO, borderwidth=0)
style.configure("TNotebook.Tab", background="#1B3A57", foreground="white", padding=[20, 10], font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab", background=[("selected", COR_BRANCO)], foreground=[("selected", COR_AZUL_ESCURO)])

# Estilo das Tabelas (Treeview)
style.configure("Treeview", background=COR_BRANCO, foreground="#2D3748", rowheight=30, fieldbackground=COR_BRANCO, font=("Segoe UI", 10))
style.configure("Treeview.Heading", background=COR_AZUL_BEBE, foreground=COR_AZUL_ESCURO, font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[("selected", COR_AZUL_BEBE)], foreground=[("selected", COR_AZUL_ESCURO)])

# Cabeçalho Principal
header_frame = tk.Frame(janela, bg=COR_AZUL_ESCURO)
header_frame.pack(fill="x", padx=20, pady=15)

titulo = tk.Label(
    header_frame,
    text="🍦 SORVETERIA DA LIS",
    bg=COR_AZUL_ESCURO,
    fg=COR_BRANCO,
    font=("Segoe UI", 20, "bold")
)
titulo.pack(side="left")

subtitulo = tk.Label(
    header_frame,
    text="Painel Integrado de Vendas & Atendimento",
    bg=COR_AZUL_ESCURO,
    fg="#A0AEC0",
    font=("Segoe UI", 10)
)
subtitulo.pack(side="right", pady=5)

# Notebook / Abas
notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

# Criando Containers das Abas
aba_vendas = tk.Frame(notebook, bg=COR_BRANCO)
aba_estoque = tk.Frame(notebook, bg=COR_BRANCO)
aba_extrato = tk.Frame(notebook, bg=COR_BRANCO)
aba_chat = tk.Frame(notebook, bg=COR_BRANCO)

notebook.add(aba_vendas, text="  💰 Vendas Balcão  ")
notebook.add(aba_estoque, text="  📦 Controle de Estoque  ")
notebook.add(aba_extrato, text="  📋 Extrato de Operações  ")
notebook.add(aba_chat, text="  💬 Chat Atendimento  ")

# ==================================================
# ABA 1: VENDAS BALCÃO
# ==================================================

# Card Dashboard do Caixa
card_caixa = tk.Frame(aba_vendas, bg=COR_AZUL_BEBE, bd=1, relief="solid")
card_caixa.pack(fill="x", padx=40, pady=20)

lbl_caixa_title = tk.Label(card_caixa, text="SALDO ATUAL EM CAIXA", bg=COR_AZUL_BEBE, fg=COR_CINZA_TEXTO, font=("Segoe UI", 9, "bold"))
lbl_caixa_title.pack(pady=(12, 0))

lbl_caixa = tk.Label(card_caixa, text="R$ 0,00", bg=COR_AZUL_BEBE, fg=COR_AZUL_ESCURO, font=("Segoe UI", 24, "bold"))
lbl_caixa.pack(pady=(0, 12))

# Card do Formulario de Venda
card_form = tk.LabelFrame(aba_vendas, text=" Registrar Nova Venda ", bg=COR_BRANCO, fg=COR_AZUL_ESCURO, font=("Segoe UI", 11, "bold"), padx=20, pady=15)
card_form.pack(fill="both", expand=True, padx=40, pady=(0, 20))

tk.Label(card_form, text="Sabor do Sorvete:", bg=COR_BRANCO, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=8)
combo_sabores = ttk.Combobox(card_form, values=list(sabores.keys()), width=35, state="readonly", font=("Segoe UI", 10))
combo_sabores.grid(row=0, column=1, padx=10, pady=8)

tk.Label(card_form, text="Quantidade (un):", bg=COR_BRANCO, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=8)
ent_quantidade = tk.Entry(card_form, font=("Segoe UI", 10), width=37, bd=1, relief="solid")
ent_quantidade.grid(row=1, column=1, padx=10, pady=8)

tk.Label(card_form, text="Forma de Pagamento:", bg=COR_BRANCO, font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=8)
combo_pagamento = ttk.Combobox(card_form, values=["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"], width=35, state="readonly", font=("Segoe UI", 10))
combo_pagamento.grid(row=2, column=1, padx=10, pady=8)
combo_pagamento.bind("<<ComboboxSelected>>", ao_mudar_pagamento)

lbl_valor_pago = tk.Label(card_form, text="Valor Entregue (Troco):", bg=COR_BRANCO, font=("Segoe UI", 10))
ent_valor_pago = tk.Entry(card_form, font=("Segoe UI", 10), width=37, bd=1, relief="solid")

btn_vender = tk.Button(
    card_form,
    text="Confirmar Venda 🛒",
    bg=COR_AZUL_BOTAO,
    fg="white",
    font=("Segoe UI", 11, "bold"),
    bd=0,
    padx=20,
    pady=8,
    cursor="hand2",
    command=vender_sorvete
)
btn_vender.grid(row=4, column=0, columnspan=2, pady=15)

# ==================================================
# ABA 2: CONTROLE DE ESTOQUE
# ==================================================

frame_tabela_est = tk.Frame(aba_estoque, bg=COR_BRANCO)
frame_tabela_est.pack(fill="both", expand=True, padx=20, pady=15)

colunas_est = ("sabor", "estoque", "preco", "status")
tree_estoque = ttk.Treeview(frame_tabela_est, columns=colunas_est, show="headings", height=8)

tree_estoque.heading("sabor", text="Sabor")
tree_estoque.heading("estoque", text="Qtd. Estoque")
tree_estoque.heading("preco", text="Preço Unitário")
tree_estoque.heading("status", text="Status")

tree_estoque.column("sabor", width=200)
tree_estoque.column("estoque", width=120, anchor="center")
tree_estoque.column("preco", width=150, anchor="center")
tree_estoque.column("status", width=120, anchor="center")

tree_estoque.pack(fill="both", expand=True, side="left")

scroll_est = ttk.Scrollbar(frame_tabela_est, orient="vertical", command=tree_estoque.yview)
tree_estoque.configure(yscrollcommand=scroll_est.set)
scroll_est.pack(side="right", fill="y")

# Form Reposição
card_reposicao = tk.Frame(aba_estoque, bg=COR_AZUL_BEBE, padx=15, pady=15)
card_reposicao.pack(fill="x", padx=20, pady=(0, 15))

tk.Label(card_reposicao, text="Repor Estoque:", bg=COR_AZUL_BEBE, font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
combo_estoque = ttk.Combobox(card_reposicao, values=list(sabores.keys()), state="readonly", width=20)
combo_estoque.pack(side="left", padx=5)

tk.Label(card_reposicao, text="Qtd:", bg=COR_AZUL_BEBE, font=("Segoe UI", 10)).pack(side="left", padx=5)
ent_estoque = tk.Entry(card_reposicao, width=10)
ent_estoque.pack(side="left", padx=5)

btn_estoque = tk.Button(
    card_reposicao,
    text="+ Adicionar",
    bg=COR_AZUL_MEDIO,
    fg="white",
    font=("Segoe UI", 9, "bold"),
    bd=0,
    padx=15,
    command=adicionar_estoque
)
btn_estoque.pack(side="left", padx=10)

# ==================================================
# ABA 3: EXTRATO DE OPERAÇÕES
# ==================================================

frame_tabela_ext = tk.Frame(aba_extrato, bg=COR_BRANCO)
frame_tabela_ext.pack(fill="both", expand=True, padx=20, pady=20)

colunas_ext = ("operacao", "detalhes", "valor")
tree_extrato = ttk.Treeview(frame_tabela_ext, columns=colunas_ext, show="headings")

tree_extrato.heading("operacao", text="Operação")
tree_extrato.heading("detalhes", text="Detalhes")
tree_extrato.heading("valor", text="Valor")

tree_extrato.column("operacao", width=180)
tree_extrato.column("detalhes", width=400)
tree_extrato.column("valor", width=150, anchor="e")

tree_extrato.pack(fill="both", expand=True, side="left")

scroll_ext = ttk.Scrollbar(frame_tabela_ext, orient="vertical", command=tree_extrato.yview)
tree_extrato.configure(yscrollcommand=scroll_ext.set)
scroll_ext.pack(side="right", fill="y")

# ==================================================
# ABA 4: CHATBOX DE ATENDIMENTO
# ==================================================

# Tela de Mensagens
chat_frame = tk.Frame(aba_chat, bg=COR_BRANCO)
chat_frame.pack(fill="both", expand=True, padx=15, pady=(15, 5))

chat = tk.Text(chat_frame, bg="#F7FAFC", fg="#2D3748", font=("Segoe UI", 10), wrap="word", bd=1, relief="solid", padx=10, pady=10)
chat.tag_configure("remetente", font=("Segoe UI", 9, "bold"), foreground=COR_AZUL_MEDIO)
chat.tag_configure("texto", font=("Segoe UI", 10), foreground="#2D3748")
chat.pack(fill="both", expand=True, side="left")

scroll_chat = ttk.Scrollbar(chat_frame, command=chat.yview)
chat.configure(yscrollcommand=scroll_chat.set)
scroll_chat.pack(side="right", fill="y")

# Botões de Escolha Rápida (Opção A e B)
frame_botoes_opcoes = tk.Frame(aba_chat, bg=COR_BRANCO)

btn_opcao_a = tk.Button(
    frame_botoes_opcoes,
    text="[A] Fazer Pedido / Ver Sabores 🍦",
    bg=COR_AZUL_BEBE,
    fg=COR_AZUL_ESCURO,
    font=("Segoe UI", 9, "bold"),
    bd=1,
    relief="solid",
    padx=10,
    pady=5,
    cursor="hand2",
    command=selecionar_opcao_a
)
btn_opcao_a.pack(side="left", expand=True, fill="x", padx=(0, 5))

btn_opcao_b = tk.Button(
    frame_botoes_opcoes,
    text="[B] Suporte / Reclamações ⚠️",
    bg="#FFF5F5",
    fg="#C53030",
    font=("Segoe UI", 9, "bold"),
    bd=1,
    relief="solid",
    padx=10,
    pady=5,
    cursor="hand2",
    command=selecionar_opcao_b
)
btn_opcao_b.pack(side="right", expand=True, fill="x", padx=(5, 0))

# Botões Rápidos de Pagamento no Chat
frame_botoes_pagto = tk.Frame(aba_chat, bg=COR_BRANCO)

btn_pix = tk.Button(frame_botoes_pagto, text="Pix 📱", bg=COR_AZUL_BEBE, font=("Segoe UI", 8, "bold"), command=lambda: selecionar_pagamento_chat("Pix"))
btn_pix.pack(side="left", expand=True, fill="x", padx=2)

btn_credito = tk.Button(frame_botoes_pagto, text="Crédito 💳", bg=COR_AZUL_BEBE, font=("Segoe UI", 8, "bold"), command=lambda: selecionar_pagamento_chat("Cartão de Crédito"))
btn_credito.pack(side="left", expand=True, fill="x", padx=2)

btn_debito = tk.Button(frame_botoes_pagto, text="Débito 💳", bg=COR_AZUL_BEBE, font=("Segoe UI", 8, "bold"), command=lambda: selecionar_pagamento_chat("Cartão de Débito"))
btn_debito.pack(side="left", expand=True, fill="x", padx=2)

btn_dinheiro = tk.Button(frame_botoes_pagto, text="Dinheiro 💵", bg=COR_AZUL_BEBE, font=("Segoe UI", 8, "bold"), command=lambda: selecionar_pagamento_chat("Dinheiro"))
btn_dinheiro.pack(side="left", expand=True, fill="x", padx=2)

# Campo para digitar mensagem
frame_mensagem = tk.Frame(aba_chat, bg=COR_BRANCO)
frame_mensagem.pack(fill="x", padx=15, pady=10)

entrada_chat = tk.Entry(frame_mensagem, font=("Segoe UI", 10), bd=1, relief="solid")
entrada_chat.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=5)

btn_enviar = tk.Button(
    frame_mensagem,
    text="Enviar  ➤",
    bg=COR_AZUL_BOTAO,
    fg="white",
    font=("Segoe UI", 9, "bold"),
    bd=0,
    padx=20,
    pady=5,
    cursor="hand2",
    command=enviar_mensagem
)
btn_enviar.pack(side="right")

entrada_chat.bind("<Return>", lambda event: enviar_mensagem())

# ==================================================
# INICIALIZAÇÃO
# ==================================================

# Mensagem inicial do chat + Opções A e B
adicionar_chat("🍦 Atendimento Lis", "Olá! Seja muito bem-vindo(a) à Sorveteria da Lis! 💙")
mostrar_menu_opcoes()

# Carregar dados iniciais na interface
atualizar_interface()

# Iniciar Loop Principal
janela.mainloop()