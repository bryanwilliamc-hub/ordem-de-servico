import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

class SistemaOrdemServico:
    def __init__(self, root):
        self.root = root
        self.ordens = []
        self.arquivo_dados = "ordens_servico.json"
        
        self.configurar_tema()
        self.carregar_dados()
        self.configurar_interface()
        self.atualizar_treeview()
        self.atualizar_totais()

    def configurar_tema(self):
        """Configura cores e estilos modernos"""
        self.root.configure(bg='#2c3e50')
        
        # Configurar estilo moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores do tema
        self.cor_primaria = '#3498db'
        self.cor_secundaria = '#2c3e50'
        self.cor_sucesso = '#27ae60'
        self.cor_perigo = '#e74c3c'
        self.cor_alerta = '#f39c12'
        self.cor_fundo = '#ecf0f1'
        self.cor_texto = '#2c3e50'
        
        # Configurar estilos
        self.style.configure('TFrame', background=self.cor_fundo)
        self.style.configure('TLabel', background=self.cor_fundo, foreground=self.cor_texto)
        self.style.configure('TButton', font=('Arial', 10))
        
        # Estilos personalizados
        self.style.configure('Title.TLabel', 
                           font=('Arial', 18, 'bold'), 
                           foreground=self.cor_primaria,
                           background=self.cor_fundo)
        
        self.style.configure('Card.TFrame', 
                           background='white', 
                           relief='raised', 
                           borderwidth=1)
        
        self.style.configure('Primary.TButton',
                           font=('Arial', 10, 'bold'),
                           background=self.cor_primaria,
                           foreground='white')
        
        self.style.configure('Success.TButton',
                           background=self.cor_sucesso,
                           foreground='white')
        
        self.style.configure('Danger.TButton',
                           background=self.cor_perigo,
                           foreground='white')

    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    self.ordens = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.ordens = []
                self.salvar_dados()
        else:
            self.ordens = []

    def salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(self.ordens, f, ensure_ascii=False, indent=2)

    def configurar_interface(self):
        """Configura a interface gráfica moderna"""
        self.root.title("🚀 Protech OS - Sistema de Ordens de Serviço")
        self.root.geometry("1300x800")
        self.root.minsize(1200, 700)
        
        # Frame principal com cor de fundo
        main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        main_frame.pack(fill='both', expand=True)
        
        # Cabeçalho moderno
        self.criar_cabecalho(main_frame)
        
        # Cartões de estatísticas
        self.criar_cartoes_estatisticas(main_frame)
        
        # Área principal
        self.criar_area_principal(main_frame)

    def criar_cabecalho(self, parent):
        """Cria o cabeçalho moderno"""
        header_frame = ttk.Frame(parent, style='TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo e título
        title_frame = ttk.Frame(header_frame, style='TFrame')
        title_frame.pack(side='left')
        
        titulo = ttk.Label(title_frame, 
                          text="🔧 Protech OS", 
                          style='Title.TLabel')
        titulo.pack(anchor='w')
        
        subtitulo = ttk.Label(title_frame, 
                             text="Sistema Profissional de Ordens de Serviço",
                             font=('Arial', 11),
                             foreground='#7f8c8d',
                             background=self.cor_fundo)
        subtitulo.pack(anchor='w')
        
        # Botões do cabeçalho
        btn_frame = ttk.Frame(header_frame, style='TFrame')
        btn_frame.pack(side='right')
        
        botoes_header = [
            ("📊 Dashboard", self.mostrar_dashboard),
            ("⚙️ Configurações", self.mostrar_configuracoes)
        ]
        
        for texto, comando in botoes_header:
            ttk.Button(btn_frame, text=texto, command=comando).pack(side='left', padx=5)

    def criar_cartoes_estatisticas(self, parent):
        """Cria cartões com estatísticas"""
        cards_frame = ttk.Frame(parent, style='TFrame')
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Cartão 1 - Total de Ordens
        card1 = ttk.Frame(cards_frame, style='Card.TFrame', padding="15")
        card1.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        ttk.Label(card1, text="📋 Total de Ordens", 
                 font=('Arial', 12, 'bold'),
                 foreground=self.cor_primaria,
                 background='white').pack(anchor='w')
        
        self.label_total_card = ttk.Label(card1, text="0",
                                        font=('Arial', 24, 'bold'),
                                        foreground=self.cor_texto,
                                        background='white')
        self.label_total_card.pack(anchor='w')
        
        ttk.Label(card1, text="Ordens cadastradas",
                 font=('Arial', 9),
                 foreground='#7f8c8d',
                 background='white').pack(anchor='w')
        
        # Cartão 2 - Valor Total
        card2 = ttk.Frame(cards_frame, style='Card.TFrame', padding="15")
        card2.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        ttk.Label(card2, text="💰 Valor Total", 
                 font=('Arial', 12, 'bold'),
                 foreground=self.cor_sucesso,
                 background='white').pack(anchor='w')
        
        self.label_valor_card = ttk.Label(card2, text="R$ 0,00",
                                        font=('Arial', 24, 'bold'),
                                        foreground=self.cor_texto,
                                        background='white')
        self.label_valor_card.pack(anchor='w')
        
        ttk.Label(card2, text="Em ordens ativas",
                 font=('Arial', 9),
                 foreground='#7f8c8d',
                 background='white').pack(anchor='w')
        
        # Cartão 3 - Ordens Pendentes
        card3 = ttk.Frame(cards_frame, style='Card.TFrame', padding="15")
        card3.pack(side='left', fill='x', expand=True)
        
        ttk.Label(card3, text="⏳ Pendentes", 
                 font=('Arial', 12, 'bold'),
                 foreground=self.cor_alerta,
                 background='white').pack(anchor='w')
        
        self.label_pendentes_card = ttk.Label(card3, text="0",
                                            font=('Arial', 24, 'bold'),
                                            foreground=self.cor_texto,
                                            background='white')
        self.label_pendentes_card.pack(anchor='w')
        
        ttk.Label(card3, text="Aguardando conclusão",
                 font=('Arial', 9),
                 foreground='#7f8c8d',
                 background='white').pack(anchor='w')

    def criar_area_principal(self, parent):
        """Cria a área principal com tabela e controles"""
        # Frame principal
        main_content = ttk.Frame(parent, style='Card.TFrame', padding="15")
        main_content.pack(fill='both', expand=True)
        
        # Barra de ferramentas
        self.criar_barra_ferramentas(main_content)
        
        # Tabela
        self.criar_tabela(main_content)
        
        # Barra de status
        self.criar_barra_status(main_content)

    def criar_barra_ferramentas(self, parent):
        """Cria a barra de ferramentas moderna"""
        toolbar = ttk.Frame(parent, style='Card.TFrame')
        toolbar.pack(fill='x', pady=(0, 15))
        
        # Lado esquerdo - Busca e filtros
        left_toolbar = ttk.Frame(toolbar, style='Card.TFrame')
        left_toolbar.pack(side='left')
        
        # Campo de busca
        search_frame = ttk.Frame(left_toolbar, style='Card.TFrame')
        search_frame.pack(side='left', padx=(0, 15))
        
        ttk.Label(search_frame, text="🔍 Buscar:", 
                 background='white').pack(side='left')
        
        self.combo_tipo_busca = ttk.Combobox(search_frame, 
                                           values=["Cliente", "Equipamento", "Status", "Todos"],
                                           state="readonly", 
                                           width=12,
                                           height=4)
        self.combo_tipo_busca.set("Todos")
        self.combo_tipo_busca.pack(side='left', padx=5)
        
        self.entry_busca = ttk.Entry(search_frame, width=25, font=('Arial', 10))
        self.entry_busca.pack(side='left', padx=5)
        self.entry_busca.bind('<KeyRelease>', self.filtrar_ordens)
        
        # Botão limpar busca
        ttk.Button(search_frame, text="Limpar", 
                  command=self.limpar_busca,
                  width=8).pack(side='left', padx=5)
        
        # Filtro de status
        filter_frame = ttk.Frame(left_toolbar, style='Card.TFrame')
        filter_frame.pack(side='left')
        
        ttk.Label(filter_frame, text="📊 Status:", 
                 background='white').pack(side='left')
        
        self.combo_filtro_status = ttk.Combobox(filter_frame, 
                                              values=["Todos", "Aguardando Orçamento", "Em Andamento", "Concluído", "Entregue"],
                                              state="readonly", 
                                              width=18)
        self.combo_filtro_status.set("Todos")
        self.combo_filtro_status.bind('<<ComboboxSelected>>', self.filtrar_por_status)
        self.combo_filtro_status.pack(side='left', padx=5)
        
        # Lado direito - Botões de ação
        right_toolbar = ttk.Frame(toolbar, style='Card.TFrame')
        right_toolbar.pack(side='right')
        
        botoes_acao = [
            ("➕ Nova OS", self.criar_ordem_servico, 'Primary.TButton'),
            ("📈 Relatório", self.gerar_relatorio, 'TButton'),
            ("🔄 Atualizar", self.atualizar_interface, 'TButton'),
            ("📤 Exportar", self.exportar_dados, 'TButton')
        ]
        
        for texto, comando, estilo in botoes_acao:
            ttk.Button(right_toolbar, text=texto, 
                      command=comando,
                      style=estilo).pack(side='left', padx=3)

    def criar_tabela(self, parent):
        """Cria a tabela moderna"""
        table_frame = ttk.Frame(parent, style='Card.TFrame')
        table_frame.pack(fill='both', expand=True)
        
        # Treeview com estilo moderno
        colunas = ('ID', 'Data', 'Cliente', 'Equipamento', 'Modelo', 'Status', 'Valor')
        
        # Frame para treeview e scrollbars
        tree_container = ttk.Frame(table_frame)
        tree_container.pack(fill='both', expand=True)
        
        # Treeview
        self.tree = ttk.Treeview(tree_container, columns=colunas, show='headings', height=15)
        
        # Configurar colunas com cores
        for col in colunas:
            self.tree.heading(col, text=col, anchor='center')
            if col == 'ID':
                self.tree.column(col, width=70, anchor='center')
            elif col == 'Valor':
                self.tree.column(col, width=100, anchor='center')
            elif col == 'Data':
                self.tree.column(col, width=90, anchor='center')
            elif col == 'Status':
                self.tree.column(col, width=130, anchor='center')
            else:
                self.tree.column(col, width=150, anchor='w')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Bind eventos
        self.tree.bind('<Double-1>', self.editar_ordem_duplo_clique)
        self.tree.bind('<Delete>', self.excluir_ordem_selecionada)
        self.tree.bind('<<TreeviewSelect>>', self.on_selecionar_ordem)
        
        # Configurar tags para cores de status
        self.tree.tag_configure('pendente', background='#fff3cd')
        self.tree.tag_configure('andamento', background='#d1ecf1')
        self.tree.tag_configure('concluido', background='#d4edda')
        self.tree.tag_configure('entregue', background='#e2e3e5')

    def criar_barra_status(self, parent):
        """Cria a barra de status"""
        status_bar = ttk.Frame(parent, style='Card.TFrame')
        status_bar.pack(fill='x', pady=(15, 0))
        
        self.label_status = ttk.Label(status_bar, 
                                     text="✅ Sistema carregado com sucesso | 0 ordens carregadas",
                                     font=('Arial', 9),
                                     foreground='#7f8c8d',
                                     background='white')
        self.label_status.pack(side='left')
        
        self.label_ultima_atualizacao = ttk.Label(status_bar,
                                                 text=f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                                                 font=('Arial', 9),
                                                 foreground='#7f8c8d',
                                                 background='white')
        self.label_ultima_atualizacao.pack(side='right')

    def atualizar_treeview(self):
        """Atualiza a treeview com os dados atuais"""
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar novos dados com cores por status
        for ordem in self.ordens:
            valores = (
                ordem['id'],
                ordem['data_entrada'],
                ordem['cliente'],
                ordem['equipamento'],
                ordem.get('modelo', ''),
                ordem['status'],
                f"R$ {ordem['valor']:,.2f}"
            )
            
            # Definir tag baseada no status
            tag = ''
            if 'Aguardando' in ordem['status']:
                tag = 'pendente'
            elif 'Andamento' in ordem['status']:
                tag = 'andamento'
            elif 'Concluído' in ordem['status']:
                tag = 'concluido'
            elif 'Entregue' in ordem['status']:
                tag = 'entregue'
            
            self.tree.insert('', 'end', values=valores, tags=(tag,))

    def atualizar_totais(self):
        """Atualiza todos os totais e estatísticas"""
        total_ordens = len(self.ordens)
        valor_total = sum(ordem['valor'] for ordem in self.ordens)
        ordens_pendentes = len([o for o in self.ordens if 'Aguardando' in o['status'] or 'Andamento' in o['status']])
        
        # Atualizar cartões
        self.label_total_card.config(text=str(total_ordens))
        self.label_valor_card.config(text=f"R$ {valor_total:,.2f}")
        self.label_pendentes_card.config(text=str(ordens_pendentes))
        
        # Atualizar barra de status
        self.label_status.config(text=f"✅ Sistema carregado com sucesso | {total_ordens} ordens carregadas")

    def atualizar_interface(self):
        """Atualiza toda a interface"""
        self.atualizar_treeview()
        self.atualizar_totais()
        self.label_ultima_atualizacao.config(text=f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        messagebox.showinfo("Atualizado", "Interface atualizada com sucesso!")

    def on_selecionar_ordem(self, event):
        """Quando uma ordem é selecionada na tabela"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            ordem_id = self.tree.item(item)['values'][0]
            # Aqui você pode adicionar funcionalidades extras quando seleciona uma ordem

    def filtrar_ordens(self, event=None):
        """Filtra as ordens baseado no termo de busca"""
        termo = self.entry_busca.get().lower()
        tipo_busca = self.combo_tipo_busca.get().lower()
        
        if not termo:
            self.atualizar_treeview()
            return
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtrar e adicionar ordens que correspondem
        for ordem in self.ordens:
            match = False
            
            if tipo_busca == "todos" or tipo_busca == "todas":
                # Busca em todos os campos
                campos_busca = [
                    str(ordem['id']),
                    ordem['cliente'].lower(),
                    ordem['equipamento'].lower(),
                    ordem.get('modelo', '').lower(),
                    ordem['status'].lower()
                ]
                match = any(termo in campo for campo in campos_busca)
            elif tipo_busca == "cliente" and termo in ordem['cliente'].lower():
                match = True
            elif tipo_busca == "equipamento" and termo in ordem['equipamento'].lower():
                match = True
            elif tipo_busca == "status" and termo in ordem['status'].lower():
                match = True
            
            if match:
                self.adicionar_ordem_treeview(ordem)

    def filtrar_por_status(self, event=None):
        """Filtra as ordens por status"""
        status_selecionado = self.combo_filtro_status.get()
        
        if status_selecionado == "Todos":
            self.atualizar_treeview()
            return
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtrar por status
        for ordem in self.ordens:
            if status_selecionado in ordem['status']:
                self.adicionar_ordem_treeview(ordem)

    def adicionar_ordem_treeview(self, ordem):
        """Adiciona uma ordem específica na treeview"""
        valores = (
            ordem['id'],
            ordem['data_entrada'],
            ordem['cliente'],
            ordem['equipamento'],
            ordem.get('modelo', ''),
            ordem['status'],
            f"R$ {ordem['valor']:,.2f}"
        )
        
        # Definir tag baseada no status
        tag = ''
        if 'Aguardando' in ordem['status']:
            tag = 'pendente'
        elif 'Andamento' in ordem['status']:
            tag = 'andamento'
        elif 'Concluído' in ordem['status']:
            tag = 'concluido'
        elif 'Entregue' in ordem['status']:
            tag = 'entregue'
        
        self.tree.insert('', 'end', values=valores, tags=(tag,))

    def limpar_busca(self):
        """Limpa a busca e mostra todas as ordens"""
        self.entry_busca.delete(0, tk.END)
        self.combo_filtro_status.set("Todos")
        self.atualizar_treeview()

    def gerar_proximo_id(self):
        """Gera o próximo ID disponível"""
        if not self.ordens:
            return 1
        return max(ordem['id'] for ordem in self.ordens) + 1

    def criar_ordem_servico(self):
        """Abre o formulário para criar nova ordem de serviço"""
        self.formulario_ordem_servico()

    def editar_ordem_duplo_clique(self, event):
        """Abre edição ao dar duplo clique na ordem"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            ordem_id = int(self.tree.item(item)['values'][0])
            self.formulario_ordem_servico(ordem_id)

    def excluir_ordem_selecionada(self, event):
        """Exclui a ordem selecionada com tecla Delete"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            ordem_id = int(self.tree.item(item)['values'][0])
            self.excluir_ordem(ordem_id)

    def validar_dados_ordem(self, dados):
        """Valida os dados da ordem antes de salvar"""
        erros = []
        
        if not dados['cliente'].strip():
            erros.append("Nome do cliente é obrigatório")
        
        if not dados['equipamento'].strip():
            erros.append("Equipamento é obrigatório")
        
        if not dados['defeito'].strip():
            erros.append("Defeito relatado é obrigatório")
        
        if not dados['servico'].strip():
            erros.append("Serviço a realizar é obrigatório")
        
        try:
            valor = float(dados['valor'])
            if valor < 0:
                erros.append("Valor não pode ser negativo")
        except ValueError:
            erros.append("Valor deve ser um número")
        
        return erros

    def formulario_ordem_servico(self, ordem_id=None):
        """Formulário moderno para criar/editar ordem de serviço"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📝 Editar OS" if ordem_id else "➕ Nova Ordem de Serviço")
        dialog.geometry("700x750")
        dialog.configure(bg=self.cor_fundo)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Aplicar tema ao dialog
        for style in ['.', 'TFrame', 'TLabel', 'TButton', 'TEntry', 'TCombobox']:
            dialog.option_add(f'*{style}*Background', self.cor_fundo)
            dialog.option_add(f'*{style}*Foreground', self.cor_texto)

    def mostrar_dashboard(self):
        """Mostra dashboard de estatísticas"""
        messagebox.showinfo("Dashboard", "📈 Dashboard em desenvolvimento!")

    def mostrar_configuracoes(self):
        """Mostra tela de configurações"""
        messagebox.showinfo("Configurações", "⚙️ Configurações em desenvolvimento!")

    def exportar_dados(self):
        """Exporta dados para CSV"""
        messagebox.showinfo("Exportar", "📤 Funcionalidade de exportação em desenvolvimento!")
        
        # Dados da ordem existente (se edição)
        ordem_existente = None
        if ordem_id:
            ordem_existente = next((o for o in self.ordens if o['id'] == ordem_id), None)
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # Campos do formulário
        campos = []
        
        # Cliente
        ttk.Label(main_frame, text="Cliente:*").grid(row=0, column=0, sticky='w', pady=5)
        entry_cliente = ttk.Entry(main_frame, width=40)
        entry_cliente.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        campos.append(('cliente', entry_cliente))
        
        # Telefone
        ttk.Label(main_frame, text="Telefone:*").grid(row=1, column=0, sticky='w', pady=5)
        entry_telefone = ttk.Entry(main_frame, width=20)
        entry_telefone.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        campos.append(('telefone', entry_telefone))
        
        # Equipamento
        ttk.Label(main_frame, text="Equipamento:*").grid(row=2, column=0, sticky='w', pady=5)
        entry_equipamento = ttk.Entry(main_frame, width=40)
        entry_equipamento.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        campos.append(('equipamento', entry_equipamento))
        
        # Modelo
        ttk.Label(main_frame, text="Modelo:").grid(row=3, column=0, sticky='w', pady=5)
        entry_modelo = ttk.Entry(main_frame, width=30)
        entry_modelo.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        campos.append(('modelo', entry_modelo))
        
        # Número de Série
        ttk.Label(main_frame, text="Nº Série:").grid(row=4, column=0, sticky='w', pady=5)
        entry_serie = ttk.Entry(main_frame, width=20)
        entry_serie.grid(row=4, column=1, sticky='w', pady=5, padx=5)
        campos.append(('numero_serie', entry_serie))
        
        # Defeito Relatado
        ttk.Label(main_frame, text="Defeito Relatado:*").grid(row=5, column=0, sticky='nw', pady=5)
        text_defeito = scrolledtext.ScrolledText(main_frame, width=40, height=4)
        text_defeito.grid(row=5, column=1, sticky='ew', pady=5, padx=5)
        campos.append(('defeito', text_defeito))
        
        # Serviço a Realizar
        ttk.Label(main_frame, text="Serviço a Realizar:*").grid(row=6, column=0, sticky='nw', pady=5)
        text_servico = scrolledtext.ScrolledText(main_frame, width=40, height=4)
        text_servico.grid(row=6, column=1, sticky='ew', pady=5, padx=5)
        campos.append(('servico', text_servico))
        
        # Observações
        ttk.Label(main_frame, text="Observações:").grid(row=7, column=0, sticky='nw', pady=5)
        text_obs = scrolledtext.ScrolledText(main_frame, width=40, height=3)
        text_obs.grid(row=7, column=1, sticky='ew', pady=5, padx=5)
        campos.append(('observacoes', text_obs))
        
        # Valor
        ttk.Label(main_frame, text="Valor (R$):").grid(row=8, column=0, sticky='w', pady=5)
        entry_valor = ttk.Entry(main_frame, width=15)
        entry_valor.grid(row=8, column=1, sticky='w', pady=5, padx=5)
        campos.append(('valor', entry_valor))
        
        # Status
        ttk.Label(main_frame, text="Status:*").grid(row=9, column=0, sticky='w', pady=5)
        combo_status = ttk.Combobox(main_frame, values=[
            "Aguardando Orçamento", "Orçamento Aprovado", "Em Andamento", 
            "Aguardando Peças", "Concluído", "Entregue", "Cancelado"
        ], state="readonly", width=20)
        combo_status.grid(row=9, column=1, sticky='w', pady=5, padx=5)
        combo_status.set("Aguardando Orçamento")
        campos.append(('status', combo_status))
        
        # Preencher dados se for edição
        if ordem_existente:
            entry_cliente.insert(0, ordem_existente['cliente'])
            entry_telefone.insert(0, ordem_existente.get('telefone', ''))
            entry_equipamento.insert(0, ordem_existente['equipamento'])
            entry_modelo.insert(0, ordem_existente.get('modelo', ''))
            entry_serie.insert(0, ordem_existente.get('numero_serie', ''))
            text_defeito.insert('1.0', ordem_existente['defeito'])
            text_servico.insert('1.0', ordem_existente['servico'])
            text_obs.insert('1.0', ordem_existente.get('observacoes', ''))
            entry_valor.insert(0, str(ordem_existente['valor']))
            combo_status.set(ordem_existente['status'])
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        def salvar():
            # Coletar dados
            dados = {}
            for campo, widget in campos:
                if isinstance(widget, (ttk.Entry, ttk.Combobox)):
                    dados[campo] = widget.get()
                elif isinstance(widget, scrolledtext.ScrolledText):
                    dados[campo] = widget.get('1.0', 'end-1c')
            
            # Validar
            erros = self.validar_dados_ordem(dados)
            if erros:
                messagebox.showerror("Erro de Validação", "\n".join(erros))
                return
            
            # Converter valor
            try:
                dados['valor'] = float(dados['valor'] or 0)
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido")
                return
            
            # Salvar ordem
            if ordem_id:
                # Atualizar ordem existente
                for i, ordem in enumerate(self.ordens):
                    if ordem['id'] == ordem_id:
                        dados['id'] = ordem_id
                        dados['data_entrada'] = ordem_existente['data_entrada']
                        self.ordens[i] = dados
                        break
            else:
                # Nova ordem
                nova_ordem = {
                    'id': self.gerar_proximo_id(),
                    'data_entrada': datetime.now().strftime("%d/%m/%Y"),
                    **dados
                }
                self.ordens.append(nova_ordem)
            
            self.salvar_dados()
            self.atualizar_interface()
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Ordem salva com sucesso!")
        
        def excluir():
            if ordem_id and messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta ordem?"):
                self.ordens = [o for o in self.ordens if o['id'] != ordem_id]
                self.salvar_dados()
                self.atualizar_interface()
                dialog.destroy()
                messagebox.showinfo("Sucesso", "Ordem excluída com sucesso!")
        
        ttk.Button(btn_frame, text="💾 Salvar", 
                  command=salvar, style='Accent.TButton').pack(side='left', padx=5)
        
        if ordem_id:
            ttk.Button(btn_frame, text="🗑️ Excluir", 
                      command=excluir).pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="❌ Cancelar", 
                  command=dialog.destroy).pack(side='left', padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)

    def excluir_ordem(self, ordem_id):
        """Exclui uma ordem específica"""
        ordem = next((o for o in self.ordens if o['id'] == ordem_id), None)
        if not ordem:
            messagebox.showerror("Erro", "Ordem não encontrada")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", 
                              f"Tem certeza que deseja excluir a OS {ordem_id} - {ordem['cliente']}?"):
            self.ordens = [o for o in self.ordens if o['id'] != ordem_id]
            self.salvar_dados()
            self.atualizar_interface()
            messagebox.showinfo("Sucesso", "Ordem excluída com sucesso!")

    def gerar_relatorio(self):
        """Gera um relatório simples das ordens"""
        if not self.ordens:
            messagebox.showinfo("Relatório", "Nenhuma ordem para gerar relatório")
            return
        
        ordens_ativas = [o for o in self.ordens if o['status'] != 'Entregue']
        valor_total = sum(o['valor'] for o in ordens_ativas)
        
        relatorio = f"""
RELATÓRIO DE ORDENS DE SERVIÇO
===============================
Total de Ordens: {len(self.ordens)}
Ordems Ativas: {len(ordens_ativas)}
Valor Total em Aberto: R$ {valor_total:,.2f}

Status das Ordens:
"""
        # Contar por status
        status_count = {}
        for ordem in self.ordens:
            status = ordem['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        for status, count in status_count.items():
            relatorio += f"- {status}: {count} ordens\n"
        
        messagebox.showinfo("Relatório do Sistema", relatorio)

def main():
    root = tk.Tk()
    app = SistemaOrdemServico(root)
    root.mainloop()

if __name__ == "__main__":
    main()
