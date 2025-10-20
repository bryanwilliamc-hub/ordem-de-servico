import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import csv
import json
import hashlib
import os
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import sys, os


def verificar_login(usuario, senha_digitada):
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
        if usuario in usuarios:
            senha_armazenada = usuarios[usuario]["senha"]
            senha_hash = hashlib.md5(senha_digitada.encode()).hexdigest()
            if senha_hash == senha_armazenada:
                return usuarios[usuario]["nivel"]   
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
    return None

def tela_login():
    login = tk.Tk()
    login.title("🔐 Login")
    login.geometry("300x200")
    login.resizable(False, False)

    resultado = {"nivel": None}

    def autenticar():
        usuario = entrada_usuario.get()
        senha = entrada_senha.get()
        nivel = verificar_login(usuario, senha)
        if nivel:
            resultado["nivel"] = nivel
            login.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def fechar_login():
        resultado["nivel"] = None
        login.destroy()

    login.protocol("WM_DELETE_WINDOW", fechar_login)

    tk.Label(login, text="Usuário:").pack(pady=(20, 5))
    entrada_usuario = tk.Entry(login)
    entrada_usuario.pack()

    tk.Label(login, text="Senha:").pack(pady=5)
    entrada_senha = tk.Entry(login, show="*", width=30)
    entrada_senha.pack()

    tk.Button(login, text="Entrar", command=autenticar, bg="#4CAF50", fg="white").pack(pady=20)

    login.mainloop()
    return resultado["nivel"]

