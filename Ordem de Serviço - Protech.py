import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import csv

ordens_servico = []     

#FUNÇÕES PRINCIPAIS
def adicionar_ordem():
    campos = [
        entrada_modelo, entrada_descricao, entrada_tipo,
        entrada_custo, entrada_receita,
        entrada_data_ordem, entrada_data_entrega,
        entrada_cliente, entrada_telefone
    ]
    nomes_campos = [
        "modelo", "Descrição", "tipo", "custo", "receita",
        "Data da Ordem", "Data de Entrega", "cliente", "telefone"
    ]
    campos_invalidos = validar_campos(campos, nomes_campos)

    if campos_invalidos:
        lista = "\n- " + "\n- ".join(campos_invalidos)
        messagebox.showerror("Campos obrigatórios", f"Preencha os seguintes campos:\n{lista}")
        return

    try:
        ordem = {
            "modelo": entrada_modelo.get(),
            "descricao": entrada_descricao.get("1.0", tk.END).strip(),
            "tipo": entrada_tipo.get(),
            "custo": float(entrada_custo.get()),
            "receita": float(entrada_receita.get()),
            "data_ordem": datetime.strptime(entrada_data_ordem.get(), "%d/%m/%Y"),
            "data_entrega": datetime.strptime(entrada_data_entrega.get(), "%d/%m/%Y"),
            "cliente": entrada_cliente.get(),
            "telefone": entrada_telefone.get()
        }

        ordens_servico.append(ordem)
        atualizar_tabela(ordens_servico)
        limpar_campos()

    except ValueError:
        messagebox.showerror("Erro", "Verifique os valores numéricos e datas.")

def validar_campos(campos, nomes_campos):
    campos_invalidos = []   
    for campo, nome in zip(campos, nomes_campos):
        if isinstance(campo, tk.Entry):
            valor = campo.get().strip()
        elif isinstance(campo, tk.Text):
            valor = campo.get("1.0", tk.END).strip()
        else:
            valor = ""
        if not valor:
            campo.config(bg="#ffdddd")  # destaque visual
            campos_invalidos.append(nome)
        else:
            campo.config(bg="white")  # limpa cor se estiver ok
    return campos_invalidos

def limpar_campos():
    campos = [
        entrada_modelo,
        entrada_descricao,
        entrada_tipo,
        entrada_custo,
        entrada_receita,
        entrada_data_ordem,
        entrada_data_entrega,
        entrada_cliente,
        entrada_telefone,
    ]

    for campo in campos:
        if isinstance(campo, tk.Entry):
            campo.delete(0, tk.END)
        elif isinstance(campo, tk.Text):
            campo.delete("1.0", tk.END)


def atualizar_tabela(lista):
    tabela.delete(*tabela.get_children())
    for i, ordem in enumerate(lista, start=1):
        dias_diferenca = (ordem["data_entrega"] - ordem["data_ordem"]).days
        tag = "atraso" if dias_diferenca >= 5 else ""
        lucro = ordem["receita"] - ordem["custo"]
        zebra = "par" if i % 2 == 0 else "impar"
        tabela.insert("", "end", values=(
            i,
            ordem["modelo"],
            ordem["descricao"],
            ordem["tipo"],
            f"R${ordem['custo']:.2f}",
            f"R${ordem['receita']:.2f}",
            f"R${lucro:.2f}",
            ordem["data_ordem"].strftime("%d/%m/%Y"),
            ordem["data_entrega"].strftime("%d/%m/%Y"),
            ordem["cliente"],
            ordem["telefone"]
        ), tags=(tag, zebra))

# Cores alternadas
    tabela.tag_configure("par", background="#f9f9f9")
    tabela.tag_configure("impar", background="#ffffff")


def calcular_balanco():
    total_custo = sum(o["custo"] for o in ordens_servico)
    total_receita = sum(o["receita"] for o in ordens_servico)
    balanco = total_receita - total_custo
    messagebox.showinfo("Balanço Geral", f"Receita: R${total_receita:.2f}\nCusto: R${total_custo:.2f}\nBalanço: R${balanco:.2f}")


