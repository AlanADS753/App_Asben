import os
import io
from supabase import create_client
from dotenv import load_dotenv
from PIL import Image


load_dotenv()

class Database:
    def __init__(self):
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise Exception("Erro: SUPABASE_URL ou SUPABASE_KEY não encontradas no arquivo .env")
            
        self.supabase = create_client(url, key)

    def _otimizar_imagem(self, caminho_local):
       
        img = Image.open(caminho_local)
        
   
        img.thumbnail((800, 800))
        
    
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        buffer = io.BytesIO()
   
        img.save(buffer, format="JPEG", quality=70, optimize=True)
        buffer.seek(0)
        return buffer

    def cadastrar_com_foto(self, nome, cpf, data_nasc, caminho_foto_local):
        try:
            foto_url = "NULL"
            
            if caminho_foto_local and os.path.exists(caminho_foto_local):
                nome_arquivo = f"perfil_{cpf}.jpg"
                
              
                imagem_otimizada = self._otimizar_imagem(caminho_foto_local)
                
           
                self.supabase.storage.from_("fotos_perfil").upload(
                    path=nome_arquivo, 
                    file=imagem_otimizada.read(), 
                    file_options={"content-type": "image/jpeg", "upsert": "true"}
                )
                
          
                res_url = self.supabase.storage.from_("fotos_perfil").get_public_url(nome_arquivo)
                foto_url = res_url
            
            dados = {
                "Nome_completo": nome,
                "CPF": cpf,
                "Data_nascimento": data_nasc,
                "Foto": foto_url
            }
            
            self.supabase.table("Pessoa").insert(dados).execute()
            return True, "Cadastrado com sucesso e imagem otimizada!"
            
        except Exception as e:
            return False, f"Erro no cadastro: {str(e)}"

    def listar_usuarios(self):
        try:
           
            res = self.supabase.table("Pessoa").select("*").order("Nome_completo").execute()
            return res.data
        except:
            return []

    def atualizar_usuario(self, cpf_original, dados_novos):
       
        try:
            
            if "Foto" in dados_novos and os.path.exists(str(dados_novos["Foto"])):
                nome_arquivo = f"perfil_{dados_novos['CPF']}.jpg"
                imagem_otimizada = self._otimizar_imagem(dados_novos["Foto"])
                
                self.supabase.storage.from_("fotos_perfil").upload(
                    path=nome_arquivo, 
                    file=imagem_otimizada.read(), 
                    file_options={"content-type": "image/jpeg", "upsert": "true"}
                )
                dados_novos["Foto"] = self.supabase.storage.from_("fotos_perfil").get_public_url(nome_arquivo)

            self.supabase.table("Pessoa").update(dados_novos).eq("CPF", cpf_original).execute()
            return True, "Dados atualizados com sucesso!"
        except Exception as e:
            return False, f"Erro na atualização: {str(e)}"

    def deletar_usuario(self, cpf):
        try:
         
            try:
                nome_arquivo = f"perfil_{cpf}.jpg"
                self.supabase.storage.from_("fotos_perfil").remove([nome_arquivo])
            except:
                pass 
                
            self.supabase.table("Pessoa").delete().eq("CPF", cpf).execute()
            return True, "Usuário e foto removidos com sucesso!"
        except Exception as e:
            return False, str(e)