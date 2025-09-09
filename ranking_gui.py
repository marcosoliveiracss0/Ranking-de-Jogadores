import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- LÓGICA DE BACK-END ---

class Jogador:
    """ Representa um jogador com nome, nível e pontuação. """
    def __init__(self, nome: str, nivel: int, pontuacao: float):
        self.nome = nome
        self.nivel = nivel
        self.pontuacao = pontuacao

    def __repr__(self):
        return f"Jogador(Nome: {self.nome}, Nível: {self.nivel}, Pontuação: {self.pontuacao})"

def registrar_erro(linha_invalida: list, erro: Exception, numero_linha: int):
    """ Registra um erro no arquivo 'erros.log', incluindo o número da linha. """
    with open('erros.log', 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conteudo_linha = ','.join(linha_invalida)
        f.write(f"[{timestamp}] Erro na linha {numero_linha}: '{conteudo_linha}'. Detalhe: {erro}\n")

def carregar_jogadores(caminho_arquivo: str) -> list:
    """ Lê um arquivo CSV e retorna uma lista de objetos Jogador. """
    jogadores = []
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", f"O arquivo '{caminho_arquivo}' não foi encontrado.")
        return jogadores

    # Usando 'latin-1' para maior compatibilidade com arquivos do Excel no Brasil
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        leitor_csv = csv.reader(f)
        try:
            next(leitor_csv)  # Pula o cabeçalho
        except StopIteration:
            return [] # Arquivo vazio

        for numero_linha, linha in enumerate(leitor_csv, start=2):
            if not linha: # Ignora linhas vazias
                continue

            try:
                if len(linha) != 3:
                    raise ValueError("Número incorreto de colunas")
                nome = linha[0].strip()
                if not nome:
                    raise ValueError("O nome não pode ser vazio")
                nivel = int(linha[1])
                pontuacao = float(linha[2])
                jogadores.append(Jogador(nome, nivel, pontuacao))
            except (ValueError, IndexError) as e:
                registrar_erro(linha, e, numero_linha)
    return jogadores


# --- CLASSE DA APLICAÇÃO COM INTERFACE GRÁFICA (GUI) E HISTÓRICO ---

class RankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ranking de Jogadores")
        self.root.geometry("750x550")

        # Dicionário para guardar os rankings carregados
        self.historico_rankings = {}

        # Estilos
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10))

        # --- Layout da Interface ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame superior para os botões
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)

        self.btn_selecionar = ttk.Button(top_frame, text="📂 Carregar Novo Ranking", command=self.carregar_novo_ranking)
        self.btn_selecionar.pack(side=tk.LEFT, padx=(0, 10))

        # Frame para o histórico
        history_frame = ttk.Frame(main_frame)
        history_frame.pack(fill=tk.X, pady=5)
        
        history_label = ttk.Label(history_frame, text="Histórico de Rankings:")
        history_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.combo_historico = ttk.Combobox(history_frame, state="disabled", width=50)
        self.combo_historico.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.combo_historico.bind("<<ComboboxSelected>>", self.mostrar_ranking_selecionado)

        self.btn_ver_log = ttk.Button(top_frame, text="📄 Ver Log de Erros", command=self.ver_log_erros)
        self.btn_ver_log.pack(side=tk.RIGHT)
        
        # Tabela de Ranking
        self.tree = ttk.Treeview(main_frame, columns=("Posicao", "Nome", "Pontuacao", "Nivel"), show="headings")
        self.tree.heading("Posicao", text="Posição")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Pontuacao", text="Pontuação")
        self.tree.heading("Nivel", text="Nível")

        self.tree.column("Posicao", width=60, anchor='center')
        self.tree.column("Nome", width=350)
        self.tree.column("Pontuacao", width=120, anchor='center')
        self.tree.column("Nivel", width=80, anchor='center')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.tree.tag_configure('gold', background='#FFD700', foreground='black')
        self.tree.tag_configure('silver', background='#C0C0C0', foreground='black')
        self.tree.tag_configure('bronze', background='#CD7F32', foreground='white')

    def carregar_novo_ranking(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo de jogadores",
            filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
        )
        if not caminho_arquivo:
            return
        
        if os.path.exists('erros.log'):
            os.remove('erros.log')

        jogadores = carregar_jogadores(caminho_arquivo)

        if jogadores:
            # Adiciona o ranking ao histórico
            timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            nome_arquivo = os.path.basename(caminho_arquivo)
            chave_historico = f"{timestamp} - ({len(jogadores)} jogadores) - {nome_arquivo}"
            self.historico_rankings[chave_historico] = jogadores
            
            # Atualiza o Combobox
            self.combo_historico['values'] = list(self.historico_rankings.keys())
            self.combo_historico.set(chave_historico)
            self.combo_historico.config(state="readonly")

            # Exibe o ranking recém-carregado
            self.atualizar_ranking_view(jogadores)
            messagebox.showinfo("Sucesso", f"{len(jogadores)} jogadores carregados com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum jogador válido foi carregado do arquivo.")

    def mostrar_ranking_selecionado(self, event=None):
        """ Pega a seleção do combobox e atualiza a tabela. """
        chave_selecionada = self.combo_historico.get()
        if chave_selecionada in self.historico_rankings:
            jogadores = self.historico_rankings[chave_selecionada]
            self.atualizar_ranking_view(jogadores)

    def atualizar_ranking_view(self, jogadores):
        for i in self.tree.get_children():
            self.tree.delete(i)

        ranking = sorted(jogadores, key=lambda jogador: jogador.pontuacao, reverse=True)

        for i, jogador in enumerate(ranking):
            posicao = i + 1
            tag = ''
            if posicao == 1: tag = 'gold'
            elif posicao == 2: tag = 'silver'
            elif posicao == 3: tag = 'bronze'
            self.tree.insert("", tk.END, values=(f"{posicao}º", jogador.nome, f"{jogador.pontuacao:.2f}", jogador.nivel), tags=(tag,))

    def ver_log_erros(self):
        log_path = 'erros.log'
        if not os.path.exists(log_path):
            messagebox.showinfo("Log de Erros", "O arquivo 'erros.log' não existe.")
            return

        log_window = tk.Toplevel(self.root)
        log_window.title("Log de Erros")
        log_window.geometry("700x400")
        text_area = tk.Text(log_window, wrap="word", font=('Courier New', 10))
        scrollbar = ttk.Scrollbar(log_window, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        with open(log_path, 'r', encoding='utf-8') as f:
            text_area.insert(tk.END, f.read())
        text_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = RankingApp(root)
    root.mainloop()