def salvar_csv():
    with open("ordens_servico.csv", "w", newline="", encoding="utf-8") as f:
        campos = ["modelo", "descricao", "tipo", "custo", "receita", "data_ordem", "data_entrega", "cliente", "telefone"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for o in ordens_servico:
            writer.writerow({
                "modelo": o["modelo"],
                "descricao": o["descricao"],
                "tipo": o["tipo"],
                "custo": o["custo"],
                "receita": o["receita"],
                "data_ordem": o["data_ordem"].strftime("%d/%m/%Y"),
                "data_entrega": o["data_entrega"].strftime("%d/%m/%Y"),
                "cliente": o["cliente"],
                "telefone": o["telefone"]
            })
    messagebox.showinfo("Salvo", "Dados salvos em 'ordens_servico.csv'.")

def salvar_como_csv():
    caminho = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Salvar como"
    )
    if caminho:
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            campos = ["modelo", "descricao", "tipo", "custo", "receita", "data_ordem", "data_entrega", "cliente", "telefone"]
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            for o in ordens_servico:
                writer.writerow({   
                    "modelo": o["modelo"],
                    "descricao": o["descricao"],
                    "tipo": o["tipo"],
                    "custo": o["custo"],
                    "receita": o["receita"],
                    "data_ordem": o["data_ordem"].strftime("%d/%m/%Y"),
                    "data_entrega": o["data_entrega"].strftime("%d/%m/%Y"),
                    "cliente": o["cliente"],
                    "telefone": o["telefone"]
                })
        messagebox.showinfo("Salvo", f"Arquivo salvo em:\n{caminho}")

