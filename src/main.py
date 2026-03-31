import customtkinter as ctk
from tkinter import filedialog, messagebox
from database import Database
from PIL import Image
import requests
import io
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class JanelaDetalhes(ctk.CTkToplevel):
    def __init__(self, parent, usuario, db, callback_atualizar):
        super().__init__(parent)
        nome_janela = usuario.get('Nome_completo', 'Usuário')
        self.title(f"Editar: {nome_janela}")
        self.geometry("500x750")
        self.db = db
        self.usuario_original = usuario
        self.callback_atualizar = callback_atualizar
        self.nova_foto_local = None
        
      
        self.attributes("-topmost", True)
        self.grab_set()

       
        self.frame_foto = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_foto.pack(pady=20)

        self.img_perfil = self.carregar_foto_atual(usuario.get('Foto'))
        self.lbl_foto = ctk.CTkLabel(self.frame_foto, text="", image=self.img_perfil)
        self.lbl_foto.pack()

        ctk.CTkButton(self.frame_foto, text="Alterar Foto", width=120, 
                      command=self.selecionar_nova_foto).pack(pady=10)

        
        ctk.CTkLabel(self, text="Nome Completo:", text_color="black").pack(padx=50, fill="x")
        self.entry_nome = ctk.CTkEntry(self, width=400)
        self.entry_nome.insert(0, usuario.get('Nome_completo', ''))
        self.entry_nome.pack(pady=5)

        ctk.CTkLabel(self, text="CPF:", text_color="black").pack(padx=50, fill="x")
        self.entry_cpf = ctk.CTkEntry(self, width=400)
        self.entry_cpf.insert(0, str(usuario.get('CPF', '')))
        self.entry_cpf.pack(pady=5)

        ctk.CTkLabel(self, text="Data de Nascimento:", text_color="black").pack(padx=50, fill="x")
        self.entry_data = ctk.CTkEntry(self, width=400)
        self.entry_data.insert(0, str(usuario.get('Data_nascimento', '')))
        self.entry_data.pack(pady=5)

        
        ctk.CTkButton(self, text="SALVAR ALTERAÇÕES", fg_color="green", 
                      command=self.atualizar).pack(pady=20)
        ctk.CTkButton(self, text="EXCLUIR REGISTRO", fg_color="red", 
                      command=self.excluir).pack()

    def carregar_foto_atual(self, url):
        size = (150, 150)
        try:
            if url and str(url).lower() != "null":
                r = requests.get(url, timeout=5)
                img = Image.open(io.BytesIO(r.content))
            else:
                img = Image.new('RGB', size, (220, 220, 220))
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except:
            img = Image.new('RGB', size, (220, 220, 220))
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    def selecionar_nova_foto(self):
        caminho = filedialog.askopenfilename()
        if caminho:
            self.nova_foto_local = caminho
            img_nova = Image.open(caminho)
            self.lbl_foto.configure(image=ctk.CTkImage(img_nova, size=(150, 150)))

    def atualizar(self):
        dados = {
            "Nome_completo": self.entry_nome.get(),
            "CPF": self.entry_cpf.get(),
            "Data_nascimento": self.entry_data.get(),
            "Foto": self.nova_foto_local if self.nova_foto_local else self.usuario_original.get('Foto')
        }
        sucesso, msg = self.db.atualizar_usuario(self.usuario_original['CPF'], dados)
        if sucesso:
            messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
            self.callback_atualizar() 
            self.destroy()            
        else:
            messagebox.showerror("Erro", msg)

    def excluir(self):
        if messagebox.askyesno("Confirmar", "Deseja excluir permanentemente?"):
            sucesso, msg = self.db.deletar_usuario(self.usuario_original['CPF'])
            if sucesso:
                self.callback_atualizar()
                self.destroy() 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Asben - Gestão de Beneficiários")
        self.geometry("800x850")
        self.configure(fg_color="white")
        
        self.db = Database()
        self.caminho_foto_local = None

        self.tabs = ctk.CTkTabview(self, fg_color="white")
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab_cadastro = self.tabs.add("Novo Cadastro")
        self.tab_lista = self.tabs.add("Consultar Pessoas")

        self.setup_cadastro()
        self.setup_lista()

    def setup_cadastro(self):
        ctk.CTkLabel(self.tab_cadastro, text="Cadastro de Beneficiário", 
                      font=("Arial", 22, "bold"), text_color="black").pack(pady=20)
        
        self.en_nome = ctk.CTkEntry(self.tab_cadastro, placeholder_text="Nome Completo", width=400)
        self.en_nome.pack(pady=10)
        
        self.en_cpf = ctk.CTkEntry(self.tab_cadastro, placeholder_text="CPF (apenas números)", width=400)
        self.en_cpf.pack(pady=10)
        
        self.en_data = ctk.CTkEntry(self.tab_cadastro, placeholder_text="Data de Nascimento (DD/MM/AAAA)", width=400)
        self.en_data.pack(pady=10)
        
        ctk.CTkButton(self.tab_cadastro, text="Selecionar Foto", command=self.escolher_foto).pack(pady=10)
        self.lb_foto_status = ctk.CTkLabel(self.tab_cadastro, text="Nenhuma foto selecionada", text_color="gray")
        self.lb_status = self.lb_foto_status
        self.lb_status.pack()
        
        
        ctk.CTkButton(self.tab_cadastro, text="SALVAR", fg_color="green", 
                      command=self.salvar).pack(pady=30)

    def escolher_foto(self):
        caminho = filedialog.askopenfilename()
        if caminho:
            self.caminho_foto_local = caminho
            self.lb_status.configure(text="✔ Foto selecionada", text_color="green")

    def salvar(self):
        res, msg = self.db.cadastrar_com_foto(self.en_nome.get(), self.en_cpf.get(), 
                                              self.en_data.get(), self.caminho_foto_local)
        if res:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", msg)

    def limpar_campos(self):
        self.en_nome.delete(0, 'end'); self.en_cpf.delete(0, 'end'); self.en_data.delete(0, 'end')
        self.caminho_foto_local = None
        self.lb_status.configure(text="Nenhuma foto selecionada", text_color="gray")

    def setup_lista(self):
        self.en_busca = ctk.CTkEntry(self.tab_lista, placeholder_text="Filtrar por Nome ou CPF...", width=500)
        self.en_busca.pack(pady=20)
        self.en_busca.bind("<KeyRelease>", lambda e: self.atualizar_lista(self.en_busca.get().lower()))
        
        self.scroll = ctk.CTkScrollableFrame(self.tab_lista, fg_color="#F2F2F2")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.atualizar_lista()

    def _obter_foto_mini(self, url):
        size = (60, 60)
        try:
            if url and str(url).lower() != "null":
                r = requests.get(url, timeout=2)
                img = Image.open(io.BytesIO(r.content))
            else:
                img = Image.new('RGB', size, (200, 200, 200))
            return ctk.CTkImage(img, size=size)
        except:
            return ctk.CTkImage(Image.new('RGB', size, (200, 200, 200)), size=size)

    def atualizar_lista(self, filtro=""):
        for child in self.scroll.winfo_children(): child.destroy()
        
        usuarios = self.db.listar_usuarios()
        for u in usuarios:
            if filtro in u['Nome_completo'].lower() or filtro in str(u['CPF']):
                card = ctk.CTkFrame(self.scroll, fg_color="white", border_width=1, border_color="#DDD")
                card.pack(fill="x", padx=10, pady=5)
                
                lbl_img = ctk.CTkLabel(card, text="", image=self._obter_foto_mini(u.get('Foto')))
                lbl_img.pack(side="left", padx=10, pady=5)
                
                txt = f"{u['Nome_completo']}\nCPF: {u['CPF']} | Nasc: {u['Data_nascimento']}"
                ctk.CTkLabel(card, text=txt, justify="left", text_color="black").pack(side="left", padx=10)
                
                ctk.CTkButton(card, text="Editar", width=80, 
                              command=lambda user=u: JanelaDetalhes(self, user, self.db, self.atualizar_lista)).pack(side="right", padx=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
