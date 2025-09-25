#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Calendar GUI - Aplicação Desktop para Enviar Eventos via Web App
Autor: Assistente IA
Versão: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv, set_key

class GoogleCalendarGUI:
    """Interface gráfica para enviar eventos para Google Calendar via Web App."""
    
    def __init__(self, root):
        self.root = root
        self.setup_logging()
        self.setup_ui()
        self.load_config()
        
    def setup_logging(self):
        """Configura o sistema de logging para erros técnicos."""
        logging.basicConfig(
            filename='gcal_gui.log',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        
    def setup_ui(self):
        """Configura a interface gráfica."""
        self.root.title("Google Calendar - Enviar Eventos")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Configurar grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.create_config_section()
        self.create_json_editor_section()
        self.create_response_section()
        self.create_status_bar()
        
    def create_config_section(self):
        """Cria a secção de configuração."""
        # Frame de configuração
        config_frame = ttk.LabelFrame(self.root, text="Configuração", padding=10)
        config_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        config_frame.grid_columnconfigure(1, weight=1)
        
        # Web App URL
        ttk.Label(config_frame, text="Web App URL:").grid(row=0, column=0, sticky="w", pady=2)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(config_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # Calendar ID (opcional - o script usa sempre o calendário padrão)
        ttk.Label(config_frame, text="Calendar ID (opcional):").grid(row=1, column=0, sticky="w", pady=2)
        self.calendar_var = tk.StringVar(value="primary")
        self.calendar_entry = ttk.Entry(config_frame, textvariable=self.calendar_var, width=50)
        self.calendar_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # Botões de configuração
        buttons_frame = ttk.Frame(config_frame)
        buttons_frame.grid(row=2, column=1, sticky="e", pady=(10, 0))
        
        ttk.Button(
            buttons_frame, 
            text="Guardar .env", 
            command=self.save_config
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(
            buttons_frame,
            text="🔧 Debug",
            command=self.show_debug_info
        ).pack(side=tk.RIGHT, padx=(0, 5))
        
        ttk.Button(
            buttons_frame,
            text="🌐 Test URL",
            command=self.test_webapp_directly
        ).pack(side=tk.RIGHT)
        
    def create_json_editor_section(self):
        """Cria a secção do editor de JSON."""
        # Frame do editor JSON
        editor_frame = ttk.LabelFrame(self.root, text="Editor de JSON", padding=10)
        editor_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        editor_frame.grid_columnconfigure(0, weight=1)
        editor_frame.grid_rowconfigure(1, weight=1)
        
        # Botões do editor
        buttons_frame = ttk.Frame(editor_frame)
        buttons_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Inserir Template teste", 
                  command=self.insert_test_template).pack(side="left", padx=(0, 5))
        ttk.Button(buttons_frame, text="Carregar JSON de ficheiro…", 
                  command=self.load_json_file).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Formatar JSON", 
                  command=self.format_json).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Limpar", 
                  command=self.clear_json).pack(side="left", padx=5)
        
        # Editor de texto
        self.json_editor = scrolledtext.ScrolledText(
            editor_frame, 
            height=15, 
            font=("Consolas", 10),
            wrap=tk.NONE
        )
        self.json_editor.grid(row=1, column=0, sticky="nsew")
        
        # Botão de envio
        self.send_btn = ttk.Button(
            editor_frame, 
            text="Enviar para Web App", 
            command=self.send_to_webapp,
            style="Accent.TButton"
        )
        self.send_btn.grid(row=2, column=0, pady=(10, 0))
        
    def create_response_section(self):
        """Cria a secção de resposta."""
        # Frame de resposta
        response_frame = ttk.LabelFrame(self.root, text="Resposta", padding=10)
        response_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        response_frame.grid_columnconfigure(0, weight=1)
        response_frame.grid_rowconfigure(0, weight=1)
        
        # Área de resposta
        self.response_text = scrolledtext.ScrolledText(
            response_frame, 
            height=8, 
            font=("Consolas", 9),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.response_text.grid(row=0, column=0, sticky="nsew")
        
    def create_status_bar(self):
        """Cria a barra de estado."""
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        
            
    def load_config(self):
        """Carrega a configuração do ficheiro .env."""
        try:
            if os.path.exists('.env'):
                load_dotenv()
                self.url_var.set(os.getenv('WEB_APP_URL', ''))
                calendar_id = os.getenv('CALENDAR_ID', 'primary')
                self.calendar_var.set(calendar_id)
                self.update_status("Configuração carregada do ficheiro .env")
        except Exception as e:
            logging.error(f"Erro ao carregar configuração: {e}")
            self.update_status("Erro ao carregar configuração")
            
    def save_config(self):
        """Guarda a configuração no ficheiro .env."""
        try:
            set_key('.env', 'WEB_APP_URL', self.url_var.get())
            set_key('.env', 'CALENDAR_ID', self.calendar_var.get())
            self.update_status("Configuração guardada no ficheiro .env")
            messagebox.showinfo("Sucesso", "Configuração guardada com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao guardar configuração: {e}")
            messagebox.showerror("Erro", f"Erro ao guardar configuração: {e}")
            
    def insert_test_template(self):
        """Insere um template de teste no editor."""
        template = {
            "title": "Teste ChatGPT",
            "start": "2025-09-22T09:30:00+01:00",
            "end": "2025-09-22T10:00:00+01:00",
            "description": "Evento de teste criado via Web App (Apps Script).",
            "location": "Local de teste"
        }
        
        self.json_editor.delete(1.0, tk.END)
        self.json_editor.insert(1.0, json.dumps(template, indent=2, ensure_ascii=False))
        
    def load_json_file(self):
        """Carrega um ficheiro JSON."""
        file_path = filedialog.askopenfilename(
            title="Selecionar ficheiro JSON",
            filetypes=[("Ficheiros JSON", "*.json"), ("Todos os ficheiros", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Validar JSON
                    json.loads(content)
                    self.json_editor.delete(1.0, tk.END)
                    self.json_editor.insert(1.0, content)
                    self.update_status(f"Ficheiro carregado: {os.path.basename(file_path)}")
            except json.JSONDecodeError as e:
                messagebox.showerror("Erro", f"Ficheiro JSON inválido: {e}")
            except Exception as e:
                logging.error(f"Erro ao carregar ficheiro: {e}")
                messagebox.showerror("Erro", f"Erro ao carregar ficheiro: {e}")
                
    def format_json(self):
        """Formata o JSON no editor."""
        try:
            content = self.json_editor.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("Aviso", "Editor vazio")
                return
                
            # Validar e formatar JSON
            parsed = json.loads(content)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            
            self.json_editor.delete(1.0, tk.END)
            self.json_editor.insert(1.0, formatted)
            self.update_status("JSON formatado com sucesso")
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Erro", f"JSON inválido: {e}")
        except Exception as e:
            logging.error(f"Erro ao formatar JSON: {e}")
            messagebox.showerror("Erro", f"Erro ao formatar JSON: {e}")
            
    def clear_json(self):
        """Limpa o editor de JSON."""
        self.json_editor.delete(1.0, tk.END)
        self.update_status("Editor limpo")
        
    def send_to_webapp(self):
        """Envia o JSON para o Web App. Suporta evento único ou múltiplos eventos."""
        # Validar configuração
        if not self.url_var.get().strip():
            messagebox.showerror("Erro", "Web App URL é obrigatório")
            return

        # Ler e validar JSON
        try:
            content = self.json_editor.get(1.0, tk.END).strip()
            if not content:
                messagebox.showerror("Erro", "Editor de JSON está vazio")
                return

            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            messagebox.showerror("Erro", f"JSON inválido: {e}")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no JSON: {e}")
            return

        # Preparar lista de eventos a enviar
        try:
            events_to_send = []

            if isinstance(parsed, list):
                # Top-level array de eventos
                if not parsed:
                    raise ValueError("A lista de eventos está vazia")
                events_to_send = parsed
            elif isinstance(parsed, dict):
                if 'events' in parsed:
                    # Objeto com chave 'events' (lista)
                    events = parsed.get('events')
                    if not isinstance(events, list) or not events:
                        raise ValueError("'events' deve ser uma lista com pelo menos um evento")
                    events_to_send = events
                else:
                    # Evento único como objeto
                    events_to_send = [parsed]
            else:
                raise ValueError("JSON deve ser um objeto ou uma lista de eventos")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao preparar eventos: {e}")
            return

        # Enviar eventos (um POST por evento)
        self.update_status("A enviar eventos...")
        self.send_btn.config(state=tk.DISABLED)

        headers = {
            'Content-Type': 'application/json'
        }

        results = []
        try:
            logging.info(f"Envio de {len(events_to_send)} evento(s) para: {self.url_var.get()}")
            logging.info(f"Headers: Content-Type={headers['Content-Type']}")

            for idx, event_payload in enumerate(events_to_send, start=1):
                try:
                    # Log detalhado por evento (sem dados sensíveis)
                    logging.info(f"[Evento {idx}] Payload: {json.dumps(event_payload, ensure_ascii=False)}")

                    response = requests.post(
                        self.url_var.get(),
                        headers=headers,
                        data=json.dumps(event_payload, ensure_ascii=False),
                        timeout=20,
                        verify=True
                    )

                    result_entry = {
                        'index': idx,
                        'status_code': response.status_code,
                        'ok': 200 <= response.status_code < 300,
                        'body': None,
                    }
                    try:
                        result_entry['body'] = response.json()
                    except Exception:
                        result_entry['body'] = response.text

                    results.append(result_entry)
                except requests.exceptions.Timeout:
                    logging.error(f"[Evento {idx}] Timeout")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': 'Timeout'})
                except requests.exceptions.ConnectionError:
                    logging.error(f"[Evento {idx}] Erro de ligação")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': 'Erro de ligação'})
                except requests.exceptions.RequestException as e:
                    logging.error(f"[Evento {idx}] Erro na requisição: {e}")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': f'Request error: {e}'})
                except Exception as e:
                    logging.error(f"[Evento {idx}] Erro inesperado: {e}")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': f'Erro inesperado: {e}'})

            # Mostrar resultado agregado
            self.show_batch_response(results)


            self.update_status("Envio concluído")

        finally:
            self.send_btn.config(state=tk.NORMAL)
            
    def show_response(self, response):
        """Mostra a resposta da requisição."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        
        # Cabeçalho com status HTTP
        header = f"HTTP {response.status_code}\n"
        self.response_text.insert(tk.END, header)
        
        # Corpo da resposta
        try:
            # Tentar parsear como JSON
            response_json = response.json()
            response_text = json.dumps(response_json, indent=2, ensure_ascii=False)
        except:
            # Se não for JSON, mostrar texto raw
            response_text = response.text
            
        self.response_text.insert(tk.END, response_text)
        self.response_text.config(state=tk.DISABLED)

    def show_batch_response(self, results):
        """Mostra um resumo agregado das respostas por evento."""
        total = len(results)
        succeeded = sum(1 for r in results if r.get('ok'))
        failed = total - succeeded

        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)

        summary = [
            f"Total de eventos: {total}",
            f"Sucesso: {succeeded}",
            f"Falhas: {failed}",
            "",
            "Detalhes por evento:",
        ]

        for r in results:
            idx = r.get('index')
            status = r.get('status_code')
            ok_flag = 'OK' if r.get('ok') else 'FALHA'
            body = r.get('body')
            try:
                body_text = json.dumps(body, ensure_ascii=False, indent=2) if isinstance(body, (dict, list)) else str(body)
            except Exception:
                body_text = str(body)
            summary.append(f"--- Evento {idx} | HTTP {status} | {ok_flag}")
            summary.append(body_text)

        self.response_text.insert(tk.END, "\n".join(summary))
        self.response_text.config(state=tk.DISABLED)
        
    def show_error_response(self, error_msg):
        """Mostra uma mensagem de erro na área de resposta."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, f"ERRO: {error_msg}")
        self.response_text.config(state=tk.DISABLED)
        self.update_status("Erro")
        
    def update_status(self, message):
        """Atualiza a barra de estado."""
        self.status_var.set(message)
        
        
    def open_log_file(self):
        """Abre o ficheiro de log para visualização."""
        try:
            if os.path.exists('gcal_gui.log'):
                os.startfile('gcal_gui.log')
            else:
                messagebox.showinfo("Info", "Ficheiro de log não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o ficheiro de log: {e}")
            
    def test_webapp_url(self):
        """Testa se o Web App URL está acessível."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Web App URL não configurado")
            return
            
        try:
            import webbrowser
            webbrowser.open(url)
            messagebox.showinfo("Info", "Web App aberto no browser. Verifique se está acessível.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o URL: {e}")
            
    def show_debug_info(self):
        """Mostra informações de debug da configuração atual."""
        debug_info = f"""
🔧 INFORMAÇÕES DE DEBUG

Configuração Atual:
• Web App URL: {self.url_var.get() or '[NÃO CONFIGURADO]'}
• Calendar ID: {self.calendar_var.get() or '[NÃO CONFIGURADO]'}

Ficheiros:
• .env existe: {'SIM' if os.path.exists('.env') else 'NÃO'}
• gcal_gui.log existe: {'SIM' if os.path.exists('gcal_gui.log') else 'NÃO'}

JSON no Editor:
• Conteúdo: {'[VAZIO]' if not self.json_editor.get(1.0, tk.END).strip() else '[PRESENTE]'}
• Tamanho: {len(self.json_editor.get(1.0, tk.END).strip())} caracteres

Dicas:
• Confirme que o Web App está publicado como "Anyone"
• Teste o URL diretamente no browser
• Verifique os logs para mais detalhes
• O script não precisa de autenticação - só envia JSON
        """
        
        # Criar janela de debug
        debug_window = tk.Toplevel(self.root)
        debug_window.title("Informações de Debug")
        debug_window.geometry("500x400")
        debug_window.resizable(True, True)
        
        # Frame principal
        main_frame = ttk.Frame(debug_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Texto de debug
        text_widget = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Inserir texto
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(1.0, debug_info)
        text_widget.config(state=tk.DISABLED)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="Copiar Info",
            command=lambda: self.copy_debug_info(debug_info)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Fechar",
            command=debug_window.destroy
        ).pack(side=tk.RIGHT)
        
    def copy_debug_info(self, debug_info):
        """Copia as informações de debug para a área de transferência."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(debug_info)
            messagebox.showinfo("Sucesso", "Informações de debug copiadas para a área de transferência!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível copiar: {e}")
            
            
    def test_webapp_directly(self):
        """Testa o Web App com um GET request simples."""
        if not self.url_var.get().strip():
            messagebox.showerror("Erro", "Web App URL é obrigatório")
            return
            
        self.update_status("A testar Web App...")
        
        try:
            # Teste GET simples
            logging.info("=== TESTE DIRETO DO WEB APP ===")
            logging.info(f"URL: {self.url_var.get()}")
            
            response = requests.get(self.url_var.get(), timeout=10)
            
            logging.info(f"GET Response status: {response.status_code}")
            logging.info(f"GET Response headers: {dict(response.headers)}")
            logging.info(f"GET Response body: {response.text}")
            
            # Mostrar resultado
            self.response_text.config(state=tk.NORMAL)
            self.response_text.delete(1.0, tk.END)
            
            result = f"GET Request Result:\n"
            result += f"HTTP {response.status_code}\n\n"
            result += f"Headers:\n{json.dumps(dict(response.headers), indent=2)}\n\n"
            result += f"Body:\n{response.text}"
            
            self.response_text.insert(tk.END, result)
            self.response_text.config(state=tk.DISABLED)
            
            if response.status_code == 200:
                if "doGet" in response.text:
                    messagebox.showwarning("Aviso", 
                        "Web App responde, mas não tem função doGet().\n"
                        "Isto é normal - o Web App só aceita POST requests.\n"
                        "Continue com o teste de autenticação.")
                else:
                    messagebox.showinfo("Sucesso", "Web App está acessível!")
                self.update_status("✅ Web App acessível")
            else:
                messagebox.showerror("Erro", f"Web App retornou HTTP {response.status_code}")
                self.update_status("❌ Web App com problemas")
                
        except requests.exceptions.ConnectionError:
            error_msg = "Não foi possível conectar ao Web App. Verifique o URL."
            logging.error(error_msg)
            messagebox.showerror("Erro de Ligação", error_msg)
            self.update_status("❌ Erro de ligação")
        except Exception as e:
            error_msg = f"Erro no teste: {e}"
            logging.error(error_msg)
            messagebox.showerror("Erro", error_msg)
            self.update_status("❌ Erro no teste")

def main():
    """Função principal."""
    root = tk.Tk()
    
    # Configurar estilo
    style = ttk.Style()
    style.theme_use('clam')
    
    # Criar e executar aplicação
    app = GoogleCalendarGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(f"Erro na aplicação: {e}")
        messagebox.showerror("Erro Fatal", f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