def carregar_csv():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if not caminho:
        return

    try:
        with open(caminho, newline='', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            ordens_servico.clear()
            for linha in leitor:
                try:
                    ordem = {
                        "modelo": linha.get("modelo", ""),
                        "descricao": linha.get("descricao", ""),
                        "tipo": linha.get("tipo", ""),
                        "custo": float(linha.get("custo", 0)),
                        "receita": float(linha.get("receita", 0)),
                        "data_ordem": datetime.strptime(linha.get("data_ordem", "01/01/2000"), "%d/%m/%Y"),
                        "data_entrega": datetime.strptime(linha.get("data_entrega", "01/01/2000"), "%d/%m/%Y"),
                        "cliente": linha.get("cliente", ""),     # ← garante que existe
                        "telefone": linha.get("telefone", "")    # ← garante que existe
                    }
                    ordens_servico.append(ordem)
                except Exception as e:
                    print(f"Erro ao processar linha: {e}")
        atualizar_tabela(ordens_servico)
        messagebox.showinfo("Sucesso", "CSV carregado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar CSV: {e}")

        atualizar_tabela(ordens_servico)
        messagebox.showinfo("Carregado", "Dados carregados com sucesso!")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado.")

def filtrar_periodo():
    try:
        inicio = datetime.strptime(entrada_inicio.get(), "%d/%m/%Y")
        fim = datetime.strptime(entrada_fim.get(), "%d/%m/%Y")
        filtradas = [o for o in ordens_servico if inicio <= o["data_ordem"] <= fim]
        atualizar_tabela(filtradas)
        total_custo = sum(o["custo"] for o in filtradas)
        total_receita = sum(o["receita"] for o in filtradas)
        balanco = total_receita - total_custo
        messagebox.showinfo("Resumo do Período", f"Receita: R${total_receita:.2f}\nCusto: R${total_custo:.2f}\nBalanço: R${balanco:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Use datas no formato DD/MM/AAAA.")

def carregar_para_edicao(event=None):
    selecionado = tabela.focus()
    if not selecionado:
        return
    valores = tabela.item(selecionado, "values")
    if not valores:
        return

    entrada_modelo.delete(0, tk.END)
    entrada_modelo.insert(0, valores[1])

    entrada_descricao.delete("1.0", tk.END)
    entrada_descricao.insert("1.0", valores[2])

    entrada_tipo.delete(0, tk.END)
    entrada_tipo.insert(0, valores[3])

    entrada_custo.delete(0, tk.END)
    entrada_custo.insert(0, valores[4].replace("R$", "").replace(",", "."))

    entrada_receita.delete(0, tk.END)
    entrada_receita.insert(0, valores[5].replace("R$", "").replace(",", "."))

    entrada_data_ordem.delete(0, tk.END)
    entrada_data_ordem.insert(0, valores[7])

    entrada_data_entrega.delete(0, tk.END)
    entrada_data_entrega.insert(0, valores[8])

    entrada_cliente.delete(0, tk.END)
    entrada_cliente.insert(0, valores[9])

    entrada_telefone.delete(0, tk.END)
    entrada_telefone.insert(0, valores[10])


def excluir_ordem():
    selecionado = tabela.focus()
    if not selecionado:
        return
    index = int(tabela.item(selecionado, "values")[0]) - 1
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir esta ordem?")
    if resposta:
        del ordens_servico[index]
        atualizar_tabela(ordens_servico)

def salvar_edicao():
    selecionado = tabela.focus()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione uma ordem para editar.")
        return

    valores = tabela.item(selecionado, "values")
    if not valores:
        messagebox.showerror("Erro", "Não foi possível obter os dados da ordem.")
        return

    try:
        indice = int(valores[0]) - 1  # ID da ordem na tabela

        ordem = {
            "modelo": entrada_modelo.get(),
            "descricao": entrada_descricao.get("1.0", tk.END).strip(),
            "tipo": entrada_tipo.get(),
            "custo": float(entrada_custo.get()),
            "receita": float(entrada_receita.get()),
            "data_ordem": datetime.strptime(entrada_data_ordem.get(), "%d/%m/%Y"),
            "data_entrega": datetime.strptime(entrada_data_entrega.get(), "%d/%m/%Y"),
            "cliente": entrada_cliente.get(),
            "telefone": entrada_telefone.get()
        }

        ordens_servico[indice] = ordem  # ← substitui a ordem existente
        atualizar_tabela(ordens_servico)
        limpar_campos()
        messagebox.showinfo("Sucesso", "Ordem atualizada com sucesso.")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar edição: {e}")

    
def mostrar_menu_contexto(event):
    item = tabela.identify_row(event.y)
    if item:
        tabela.selection_set(item)   # seleciona visualmente
        tabela.focus(item)           # define o foco para ações como excluir
        menu_contexto.post(event.x_root, event.y_root)


# Janela principal
janela = tk.Tk()    
janela.title("Sistema de Ordem de Serviço")
janela.geometry("1100x700")
janela.configure(bg="#f2f2f2")

# Estilo visual
estilo = ttk.Style()
estilo.theme_use("default")
estilo.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=30, fieldbackground="#ffffff", font=("Segoe UI", 10))
estilo.map("Treeview", background=[("selected", "#cce5ff")])
estilo.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#e6e6e6")
tabela_tag = {"atraso": {"background": "#ffcccc"}}

botao_padrao = {"font": ("Segoe UI", 10), "bg": "#4CAF50", "fg": "white", "activebackground": "#45a049"}

