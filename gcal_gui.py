#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Calendar GUI - Desktop Application to Send Events via Web App
Author: AI Assistant
Version: 1.0
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
    """Graphical interface to send events to Google Calendar via Web App."""
    
    def __init__(self, root):
        self.root = root
        self.setup_logging()
        self.setup_ui()
        self.load_config()
        
    def setup_logging(self):
        """Configure logging system for technical errors."""
        logging.basicConfig(
            filename='gcal_gui.log',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        
    def setup_ui(self):
        """Configure the graphical interface."""
        self.root.title("Google Calendar - Send Events")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.create_config_section()
        self.create_json_editor_section()
        self.create_response_section()
        self.create_status_bar()
        
    def create_config_section(self):
        """Create the configuration section."""
        # Configuration frame
        config_frame = ttk.LabelFrame(self.root, text="Configuration", padding=10)
        config_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        config_frame.grid_columnconfigure(1, weight=1)
        
        # Web App URL
        ttk.Label(config_frame, text="Web App URL:").grid(row=0, column=0, sticky="w", pady=2)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(config_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # Calendar ID (optional - script always uses default calendar)
        ttk.Label(config_frame, text="Calendar ID (optional):").grid(row=1, column=0, sticky="w", pady=2)
        self.calendar_var = tk.StringVar(value="primary")
        self.calendar_entry = ttk.Entry(config_frame, textvariable=self.calendar_var, width=50)
        self.calendar_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=2)
        
        # Configuration buttons
        buttons_frame = ttk.Frame(config_frame)
        buttons_frame.grid(row=2, column=1, sticky="e", pady=(10, 0))
        
        ttk.Button(
            buttons_frame, 
            text="Save .env", 
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
        """Create the JSON editor section."""
        # JSON editor frame
        editor_frame = ttk.LabelFrame(self.root, text="JSON Editor", padding=10)
        editor_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        editor_frame.grid_columnconfigure(0, weight=1)
        editor_frame.grid_rowconfigure(1, weight=1)
        
        # Editor buttons
        buttons_frame = ttk.Frame(editor_frame)
        buttons_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Insert Test Template", 
                  command=self.insert_test_template).pack(side="left", padx=(0, 5))
        ttk.Button(buttons_frame, text="Load JSON from file…", 
                  command=self.load_json_file).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Format JSON", 
                  command=self.format_json).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Clear", 
                  command=self.clear_json).pack(side="left", padx=5)
        
        # Text editor
        self.json_editor = scrolledtext.ScrolledText(
            editor_frame, 
            height=15, 
            font=("Consolas", 10),
            wrap=tk.NONE
        )
        self.json_editor.grid(row=1, column=0, sticky="nsew")
        
        # Send button
        self.send_btn = ttk.Button(
            editor_frame, 
            text="Send to Web App", 
            command=self.send_to_webapp,
            style="Accent.TButton"
        )
        self.send_btn.grid(row=2, column=0, pady=(10, 0))
        
    def create_response_section(self):
        """Create the response section."""
        # Response frame
        response_frame = ttk.LabelFrame(self.root, text="Response", padding=10)
        response_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        response_frame.grid_columnconfigure(0, weight=1)
        response_frame.grid_rowconfigure(0, weight=1)
        
        # Response area
        self.response_text = scrolledtext.ScrolledText(
            response_frame, 
            height=8, 
            font=("Consolas", 9),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.response_text.grid(row=0, column=0, sticky="nsew")
        
    def create_status_bar(self):
        """Create the status bar."""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
        
            
    def load_config(self):
        """Load configuration from .env file."""
        try:
            if os.path.exists('.env'):
                load_dotenv()
                self.url_var.set(os.getenv('WEB_APP_URL', ''))
                calendar_id = os.getenv('CALENDAR_ID', 'primary')
                self.calendar_var.set(calendar_id)
                self.update_status("Configuration loaded from .env file")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            self.update_status("Error loading configuration")
            
    def save_config(self):
        """Save configuration to .env file."""
        try:
            set_key('.env', 'WEB_APP_URL', self.url_var.get())
            set_key('.env', 'CALENDAR_ID', self.calendar_var.get())
            self.update_status("Configuration saved to .env file")
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
            messagebox.showerror("Error", f"Error saving configuration: {e}")
            
    def insert_test_template(self):
        """Insert a test template into the editor."""
        template = {
            "title": "Test Event",
            "start": "2025-09-22T09:30:00+01:00",
            "end": "2025-09-22T10:00:00+01:00",
            "description": "Test event created via Web App (Apps Script).",
            "location": "Test Location"
        }
        
        self.json_editor.delete(1.0, tk.END)
        self.json_editor.insert(1.0, json.dumps(template, indent=2, ensure_ascii=False))
        
    def load_json_file(self):
        """Load a JSON file."""
        file_path = filedialog.askopenfilename(
            title="Select JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Validate JSON
                    json.loads(content)
                    self.json_editor.delete(1.0, tk.END)
                    self.json_editor.insert(1.0, content)
                    self.update_status(f"File loaded: {os.path.basename(file_path)}")
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Invalid JSON file: {e}")
            except Exception as e:
                logging.error(f"Error loading file: {e}")
                messagebox.showerror("Error", f"Error loading file: {e}")
                
    def format_json(self):
        """Format JSON in the editor."""
        try:
            content = self.json_editor.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("Warning", "Editor is empty")
                return
                
            # Validate and format JSON
            parsed = json.loads(content)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            
            self.json_editor.delete(1.0, tk.END)
            self.json_editor.insert(1.0, formatted)
            self.update_status("JSON formatted successfully")
            
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON: {e}")
        except Exception as e:
            logging.error(f"Error formatting JSON: {e}")
            messagebox.showerror("Error", f"Error formatting JSON: {e}")
            
    def clear_json(self):
        """Clear the JSON editor."""
        self.json_editor.delete(1.0, tk.END)
        self.update_status("Editor cleared")
        
    def send_to_webapp(self):
        """Send JSON to Web App. Supports single or multiple events."""
        # Validate configuration
        if not self.url_var.get().strip():
            messagebox.showerror("Error", "Web App URL is required")
            return

        # Read and validate JSON
        try:
            content = self.json_editor.get(1.0, tk.END).strip()
            if not content:
                messagebox.showerror("Error", "JSON editor is empty")
                return

            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON: {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"JSON error: {e}")
            return

        # Prepare list of events to send
        try:
            events_to_send = []

            if isinstance(parsed, list):
                # Top-level array of events
                if not parsed:
                    raise ValueError("Event list is empty")
                events_to_send = parsed
            elif isinstance(parsed, dict):
                if 'events' in parsed:
                    # Object with 'events' key (list)
                    events = parsed.get('events')
                    if not isinstance(events, list) or not events:
                        raise ValueError("'events' must be a list with at least one event")
                    events_to_send = events
                else:
                    # Single event as object
                    events_to_send = [parsed]
            else:
                raise ValueError("JSON must be an object or a list of events")

        except Exception as e:
            messagebox.showerror("Error", f"Error preparing events: {e}")
            return

        # Send events (one POST per event)
        self.update_status("Sending events...")
        self.send_btn.config(state=tk.DISABLED)

        headers = {
            'Content-Type': 'application/json'
        }

        results = []
        try:
            logging.info(f"Sending {len(events_to_send)} event(s) to: {self.url_var.get()}")
            logging.info(f"Headers: Content-Type={headers['Content-Type']}")

            for idx, event_payload in enumerate(events_to_send, start=1):
                try:
                    # Detailed log per event (no sensitive data)
                    logging.info(f"[Event {idx}] Payload: {json.dumps(event_payload, ensure_ascii=False)}")

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
                    logging.error(f"[Event {idx}] Timeout")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': 'Timeout'})
                except requests.exceptions.ConnectionError:
                    logging.error(f"[Event {idx}] Connection error")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': 'Connection error'})
                except requests.exceptions.RequestException as e:
                    logging.error(f"[Event {idx}] Request error: {e}")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': f'Request error: {e}'})
                except Exception as e:
                    logging.error(f"[Event {idx}] Unexpected error: {e}")
                    results.append({'index': idx, 'status_code': 0, 'ok': False, 'body': f'Unexpected error: {e}'})

            # Show aggregated result
            self.show_batch_response(results)


            self.update_status("Send completed")

        finally:
            self.send_btn.config(state=tk.NORMAL)
            
    def show_response(self, response):
        """Show the request response."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        
        # Header with HTTP status
        header = f"HTTP {response.status_code}\n"
        self.response_text.insert(tk.END, header)
        
        # Response body
        try:
            # Try to parse as JSON
            response_json = response.json()
            response_text = json.dumps(response_json, indent=2, ensure_ascii=False)
        except:
            # If not JSON, show raw text
            response_text = response.text
            
        self.response_text.insert(tk.END, response_text)
        self.response_text.config(state=tk.DISABLED)

    def show_batch_response(self, results):
        """Show an aggregated summary of responses per event."""
        total = len(results)
        succeeded = sum(1 for r in results if r.get('ok'))
        failed = total - succeeded

        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)

        summary = [
            f"Total events: {total}",
            f"Success: {succeeded}",
            f"Failures: {failed}",
            "",
            "Details per event:",
        ]

        for r in results:
            idx = r.get('index')
            status = r.get('status_code')
            ok_flag = 'OK' if r.get('ok') else 'FAILED'
            body = r.get('body')
            try:
                body_text = json.dumps(body, ensure_ascii=False, indent=2) if isinstance(body, (dict, list)) else str(body)
            except Exception:
                body_text = str(body)
            summary.append(f"--- Event {idx} | HTTP {status} | {ok_flag}")
            summary.append(body_text)

        self.response_text.insert(tk.END, "\n".join(summary))
        self.response_text.config(state=tk.DISABLED)
        
    def show_error_response(self, error_msg):
        """Show an error message in the response area."""
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, f"ERROR: {error_msg}")
        self.response_text.config(state=tk.DISABLED)
        self.update_status("Error")
        
    def update_status(self, message):
        """Update the status bar."""
        self.status_var.set(message)
        
        
    def open_log_file(self):
        """Open the log file for viewing."""
        try:
            if os.path.exists('gcal_gui.log'):
                os.startfile('gcal_gui.log')
            else:
                messagebox.showinfo("Info", "Log file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open log file: {e}")
            
    def test_webapp_url(self):
        """Test if the Web App URL is accessible."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Web App URL not configured")
            return
            
        try:
            import webbrowser
            webbrowser.open(url)
            messagebox.showinfo("Info", "Web App opened in browser. Check if it's accessible.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {e}")
            
    def show_debug_info(self):
        """Show debug information about current configuration."""
        debug_info = f"""
🔧 DEBUG INFORMATION

Current Configuration:
• Web App URL: {self.url_var.get() or '[NOT CONFIGURED]'}
• Calendar ID: {self.calendar_var.get() or '[NOT CONFIGURED]'}

Files:
• .env exists: {'YES' if os.path.exists('.env') else 'NO'}
• gcal_gui.log exists: {'YES' if os.path.exists('gcal_gui.log') else 'NO'}

JSON in Editor:
• Content: {'[EMPTY]' if not self.json_editor.get(1.0, tk.END).strip() else '[PRESENT]'}
• Size: {len(self.json_editor.get(1.0, tk.END).strip())} characters

Tips:
• Confirm the Web App is published as "Anyone"
• Test the URL directly in browser
• Check logs for more details
• The script doesn't need authentication - just sends JSON
        """
        
        # Create debug window
        debug_window = tk.Toplevel(self.root)
        debug_window.title("Debug Information")
        debug_window.geometry("500x400")
        debug_window.resizable(True, True)
        
        # Main frame
        main_frame = ttk.Frame(debug_window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Debug text
        text_widget = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Insert text
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(1.0, debug_info)
        text_widget.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="Copy Info",
            command=lambda: self.copy_debug_info(debug_info)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Close",
            command=debug_window.destroy
        ).pack(side=tk.RIGHT)
        
    def copy_debug_info(self, debug_info):
        """Copy debug information to clipboard."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(debug_info)
            messagebox.showinfo("Success", "Debug information copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy: {e}")
            
            
    def test_webapp_directly(self):
        """Test the Web App with a simple GET request."""
        if not self.url_var.get().strip():
            messagebox.showerror("Error", "Web App URL is required")
            return
            
        self.update_status("Testing Web App...")
        
        try:
            # Simple GET test
            logging.info("=== DIRECT WEB APP TEST ===")
            logging.info(f"URL: {self.url_var.get()}")
            
            response = requests.get(self.url_var.get(), timeout=10)
            
            logging.info(f"GET Response status: {response.status_code}")
            logging.info(f"GET Response headers: {dict(response.headers)}")
            logging.info(f"GET Response body: {response.text}")
            
            # Show result
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
                    messagebox.showwarning("Warning", 
                        "Web App responds, but doesn't have doGet() function.\n"
                        "This is normal - the Web App only accepts POST requests.\n"
                        "Continue with authentication test.")
                else:
                    messagebox.showinfo("Success", "Web App is accessible!")
                self.update_status("✅ Web App accessible")
            else:
                messagebox.showerror("Error", f"Web App returned HTTP {response.status_code}")
                self.update_status("❌ Web App with problems")
                
        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to Web App. Check the URL."
            logging.error(error_msg)
            messagebox.showerror("Connection Error", error_msg)
            self.update_status("❌ Connection error")
        except Exception as e:
            error_msg = f"Test error: {e}"
            logging.error(error_msg)
            messagebox.showerror("Error", error_msg)
            self.update_status("❌ Test error")

def main():
    """Main function."""
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create and run application
    app = GoogleCalendarGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Fatal Error", f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