def iniciar_sistema(nivel):
    root = tk.Tk()
    root.title(f"Sistema de Ordens - Acesso: {nivel}")
    root.geometry("1000x600")

    if nivel == "gerente":
        tk.Label(root, text="Bem-vindo, Gerente!", font=("Arial", 14)).pack(pady=10)
    elif nivel == "operador":
        tk.Label(root, text="Bem-vindo, Operador!", font=("Arial", 14)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    nivel = tela_login()
    if nivel:
        iniciar_sistema(nivel)
    else:
        print("Login cancelado. Encerrando o sistema.")

ordens_servico = []     

def gerar_id():
    if not ordens_servico:
        return 1
    else:
        return max(ordem.get("id", 0) for ordem in ordens_servico if "id" in ordem) + 1

#FUNÇÕES PRINCIPAIS
def adicionar_ordem():
    # validação existente (mantém sua função validar_campos se tiver)
    campos = [entrada_modelo, entrada_descricao, entrada_tipo, entrada_custo, entrada_valor_total, entrada_data_ordem, entrada_data_entrega, entrada_cliente, entrada_telefone]
    nomes_campos = ["modelo", "Descricao", "tipo", "custo", "valor total", "Data da Ordem", "Data de Entrega", "cliente", "telefone"]
    campos_invalidos = validar_campos(campos, nomes_campos)
    if campos_invalidos:
        lista = "\n- " + "\n- ".join(campos_invalidos)
        messagebox.showerror("Campos obrigatorios", f"Preencha os seguintes campos:\n{lista}")
        return

    try:
        # custo numérico
        custo = float(entrada_custo.get().replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
        # valor_total: pega do campo de exibição (entrada_valor_total) ou calcula a partir de campo_servicos_var se preferir
        raw_val = entrada_valor_total.get().replace("R$", "").replace(" ", "").strip()
        raw_val = raw_val.replace(".", "").replace(",", ".") if raw_val else "0"
        valor_total = float(raw_val)

        lucro = valor_total - custo

        ordem = {
            "id": gerar_id(),
            "modelo": entrada_modelo.get(),
            "descricao": entrada_descricao.get("1.0", tk.END).strip(),
            "tipo": entrada_tipo.get(),
            "custo": custo,
            "valor_total": valor_total,               # número (para salvar)
            "valor_total_str": entrada_valor_total.get(),  # string formatada (exibição)
            "lucro": lucro,
            "data_ordem": datetime.strptime(entrada_data_ordem.get(), "%d/%m/%Y").date() if entrada_data_ordem.get() else None,
            "data_entrega": datetime.strptime(entrada_data_entrega.get(), "%d/%m/%Y") if entrada_data_entrega.get() else None,
            "cliente": entrada_cliente.get(),
            "telefone": entrada_telefone.get(),
            "servicos": campo_servicos_var.get().strip(),   # <<-- garante salvar serviços do popup
        }
        print("DEBUG adicionar_ordem -> servicos:", ordem["servicos"])
       
        ordens_servico.append(ordem)
        atualizar_tabela(ordens_servico)
        limpar_campos()
    except ValueError:
        messagebox.showerror("Erro", "Verifique os valores numericos e datas.")

def abrir_janela_servicos_cadastrados():
    janela_servicos = tk.Toplevel(janela)
    janela_servicos.title("Serviços Cadastrados")
    janela_servicos.geometry("800x600")  # Mesmo tamanho da principal
    janela_servicos.configure(bg="#f2f2f2")

    tk.Label(janela_servicos, text="Serviços Cadastrados", font=("Segoe UI", 14, "bold"), bg="#f2f2f2").pack(pady=10)

    # Frame para a lista
    frame_lista = tk.Frame(janela_servicos, bg="#f2f2f2")
    frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

    # Cabeçalhos
    tk.Label(frame_lista, text="Serviço", font=("Segoe UI", 11, "bold"), bg="#f2f2f2", anchor="w", width=40).grid(row=0, column=0, sticky="w")
    tk.Label(frame_lista, text="Valor (R$)", font=("Segoe UI", 11, "bold"), bg="#f2f2f2", anchor="w", width=20).grid(row=0, column=1, sticky="w")

    # Listar serviços
    for i, servico in enumerate(servicos_cadastrados, start=1):
        tk.Label(frame_lista, text=servico["nome"], font=("Segoe UI", 10), bg="#f2f2f2", anchor="w", width=40).grid(row=i, column=0, sticky="w", pady=2)
        tk.Label(frame_lista, text=servico["valor"], font=("Segoe UI", 10), bg="#f2f2f2", anchor="w", width=20).grid(row=i, column=1, sticky="w", pady=2) 

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
        entrada_modelo, entrada_descricao, entrada_tipo, entrada_custo, entrada_valor_total,
        entrada_data_ordem, entrada_data_entrega, entrada_cliente, entrada_telefone,
    ]
    for campo in campos:
        if isinstance(campo, tk.Entry):
            campo.delete(0, tk.END)
        elif isinstance(campo, tk.Text):
            campo.delete("1.0", tk.END)
    # limpa serviços e seu campo
    try:
        campo_servicos_var.set("")
        campo_valor_total_var.set("")
    except Exception:
        pass


def atualizar_tabela(lista):
    # Limpa a tabela atual
    tabela.delete(*tabela.get_children())
    # Insere os dados da lista fornecida
    for ordem in lista:
        # cuidado: data_ordem e data_entrega podem ser None, ajustar exibição
        data_ordem_str = ordem["data_ordem"].strftime("%d/%m/%Y") if ordem.get("data_ordem") else ""
        data_entrega_str = ordem["data_entrega"].strftime("%d/%m/%Y") if ordem.get("data_entrega") else ""
        tabela.insert("", "end", values=(
            ordem["id"],
            ordem.get("modelo", ""),
            ordem.get("descricao", ""),
            ordem.get("tipo", ""),
            f'R${ordem.get("custo", 0):.2f}',
            f'R${ordem.get("valor_total", 0):.2f}',
            f'R${ordem.get("lucro", 0):.2f}',
            data_ordem_str,
            data_entrega_str,
            ordem.get("cliente", ""),
            ordem.get("telefone", ""),
            ordem.get("servicos", "")
        ))


def filtrar_por_dia():
    data_selecionada = entrada_data_filtro.get_date()

    # Debug: verificar tipos e valores
    print("Data selecionada:", data_selecionada, type(data_selecionada))
    for o in ordens_servico:
        print("Data da ordem:", o["data_ordem"], type(o["data_ordem"]))

    filtradas = [o for o in ordens_servico if o["data_ordem"] == data_selecionada]

    if not filtradas:
        messagebox.showinfo("Sem resultados", "Nenhuma ordem encontrada para a data selecionada.")
    else:
        atualizar_tabela(filtradas)
        try:
            total_custo = sum(o["custo"] for o in filtradas)
            total_valor_total = sum(o["valor_total"] for o in filtradas)
            balanco = total_valor_total - total_custo

            messagebox.showinfo("Resumo do Dia", f"Data: {data_selecionada.strftime('%d/%m/%Y')}\n"
                                                 f"Ordens: {len(filtradas)}\n"
                                                 f"Valor Total: R${total_valor_total:.2f}\n"
                                                 f"Custo: R${total_custo:.2f}\n"
                                                 f"Balanço: R${balanco:.2f}")
        except ValueError:
            messagebox.showerror("Erro", "Selecione uma data válida.")

# Cores alternadas
    tabela.tag_configure("par", background="#f9f9f9")
    tabela.tag_configure("impar", background="#ffffff")

def limpar_filtro():
    if not ordens_servico:
        messagebox.showinfo("Sem dados", "Nenhuma ordem foi carregada ainda.")
        return

    atualizar_tabela(ordens_servico)
    messagebox.showinfo("Filtro removido", "Todas as ordens estão sendo exibidas.")

def calcular_balanco():
    total_custo = sum(o["custo"] for o in ordens_servico)
    total_valor_total = sum(o["valor_total"] for o in ordens_servico)
    balanco = total_valor_total - total_custo
    messagebox.showinfo("Balanço Geral", f"valor total: R${total_valor_total:.2f}\nCusto: R${total_custo:.2f}\nBalanço: R${balanco:.2f}")


def salvar_csv():

    print("DEBUG salvar_csv -> ordens_servico servicos:", [o.get("servicos") for o in ordens_servico])
    
    if not ordens_servico:
        messagebox.showwarning("Nenhuma ordem", "Nao ha ordens para salvar.")
        return

    resposta = messagebox.askyesnocancel(
        "Salvar CSV",
        "Deseja sobrescrever o arquivo atual?\n\nSim: sobrescrever\nNao: salvar como novo\nCancelar: abortar"
    )
    if resposta is None:
        return
    if resposta:
        caminho = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")], title="Selecione o arquivo para sobrescrever")
    else:
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivos CSV", "*.csv")], title="Salvar como novo")
    if not caminho:
        return

    def _normalizar_valor(v):
        # aceita float ou string; retorna string com ponto como separador (para CSV)
        try:
            if v is None:
                return "0.00"
            if isinstance(v, (int, float)):
                return f"{float(v):.2f}"
            s = str(v).strip()
            # remove "R$", espaços e milhares, transforma vírgula em ponto
            s = s.replace("R$", "").replace("r$", "").replace(" ", "")
            s = s.replace(".", "").replace(",", ".") if ("," in s and "." in s and s.find(",") > s.find(".")) else s.replace(".", "")
            s = s.replace(",", ".")
            return f"{float(s):.2f}"
        except Exception:
            return "0.00"

    try:
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            campos = ["ID", "modelo", "descricao", "tipo", "custo", "valor_total", "lucro", "data_ordem", "data_entrega", "cliente", "telefone", "servicos"]
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            for o in ordens_servico:
                # garante presença das chaves e normaliza tipos
                id_val = o.get("id", "")
                modelo = o.get("modelo", "")
                descricao = o.get("descricao", "")
                tipo = o.get("tipo", "")
                custo_raw = o.get("custo", 0)
                # normaliza custo para número com ponto
                try:
                    custo = float(custo_raw)
                except Exception:
                    try:
                        custo = float(str(custo_raw).replace("R$", "").replace(".", "").replace(",", "."))
                    except Exception:
                        custo = 0.0
                valor_total_norm = _normalizar_valor(o.get("valor_total", o.get("valor_total_str", "")))
                # lucro: calcula se não existir
                lucro = o.get("lucro", "")
                try:
                    if lucro == "" or lucro is None:
                        lucro = float(valor_total_norm) - float(custo)
                    else:
                        lucro = float(lucro)
                except Exception:
                    lucro = 0.0

                data_ordem = ""
                data_entrega = ""
                try:
                    if o.get("data_ordem"):
                        dt = o.get("data_ordem")
                        data_ordem = dt.strftime("%d/%m/%Y") if hasattr(dt, "strftime") else str(dt)
                except Exception:
                    data_ordem = str(o.get("data_ordem", "")) or ""

                try:
                    if o.get("data_entrega"):
                        dt2 = o.get("data_entrega")
                        data_entrega = dt2.strftime("%d/%m/%Y") if hasattr(dt2, "strftime") else str(dt2)
                except Exception:
                    data_entrega = str(o.get("data_entrega", "")) or ""

                escritor.writerow({
                    "ID": id_val,
                    "modelo": modelo,
                    "descricao": descricao,
                    "tipo": tipo,
                    "custo": f"{float(custo):.2f}",
                    "valor_total": valor_total_norm,
                    "lucro": f"{float(lucro):.2f}",
                    "data_ordem": data_ordem,
                    "data_entrega": data_entrega,
                    "cliente": o.get("cliente", ""),
                    "telefone": o.get("telefone", ""),
                    "servicos": o.get("servicos", "") or ""
                })
        messagebox.showinfo("Sucesso", "Arquivo CSV salvo com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro ao salvar", f"Ocorreu um erro:\n{e}")


def salvar_como_csv():
    caminho = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Salvar como"
    )
    if caminho:
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            campos = ["modelo","modelo", "descricao", "tipo", "custo", "valor_total", "data_ordem", "data_entrega", "cliente", "telefone"]
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            for o in ordens_servico:
                writer.writerow({   
                    "modelo": o["modelo"],
                    "descricao": o["descricao"],
                    "tipo": o["tipo"],
                    "custo": o["custo"],
                    "valor_total": o["valor_total"],
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
                    # Helper: normalizar valor vindo do CSV (aceita "1234.56" ou "R$ 1.234,56")
                    def _parse_valor(v):
                        if v is None:
                            return 0.0
                        if isinstance(v, (int, float)):
                            return float(v)
                        s = str(v).strip()
                        if not s:
                            return 0.0
                        s = s.replace("R$", "").replace("r$", "").replace(" ", "")
                        # tenta formas comuns: "1.234,56" ou "1234.56"
                        # primeiro remove pontos de milhares, transformando vírgula em ponto
                        if "," in s and "." in s and s.find(",") > s.find("."):
                            s = s.replace(".", "")
                        s = s.replace(",", ".")
                        try:
                            return float(s)
                        except Exception:
                            # último recurso: extrai dígitos e pontos
                            filtered = "".join(ch for ch in s if ch.isdigit() or ch == ".")
                            try:
                                return float(filtered) if filtered else 0.0
                            except Exception:
                                return 0.0

                    # parse datas (tenta formato dd/mm/YYYY, se falhar deixa None ou string)
                    def _parse_data(s):
                        if not s:
                            return None
                        try:
                            return datetime.strptime(s, "%d/%m/%Y").date()
                        except Exception:
                            try:
                                return datetime.strptime(s, "%Y-%m-%d").date()
                            except Exception:
                                return s  # mantém como string se não reconhecer

                    id_raw = linha.get("ID") or linha.get("id") or linha.get("Id") or ""
                    try:
                        id_parsed = int(id_raw)
                    except Exception:
                        id_parsed = id_raw or 0

                    custo = _parse_valor(linha.get("custo", "") or 0)
                    # valor_total pode vir como número ou string formatada; tenta chave valor_total, depois valor_total_str
                    valor_total = _parse_valor(linha.get("valor_total", linha.get("valor_total_str", "")))
                    lucro = _parse_valor(linha.get("lucro", "")) if linha.get("lucro", "") else (valor_total - custo)

                    ordem = {
                        "id": id_parsed,
                        "modelo": linha.get("modelo", "") or "",
                        "descricao": linha.get("descricao", "") or "",
                        "tipo": linha.get("tipo", "") or "",
                        "custo": custo,
                        "valor_total": valor_total,
                        "lucro": lucro,
                        "data_ordem": _parse_data(linha.get("data_ordem", "") or linha.get("Data da Ordem", "")),
                        "data_entrega": _parse_data(linha.get("data_entrega", "") or linha.get("Data de Entrega", "")),
                        "cliente": linha.get("cliente", "") or "",
                        "telefone": linha.get("telefone", "") or "",
                        "servicos": linha.get("servicos", "") or ""
                    }
                    ordens_servico.append(ordem)
                except Exception as e:
                    print(f"Erro ao carregar linha: {linha}\n{e}")
            atualizar_tabela(ordens_servico)
            messagebox.showinfo("Sucesso", "Arquivo CSV carregado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro ao carregar", f"Ocorreu um erro:\n{e}")

def filtrar_periodo():
    try:
        data_inicio = datetime.strptime(entrada_inicio.get(), "%d/%m/%Y").date()
        data_fim = datetime.strptime(entrada_fim.get(), "%d/%m/%Y").date()

        filtradas = [o for o in ordens_servico if data_inicio <= o["data_ordem"] <= data_fim]

        if not filtradas:
            messagebox.showinfo("Sem resultados", "Nenhuma ordem encontrada no período selecionado.")
        else:
            atualizar_tabela(filtradas)

            total_custo = sum(o["custo"] for o in filtradas)
            total_valor_total = sum(o["valor_total"] for o in filtradas)
            balanco = total_valor_total - total_custo

            messagebox.showinfo("Resumo do Período", f"De {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}\n"
                                                      f"Ordens: {len(filtradas)}\n"
                                                      f"Valor Total: R${total_valor_total:.2f}\n"
                                                      f"Custo: R${total_custo:.2f}\n"
                                                      f"Balanço: R${balanco:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Insira datas válidas no formato DD/MM/AAAA.")

def carregar_para_edicao(event=None):
    selecionado = tabela.focus()
    if not selecionado:
        return
    valores = tabela.item(selecionado, "values")
    if not valores:
        return

    # popula campos existentes (ajuste índices conforme sua tabela)
    entrada_modelo.delete(0, tk.END)
    entrada_modelo.insert(0, valores[1])
    entrada_descricao.delete("1.0", tk.END)
    entrada_descricao.insert("1.0", valores[2])
    entrada_tipo.delete(0, tk.END)
    entrada_tipo.insert(0, valores[3])
    entrada_custo.delete(0, tk.END)
    entrada_custo.insert(0, valores[4].replace("R$", "").replace(",", ".").strip())
    entrada_valor_total.delete(0, tk.END)
    entrada_valor_total.insert(0, valores[5].replace("R$", "").replace(",", ".").strip())
    entrada_data_ordem.delete(0, tk.END)
    entrada_data_ordem.insert(0, valores[7])
    entrada_data_entrega.delete(0, tk.END)
    entrada_data_entrega.insert(0, valores[8])
    entrada_cliente.delete(0, tk.END)
    entrada_cliente.insert(0, valores[9])
    entrada_telefone.delete(0, tk.END)
    entrada_telefone.insert(0, valores[10])

    # serviços: se estiver na coluna da tabela, usa; senão tenta pegar da lista ordens_servico pelo id
    servicos_val = ""
    if len(valores) > 11:
        servicos_val = valores[11]
    else:
        try:
            id_val = valores[0]
            for o in ordens_servico:
                if str(o.get("id")) == str(id_val):
                    servicos_val = o.get("servicos", "")
                    break
        except Exception:
            servicos_val = ""
    # preenche a variável ligada ao campo (entry_servicos deve ter textvariable=campo_servicos_var)
    campo_servicos_var.set(servicos_val)


def excluir_ordem():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Seleção necessária", "Selecione uma ordem para excluir.")
        return

    resposta = messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir esta ordem?")
    if not resposta:
        return

    item = tabela.item(selecionado[0])
    valores = item["values"]
    id_selecionado = int(valores[0])  # o ID está na primeira coluna

    # Remove da lista usando o ID
    ordens_servico[:] = [o for o in ordens_servico if o["id"] != id_selecionado]
    atualizar_tabela(ordens_servico)

def salvar_edicao(id_ordem):
    # localizar índice/objeto na lista ordens_servico pelo id_ordem
    for i, o in enumerate(ordens_servico):
        if str(o.get("id")) == str(id_ordem):
            try:
                custo = float(entrada_custo.get().replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
            except Exception:
                custo = 0.0
            raw_val = entrada_valor_total.get().replace("R$", "").replace(" ", "").strip()
            raw_val = raw_val.replace(".", "").replace(",", ".") if raw_val else "0"
            try:
                valor_total = float(raw_val)
            except Exception:
                valor_total = 0.0
            lucro = valor_total - custo

            ordens_servico[i].update({
                "modelo": entrada_modelo.get(),
                "descricao": entrada_descricao.get("1.0", tk.END).strip(),
                "tipo": entrada_tipo.get(),
                "custo": custo,
                "valor_total": valor_total,
                "valor_total_str": entrada_valor_total.get(),
                "lucro": lucro,
                "data_ordem": datetime.strptime(entrada_data_ordem.get(), "%d/%m/%Y").date() if entrada_data_ordem.get() else None,
                "data_entrega": datetime.strptime(entrada_data_entrega.get(), "%d/%m/%Y") if entrada_data_entrega.get() else None,
                "cliente": entrada_cliente.get(),
                "telefone": entrada_telefone.get(),
                "servicos": campo_servicos_var.get().strip(),   # <<-- garante salvar serviços editados
            })
            atualizar_tabela(ordens_servico)
            limpar_campos()
            return True
    messagebox.showerror("Erro", "Ordem para edição não encontrada.")
    return False

    
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

# Lista global para armazenar os serviços cadastrados

servicos_cadastrados = []

def abrir_janela_parametrizacao():
    popup = tk.Toplevel(janela)
    popup.title("Cadastro de Serviços e Valores")
    popup.geometry("400x300")
    popup.configure(bg="#f2f2f2")

    tk.Label(popup, text="Cadastrar Serviço", font=("Segoe UI", 12, "bold"), bg="#f2f2f2").pack(pady=10)

    tk.Label(popup, text="Nome do Serviço:", font=("Segoe UI", 10), bg="#f2f2f2").pack(anchor="w", padx=20)
    entrada_nome = tk.Entry(popup, font=("Segoe UI", 10), width=40)
    entrada_nome.pack(padx=20, pady=5)

    tk.Label(popup, text="Valor (R$):", font=("Segoe UI", 10), bg="#f2f2f2").pack(anchor="w", padx=20)
    entrada_valor = tk.Entry(popup, font=("Segoe UI", 10), width=20)
    entrada_valor.pack(padx=20, pady=5)

    def salvar_servico():
        nome = entrada_nome.get().strip()
        valor = entrada_valor.get().strip()
        if nome and valor:
            servicos_cadastrados.append({"nome": nome, "valor": valor})
            print(f"Serviço cadastrado: {nome} - R$ {valor}")
            entrada_nome.delete(0, tk.END)
            entrada_valor.delete(0, tk.END)

    tk.Button(popup, text="Salvar", command=salvar_servico, font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white").pack(pady=10)


# Barra de menu no topo
barra_menu = tk.Menu(janela)
janela.config(menu=barra_menu)

# Menu "Configurações"
menu_config = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Serviços e Valores", menu=menu_config)

# Nova opção no menu para visualizar serviços cadastrados
menu_config.add_command(label="Serviços Cadastrados", command=abrir_janela_servicos_cadastrados)

# Item que abre a janela de parametrização
menu_config.add_command(label="Cadastrar Serviços", command=abrir_janela_parametrizacao)


# Frame do topo com logo e título
frame_topo = tk.Frame(janela, bg="#f0f0f0")
frame_topo.pack(fill="x", padx=10, pady=10)

# Detecta se está rodando como .exe ou .py
if getattr(sys, 'frozen', False):
    caminho_base = sys._MEIPASS
else:
    caminho_base = os.path.dirname(__file__)

# Caminho seguro para o logo
caminho_logo = os.path.join(caminho_base, "logo.png")

# Logo
imagem_logo = Image.open(caminho_logo)
imagem_logo = imagem_logo.resize((100, 100))
logo_tk = ImageTk.PhotoImage(imagem_logo)

label_logo = tk.Label(frame_topo, image=logo_tk, bg="#f0f0f0")
label_logo.image = logo_tk
label_logo.pack(side="left")

# Título
label_titulo = tk.Label(frame_topo, text="Sistema de Ordem de Serviço", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
label_titulo.pack(side="left", padx=20)


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

    # obtém serviços (coluna ou lista em memória)
    servicos_text = ""
    if len(valores) > 11 and valores[11]:
        servicos_text = valores[11]
    else:
        try:
            id_val = valores[0]
            if 'ordens_servico' in globals():
                for o in ordens_servico:
                    if str(o.get("id")) == str(id_val):
                        servicos_text = o.get("servicos", "") or servicos_text
                        break
        except Exception:
            servicos_text = servicos_text or ""

    # normaliza linhas de serviço
    linhas = []
    if servicos_text:
        if "\n" in servicos_text:
            linhas = [s.strip() for s in servicos_text.splitlines() if s.strip()]
        else:
            import re
            partes = re.split(r'\s*[;,]\s*', servicos_text)
            linhas = [p.strip() for p in partes if p.strip()]

    # Janela maior e redimensionável
    janela_detalhes = tk.Toplevel()
    janela_detalhes.title("🔍 Detalhes da Ordem")
    janela_detalhes.geometry("720x820")   # maior por padrão
    janela_detalhes.minsize(640, 560)     # tamanho mínimo aceitável
    janela_detalhes.configure(bg="#f0f0f0")
    janela_detalhes.resizable(True, True)

    # Usar frame principal com grid para manter botões fixos abaixo
    main = tk.Frame(janela_detalhes, bg="#f0f0f0")
    main.grid(row=0, column=0, sticky="nsew")
    janela_detalhes.grid_rowconfigure(0, weight=1)
    janela_detalhes.grid_columnconfigure(0, weight=1)

    # Cabeçalho
    tk.Label(main, text=f"🆔 Ordem #{valores[0]}", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=(14, 6))
    tk.Label(main, text=f"👤 Cliente: {valores[9]}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
    tk.Label(main, text=f"📞 Telefone: {valores[10]}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
    tk.Label(main, text="────────────────────────────", bg="#f0f0f0", fg="#888").pack(pady=10)

    # Campos principais
    campos = [
        ("Modelo", valores[1] if len(valores) > 1 else ""),
        ("Descrição", valores[2] if len(valores) > 2 else ""),
        ("Tipo", valores[3] if len(valores) > 3 else ""),
        ("Valor Total", valores[5] if len(valores) > 5 else ""),
        ("Data da Ordem", valores[7] if len(valores) > 7 else ""),
        ("Data de Entrega", valores[8] if len(valores) > 8 else "")
    ]
    for label, valor in campos:
        frame = tk.Frame(main, bg="#f0f0f0")
        frame.pack(fill="x", padx=22, pady=4)
        tk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold"), width=16, anchor="w", bg="#f0f0f0").pack(side="left")
        tk.Label(frame, text=valor, font=("Arial", 10), anchor="w", bg="#f0f0f0", wraplength=520).pack(side="left")

    # Área de serviços: título + container com canvas (maior)
    tk.Label(main, text="Serviços Prestados:", anchor="w", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(anchor="w", padx=22, pady=(8,0))
    cont_serv = tk.Frame(main, bg="#ffffff", bd=1, relief="solid")
    cont_serv.pack(fill="both", expand=True, padx=22, pady=(6, 12))

    # Canvas com scrollbar vertical e também horizontal para linhas longas
    canvas = tk.Canvas(cont_serv, bg="#ffffff", highlightthickness=0)
    v_scroll = tk.Scrollbar(cont_serv, orient="vertical", command=canvas.yview)
    h_scroll = tk.Scrollbar(cont_serv, orient="horizontal", command=canvas.xview)
    scroll_frame = tk.Frame(canvas, bg="#ffffff")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    canvas.pack(side="top", fill="both", expand=True)
    v_scroll.pack(side="right", fill="y")
    h_scroll.pack(side="bottom", fill="x")

    # Preenche cada serviço como label separada, mantendo padrão de fonte e alinhamento
    if not linhas:
        tk.Label(scroll_frame, text="Nenhum serviço registrado.", font=("Arial", 11), bg="#ffffff", anchor="w", justify="left").pack(fill="x", padx=12, pady=8)
    else:
        for s in linhas:
            tk.Label(scroll_frame, text=f"• {s}", font=("Arial", 11), bg="#ffffff", anchor="w", justify="left", wraplength=620).pack(fill="x", padx=12, pady=6)

    # Área de assinaturas e botões fixos em frame inferior
    footer = tk.Frame(janela_detalhes, bg="#f0f0f0")
    footer.grid(row=1, column=0, sticky="ew")
    janela_detalhes.grid_rowconfigure(1, weight=0)

    # Linhas de assinatura dentro do footer para garantir visibilidade
    sig_frame = tk.Frame(footer, bg="#f0f0f0")
    sig_frame.pack(fill="x", padx=22, pady=(8,6))
    tk.Frame(sig_frame, height=2, bg="black").pack(fill="x", padx=40, pady=(4,2))
    tk.Label(sig_frame, text="Assinatura do cliente", font=("Arial", 10, "italic"), bg="#f0f0f0").pack(pady=(2,8))
    tk.Frame(sig_frame, height=2, bg="black").pack(fill="x", padx=40, pady=(4,2))
    tk.Label(sig_frame, text="Assinatura do executor", font=("Arial", 10, "italic"), bg="#f0f0f0").pack(pady=(2,8))

    # Botões finais: Imprimir, Salvar PDF, Fechar (sempre visíveis)
    btn_frame = tk.Frame(footer, bg="#f0f0f0")
    btn_frame.pack(fill="x", padx=22, pady=(0,12))
    def _montar_texto_exportacao():
        lines = []
        lines.append(f"Ordem ID: {valores[0]}")
        lines.append(f"Cliente: {valores[9]}")
        lines.append(f"Telefone: {valores[10]}")
        lines.append("")
        for label, valor in campos:
            lines.append(f"{label}: {valor}")
        lines.append("")
        lines.append("Serviços Prestados:")
        if linhas:
            for s in linhas:
                lines.append(f"- {s}")
        else:
            lines.append("Nenhum serviço registrado.")
        lines.append("")
        lines.append("Assinatura do cliente: ________________________")
        lines.append("Assinatura do executor: _______________________")
        return "\n".join(lines)

    import os, tempfile
    from tkinter import filedialog
    def imprimir():
        try:
            texto = _montar_texto_exportacao()
            fd, path = tempfile.mkstemp(suffix=".txt")
            os.close(fd)
            with open(path, "w", encoding="utf-8") as f:
                f.write(texto)
            if os.name == "nt":
                try:
                    os.startfile(path, "print")
                except Exception:
                    messagebox.showinfo("Imprimir", f"Arquivo preparado para impressão em: {path}")
            else:
                messagebox.showinfo("Imprimir", f"Arquivo preparado em: {path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao preparar impressão:\n{e}")

    def salvar_pdf():
        try:
            texto = _montar_texto_exportacao()
            caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf"), ("Texto", "*.txt")])
            if not caminho:
                return
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto)
            messagebox.showinfo("Salvar", f"Arquivo salvo em: {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar arquivo:\n{e}")

    def copiar_servicos():
        try:
            janela.clipboard_clear()
            janela.clipboard_append(servicos_text)
            messagebox.showinfo("Copiado", "Serviços copiados para a área de transferência.")
        except Exception:
            messagebox.showerror("Erro", "Falha ao copiar para a área de transferência.")

    tk.Button(btn_frame, text="Imprimir", command=imprimir, width=14, bg="#4CAF50", fg="white").pack(side="left")
    tk.Button(btn_frame, text="Salvar PDF", command=salvar_pdf, width=14).pack(side="left", padx=8)
    tk.Button(btn_frame, text="Copiar Serviços", command=copiar_servicos, width=14).pack(side="left", padx=8)
    tk.Button(btn_frame, text="Fechar", command=janela_detalhes.destroy, width=12).pack(side="right")

    def imprimir_detalhes():
        texto = "\n".join([f"{label}: {valor}" for label, valor in campos])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp:
            temp.write(texto)
            os.startfile(temp.name, "print")

    def salvar_detalhes_pdf():
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if caminho:
            c = canvas.Canvas(caminho, pagesize=A4)
            largura, altura = A4
            y = altura - 50
            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"Ordem #{valores[0]}")
            y -= 30
            for label, valor in campos:
                c.drawString(50, y, f"{label}: {valor}")
                y -= 20
            c.drawString(50, y - 20, "Assinatura do cliente: __________________________")
            c.save()
            messagebox.showinfo("PDF", "Detalhes salvos em PDF com sucesso.")

    # Botões de ação
    frame_botoes = tk.Frame(janela_detalhes, bg="#f0f0f0")
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="🖨️ Imprimir", command=imprimir_detalhes, bg="#0275d8", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="📄 Salvar PDF", command=salvar_detalhes_pdf, bg="#5bc0de", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="❌ Fechar", command=janela_detalhes.destroy, bg="#d9534f", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    
def duplicar_ordem():
    selecionado = tabela.focus()
    if not selecionado:
        return
    valores = tabela.item(selecionado, "values")
    if not valores:
        return

    try:
        nova_ordem = {
            "id": gerar_id(),
            "modelo": valores[1],
            "descricao": valores[2],
            "tipo": valores[3],
            "custo": float(valores[4].replace("R$", "").replace(",", ".")),
            "valor_total": float(valores[5].replace("R$", "").replace(",", ".")),
            "lucro": float(valores[5].replace("R$", "").replace(",", ".")) - float(valores[4].replace("R$", "").replace(",", ".")),
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

# Função para abrir o popup
def abrir_popup_servicos():
    global entrada_valor_total
    popup = tk.Toplevel(janela)
    popup.title("Selecionar Serviços Prestados")
    popup.geometry("400x400")
    popup.configure(bg="#f2f2f2")

    vars_popup = []
    for servico in servicos_cadastrados:
        texto = f"{servico['nome']} - R$ {servico['valor']}"
        var = tk.BooleanVar()
        chk = tk.Checkbutton(popup, text=texto, variable=var, bg="#f2f2f2", font=("Segoe UI", 10), anchor="w")
        chk.pack(anchor="w", padx=20, pady=2)
        vars_popup.append((servico, var))

    def confirmar():
        servicos_selecionados.clear()
        total = 0.0
        textos = []
        for servico, var in vars_popup:
            if var.get():
                textos.append(f"{servico['nome']} - R$ {servico['valor']}")
                try:
                    total += float(servico['valor'].replace(",", "."))
                except ValueError:
                    pass
        campo_servicos_var.set(", ".join(textos))
        campo_valor_total_var.set(f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        popup.destroy()

    btn_confirmar = tk.Button(popup, text="Confirmar", command=confirmar, font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white")
    btn_confirmar.pack(pady=10)

# Frame de entrada
frame_entrada = tk.Frame(janela, bg="#f2f2f2")
frame_entrada.pack(pady=10)

tk.Label(frame_entrada, text="Modelo:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
entrada_modelo = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_modelo.grid(row=0, column=1)    

tk.Label(frame_entrada, text="Descrição:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, padx=5)
entrada_descricao = tk.Text(frame_entrada, width=40, height=1, font=("Segoe UI", 10))
entrada_descricao.grid(row=0, column=5, rowspan=1, pady=5)

frame_botoes_descricao = tk.Frame(frame_entrada, bg="#f2f2f2")
frame_botoes_descricao.grid(row=5, column=5, pady=(0, 10), sticky="e")

# Lista de serviços disponíveis
servicos_disponiveis = [
    "Manutenção preventiva",
    "Manutenção corretiva",
    "Instalação de equipamento",
    "Configuração de sistema",
    "Treinamento ao cliente"
]

# Variável para armazenar os serviços selecionados
servicos_selecionados = []
campo_servicos_var = tk.StringVar()
campo_valor_total_var = tk.StringVar()

# Label e campo de exibição

tk.Label(frame_entrada, text="Serviços Prestados:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=1, column=4, padx=5)
entry_servicos = tk.Entry(frame_entrada, textvariable=campo_servicos_var, width=50, state="readonly")
entry_servicos.grid(row=1, column=5, padx=(0, 5), pady=5)

btn_servicos = tk.Button(frame_entrada, text="Selecionar", command=abrir_popup_servicos, font=("Segoe UI", 9), bg="#4CAF50", fg="white")
btn_servicos.grid(row=1, column=6, padx=5)

tk.Label(frame_entrada, text="Tipo:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=5)
entrada_tipo = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_tipo.grid(row=0, column=3)

tk.Label(frame_entrada, text="Custo (R$):", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
entrada_custo = tk.Entry(frame_entrada, width=20, font=("Segoe UI", 10))
entrada_custo.grid(row=1, column=1)

tk.Label(frame_entrada, text="Data da Ordem:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
entrada_data_ordem = tk.Entry(frame_entrada, font=("Segoe UI", 10), width=20)
entrada_data_ordem.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_entrada, text="Valor Total (R$):", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, padx=5)
global entrada_valor_total
entrada_valor_total = tk.Entry(frame_entrada, textvariable=campo_valor_total_var, width=20, font=("Segoe UI", 10), state="readonly")
entrada_valor_total.grid(row=1, column=3, padx=5)


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

# Botões de filtro por período
tk.Label(frame_filtro, text="Filtrar por Período (DD/MM/AAAA):", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5)
entrada_inicio = tk.Entry(frame_filtro, width=15, font=("Segoe UI", 10))
entrada_inicio.grid(row=0, column=1)
entrada_fim = tk.Entry(frame_filtro, width=15, font=("Segoe UI", 10))
entrada_fim.grid(row=0, column=2)
tk.Button(frame_filtro, text="Filtrar e Mostrar Resumo", command=filtrar_periodo, width=25, **botao_padrao).grid(row=0, column=3, padx=5)

# Filtro por data específica
tk.Label(frame_filtro, text="Filtrar por Data da Ordem:", bg="#f2f2f2", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)

entrada_data_filtro = DateEntry(frame_filtro, font=("Segoe UI", 10), date_pattern="dd/mm/yyyy", width=15)
entrada_data_filtro.grid(row=1, column=1, padx=5)

btn_filtrar_data = tk.Button(
    frame_filtro,
    text="Filtrar por Dia",
    command=filtrar_por_dia,
    bg="#0275d8",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=20
)
btn_filtrar_data.grid(row=1, column=2, padx=5)

btn_limpar_filtro = tk.Button(
    frame_filtro,
    text="Limpar Filtro",
    command=limpar_filtro,
    bg="#5cb85c",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    width=20
)
btn_limpar_filtro.grid(row=1, column=3, padx=5)

# Tabela
colunas = ("ID", "modelo", "Descriçao", "tipo", "custo", "valor total", "Valor Lucro", "Data Ordem", "Data Entrega", "cliente", "telefone", "servicos")
tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=20)
tabela.tag_configure("atraso", background="#ffcccc")  # vermelho claro para entregas com atraso

for col in colunas:
    tabela.heading(col, text=col)
    if col == "Descrição":
        tabela.column(col, width=100)
    elif col =="Valor Lucro":
        tabela.column(col, width=80)
    elif col == "cliente":
        tabela.column(col, width=100)
    elif col == "telefone":
        tabela.column(col, width=120)
    elif col == "servicos":
        tabela.column(col, width=120)
    else:
        tabela.column(col, width=110)

tabela.pack(expand=True, fill="both", padx=10, pady=10)
tabela.bind("<Double-1>", carregar_para_edicao)

menu_contexto = tk.Menu(janela, tearoff=0)
menu_contexto.add_command(label="Editar", command=carregar_para_edicao)
menu_contexto.add_command(label="Excluir", command=excluir_ordem)

tabela.bind("<Button-3>", mostrar_menu_contexto)  # Botão direito


menu_contexto.add_command(label="Ver Detalhes", command=ver_detalhes)
menu_contexto.add_command(label="Duplicar Ordem", command=duplicar_ordem)

tabela.bind("<Button-3>", mostrar_menu_contexto)

# Iniciar interface
janela.mainloop()