def ver_detalhes():
    selecionado = tabela.focus()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione uma ordem para visualizar.")
        return

    valores = tabela.item(selecionado, "values")
    if not valores:
        messagebox.showerror("Erro", "Não foi possível obter os dados da ordem.")
        return

    janela_detalhes = tk.Toplevel()
    janela_detalhes.title("🔍 Detalhes da Ordem")
    janela_detalhes.geometry("420x520")
    janela_detalhes.configure(bg="#f0f0f0")
    janela_detalhes.resizable(False, False)

    # Cabeçalho
    tk.Label(janela_detalhes, text=f"🆔 Ordem #{valores[0]}", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(20, 5))
    tk.Label(janela_detalhes, text=f"👤 Cliente: {valores[9]}", font=("Arial", 11), bg="#f0f0f0").pack(pady=2)
    tk.Label(janela_detalhes, text=f"📞 Telefone: {valores[10]}", font=("Arial", 11), bg="#f0f0f0").pack(pady=2)

    # Separador visual
    tk.Label(janela_detalhes, text="────────────────────────────", bg="#f0f0f0", fg="#888").pack(pady=10)

    # Demais campos organizados
    campos = [
        ("Modelo", valores[1]),
        ("Descrição", valores[2]),
        ("Tipo", valores[3]),
        ("Custo", valores[4]),
        ("Receita", valores[5]),
        ("Lucro", valores[6]),
        ("Data da Ordem", valores[7]),
        ("Data de Entrega", valores[8])
    ]

    for label, valor in campos:
        frame = tk.Frame(janela_detalhes, bg="#f0f0f0")
        frame.pack(fill="x", padx=20, pady=4)
        tk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold"), width=15, anchor="w", bg="#f0f0f0").pack(side="left")
        tk.Label(frame, text=valor, font=("Arial", 10), anchor="w", bg="#f0f0f0").pack(side="left")

    # Linha de assinatura
    tk.Label(janela_detalhes, text="", bg="#f0f0f0").pack(pady=10)  # espaçamento
    tk.Frame(janela_detalhes, height=2, bg="black").pack(fill="x", padx=60, pady=(10, 2))
    tk.Label(janela_detalhes, text="Assinatura do cliente", font=("Arial", 10, "italic"), bg="#f0f0f0").pack(pady=(0, 20))

    # Botão de fechar
    tk.Button(janela_detalhes, text="Fechar", command=janela_detalhes.destroy, bg="#d9534f", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

def duplicar_ordem():
    selecionado = tabela.focus()
    if not selecionado:
        return
    valores = tabela.item(selecionado, "values")
    if not valores:
        return

    try:
        nova_ordem = {
            "modelo": valores[1],
            "descricao": valores[2],
            "tipo": valores[3],
            "custo": float(valores[4].replace("R$", "").replace(",", ".")),
            "receita": float(valores[5].replace("R$", "").replace(",", ".")),
            "data_ordem": datetime.strptime(valores[7], "%d/%m/%Y"),
            "data_entrega": datetime.strptime(valores[8], "%d/%m/%Y"),
            "cliente": valores[9] if len(valores) > 9 else "",
            "telefone": valores[10] if len(valores) > 10 else "",

        }
        ordens_servico.append(nova_ordem)
        atualizar_tabela(ordens_servico)
        messagebox.showinfo("Duplicado", "Ordem duplicada com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao duplicar: {e}")

# Botão "Salvar Como..."
tk.Button(janela, text="Salvar Como...", command=salvar_como_csv, width=20, **botao_padrao).pack(pady=5)

modo_escuro = False

def alternar_tema():
    global modo_escuro
    modo_escuro = not modo_escuro

    cor_fundo = "#2c2c2c" if modo_escuro else "#f2f2f2"
    cor_texto = "#ffffff" if modo_escuro else "#000000"
    cor_entry = "#3c3c3c" if modo_escuro else "#ffffff"

    janela.configure(bg=cor_fundo)

    # Atualiza todos os frames e seus filhos
    for frame in [frame_entrada, frame_botoes, frame_filtro]:
        frame.configure(bg=cor_fundo)
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=cor_fundo, fg=cor_texto)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=cor_entry, fg=cor_texto, insertbackground=cor_texto)
            elif isinstance(widget, tk.Button):
                widget.configure(bg="#555555" if modo_escuro else botao_padrao["bg"], fg=cor_texto)
            elif isinstance(widget, tk.Text):
                widget.configure(bg=cor_entry, fg=cor_texto, insertbackground=cor_texto)

    # Atualiza botões fora dos frames
    for widget in janela.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(bg="#555555" if modo_escuro else botao_padrao["bg"], fg=cor_texto)

tk.Button(janela, text="Alternar Tema", command=alternar_tema, width=20, bg="#333", fg="white").pack(pady=5)


# Frame de entrada
frame_entrada = tk.Frame(janela, bg="#f2f2f2")
frame_entrada.pack(pady=10)

