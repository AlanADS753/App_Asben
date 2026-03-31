import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO

class CardUsuario(ctk.CTkFrame):
    def __init__(self, master, usuario, callback):
        super().__init__(master, fg_color="#333333", corner_radius=10)
        self.pack(fill="x", padx=10, pady=5)

    
        self.foto = self.get_img(usuario.get('Foto'))
        self.lbl_foto = ctk.CTkLabel(self, text="", image=self.foto)
        self.lbl_foto.pack(side="left", padx=15, pady=10)
        
        f_info = ctk.CTkFrame(self, fg_color="transparent")
        f_info.pack(side="left", fill="both", expand=True, pady=10)

        ctk.CTkLabel(f_info, text=usuario.get('Nome_completo', 'Sem Nome'), 
                     font=("Arial", 15, "bold"), text_color="white").pack(anchor="w")
        
        ctk.CTkLabel(f_info, text=f"CPF: {usuario.get('CPF', '---')}", 
                     font=("Arial", 12), text_color="#bbbbbb").pack(anchor="w")

        
        self.btn = ctk.CTkButton(self, text="Ver Detalhes", width=100, height=32,
                                 fg_color="#1f6aa5", hover_color="#144870",
                                 command=lambda: callback(usuario))
        self.btn.pack(side="right", padx=15)

    def get_img(self, url):
        size = (55, 55)
        try:
            if url and str(url).lower() != "null":
                r = requests.get(url, timeout=5)
                img = Image.open(BytesIO(r.content))
            else:
            
                img = Image.new('RGB', size, (80, 80, 80))
            
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except:
            
            img = Image.new('RGB', size, (150, 0, 0))
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)