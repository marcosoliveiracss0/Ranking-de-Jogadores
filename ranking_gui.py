import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- LÓGICA DE BACK-END (COM A CORREÇÃO FINAL) ---

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

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        leitor_csv = csv.reader(f)
        try:
            next(leitor_csv)  # Pula o cabeçalho (linha 1)
        except StopIteration:
            return jogadores # Arquivo vazio

        for numero_linha, linha in enumerate(leitor_csv, start=2):
            # ADICIONADO: Se a linha estiver vazia, pule para a próxima.
            if not linha:
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


# --- CLASSE DA APLICAÇÃO COM INTERFACE GRÁFICA (GUI) ---
# Nenhuma alteração necessária aqui
class RankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ranking de Jogadores")
        self.root.geometry("650x500")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10))

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)

        self.btn_selecionar = ttk.Button(top_frame, text="📂 Selecionar Arquivo CSV", command=self.selecionar_e_exibir_ranking)
        self.btn_selecionar.pack(side=tk.LEFT, padx=5)

        self.btn_ver_log = ttk.Button(top_frame, text="📄 Ver Log de Erros", command=self.ver_log_erros)
        self.btn_ver_log.pack(side=tk.RIGHT, padx=5)

        self.tree = ttk.Treeview(main_frame, columns=("Posicao", "Nome", "Pontuacao", "Nivel"), show="headings")
        self.tree.heading("Posicao", text="Posição")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Pontuacao", text="Pontuação")
        self.tree.heading("Nivel", text="Nível")

        self.tree.column("Posicao", width=60, anchor='center')
        self.tree.column("Nome", width=250)
        self.tree.column("Pontuacao", width=120, anchor='center')
        self.tree.column("Nivel", width=80, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree.tag_configure('gold', background='#FFD700', foreground='black')
        self.tree.tag_configure('silver', background='#C0C0C0', foreground='black')
        self.tree.tag_configure('bronze', background='#CD7F32', foreground='white')

    def selecionar_e_exibir_ranking(self):
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
             messagebox.showinfo("Sucesso", f"{len(jogadores)} jogadores carregados com sucesso!\nVerifique 'erros.log' para possíveis linhas inválidas.")
        else:
            messagebox.showwarning("Aviso", "Nenhum jogador válido foi carregado do arquivo.")

        self.atualizar_ranking_view(jogadores)

    def atualizar_ranking_view(self, jogadores):
        for i in self.tree.get_children():
            self.tree.delete(i)

        ranking = sorted(jogadores, key=lambda jogador: jogador.pontuacao, reverse=True)

        for i, jogador in enumerate(ranking):
            posicao = i + 1
            tag = ''
            if posicao == 1:
                tag = 'gold'
            elif posicao == 2:
                tag = 'silver'
            elif posicao == 3:
                tag = 'bronze'
            self.tree.insert("", tk.END, values=(f"{posicao}º", jogador.nome, f"{jogador.pontuacao:.2f}", jogador.nivel), tags=(tag,))

    def ver_log_erros(self):
        log_path = 'erros.log'
        if not os.path.exists(log_path):
            messagebox.showinfo("Log de Erros", "O arquivo 'erros.log' não existe. Nenhum erro foi registrado ainda.")
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


# --- PONTO DE ENTRADA DA APLICAÇÃO ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RankingApp(root)
    root.mainloop()