tk.Label(frame_entrada, text="Modelo:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
entrada_modelo = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_modelo.grid(row=0, column=1)

tk.Label(frame_entrada, text="Descrição:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, padx=5)
entrada_descricao = tk.Text(frame_entrada, width=40, height=5, font=("Segoe UI", 10))
entrada_descricao.grid(row=0, column=5, rowspan=5, pady=5)

tk.Label(frame_entrada, text="Tipo:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5)
entrada_tipo = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_tipo.grid(row=0, column=3)

tk.Label(frame_entrada, text="Custo (R$):", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
entrada_custo = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_custo.grid(row=1, column=1)

tk.Label(frame_entrada, text="Receita (R$):", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, padx=5)
entrada_receita = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_receita.grid(row=1, column=3)

tk.Label(frame_entrada, text="Data Ordem:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, padx=5)
entrada_data_ordem = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_data_ordem.grid(row=2, column=1)


tk.Label(frame_entrada, text="Data Entrega:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, padx=5)
entrada_data_entrega = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_data_entrega.grid(row=2, column=3)

tk.Label(frame_entrada, text="Cliente:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
entrada_cliente = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_cliente.grid(row=3, column=1)

tk.Label(frame_entrada, text="Telefone:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=3, column=2, padx=5, pady=5)
entrada_telefone = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_telefone.grid(row=3, column=3)

# Botões principais
frame_botoes = tk.Frame(janela, bg="#f2f2f2")
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Adicionar Ordem", command=adicionar_ordem, width=20, **botao_padrao).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text="Calcular Balanço Geral", command=calcular_balanco, width=20, **botao_padrao).grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text="Salvar em CSV", command=salvar_csv, width=20, **botao_padrao).grid(row=0, column=2, padx=5)
tk.Button(frame_botoes, text="Carregar do CSV", command=carregar_csv, width=20, **botao_padrao).grid(row=0, column=3, padx=5)
tk.Button(frame_botoes, text="Carregar para Edição", command=carregar_para_edicao, width=20, **botao_padrao).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Salvar Edição", command=salvar_edicao, width=20, **botao_padrao).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_botoes, text="Limpar Campos", command=limpar_campos, width=20, **botao_padrao).grid(row=1, column=2, padx=5, pady=5)


# Filtro por período
frame_filtro = tk.Frame(janela, bg="#f2f2f2")
frame_filtro.pack(pady=10)

tk.Label(frame_filtro, text="Filtrar por Período (DD/MM/AAAA):", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
entrada_inicio = tk.Entry(frame_filtro, width=15, font=("Segoe UI", 10))
entrada_inicio.grid(row=0, column=1)
entrada_fim = tk.Entry(frame_filtro, width=15, font=("Segoe UI", 10))
entrada_fim.grid(row=0, column=2)
tk.Button(frame_filtro, text="Filtrar e Mostrar Resumo", command=filtrar_periodo, width=25, **botao_padrao).grid(row=0, column=3, padx=5)

# Tabela
colunas = ("ID", "modelo", "Descrição", "tipo", "custo", "receita", "Valor Lucro", "Data Ordem", "Data Entrega", "cliente", "telefone")
tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=20)
tabela.tag_configure("atraso", background="#ffcccc")  # vermelho claro para entregas com atraso

for col in colunas:
    tabela.heading(col, text=col)
    if col == "Descrição":
        tabela.column(col, width=200)
    elif col =="Valor Lucro":
        tabela.column(col, width=120)
    elif col == "cliente":
        tabela.column(col, width=150)
    elif col == "telefone":
        tabela.column(col, width=120)
    else:
        tabela.column(col, width=110)

tabela.pack(expand=True, fill="both", padx=10, pady=10)
tabela.bind("<Double-1>", carregar_para_edicao)

menu_contexto = tk.Menu(janela, tearoff=0)
menu_contexto.add_command(label="Editar", command=carregar_para_edicao)
menu_contexto.add_command(label="Excluir", command=excluir_ordem)

tabela.bind("<Button-3>", mostrar_menu_contexto)  # Botão direito

menu_contexto = tk.Menu(janela, tearoff=0)
menu_contexto.add_command(label="Editar", command=carregar_para_edicao)
menu_contexto.add_command(label="Excluir", command=excluir_ordem)
menu_contexto.add_command(label="Ver Detalhes", command=ver_detalhes)
menu_contexto.add_command(label="Duplicar Ordem", command=duplicar_ordem)

tabela.bind("<Button-3>", mostrar_menu_contexto)

# Iniciar interface
janela.mainloop()


