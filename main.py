import threading
import pickle
import os
from flask import Flask, request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Import your helper
from utils import is_malicious_url

# --- FLASK WEB SERVER (THE ENGINE) ---
webapp = Flask(__name__)
chat_instance = None

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhishGuard Remote</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f1216; color: #e0e0e0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { width: 90%; max-width: 400px; padding: 25px; background: #1c2128; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #30363d; }
        h2 { color: #58a6ff; margin-bottom: 5px; font-weight: 500; }
        p { color: #8b949e; margin-bottom: 25px; font-size: 14px; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #30363d; background: #0d1117; color: white; font-size: 16px; box-sizing: border-box; }
        input:focus { border-color: #58a6ff; outline: none; }
        button { width: 100%; padding: 15px; background: #238636; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: 0.3s; }
        button:hover { background: #2ea043; }
        .status { font-size: 12px; margin-top: 15px; color: #3fb950; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Forensic Client</h2>
        <p>Agentic Threat Detection System</p>
        <input id="msg" type="text" placeholder="Enter message or URL...">
        <button onclick="send()">EMIT DATA</button>
        <div class="status">● System Synchronized</div>
    </div>
    <script>
        function send() {
            const val = document.getElementById('msg').value;
            if(!val) return;
            fetch('/send?msg=' + encodeURIComponent(val))
                .then(() => {
                    document.getElementById('msg').value = '';
                });
        }
    </script>
</body>
</html>
"""

@webapp.route('/')
def index():
    return HTML_INTERFACE

@webapp.route('/send')
def receive_from_web():
    msg = request.args.get('msg')
    if msg and chat_instance:
        threat = chat_instance.analyze_text(msg)
        Clock.schedule_once(lambda dt: chat_instance.update_chat("Remote-IP", msg, threat))
    return "OK"

# --- KIVY FORENSIC MONITOR APP (THE UI) ---
class PhishGuardApp(App):
    def build(self):
        # Professional Setup
        Window.size = (600, 800)
        Window.clearcolor = (0.05, 0.07, 0.09, 1) # Deep Midnight Blue
        self.title = "PhishGuard Forensic Monitoring Dashboard"
        self.load_models()

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header Label
        header = Label(
            text="[b]CYBER-FORENSIC DATA STREAM[/b]",
            markup=True, size_hint_y=0.05, color=(0.35, 0.65, 1, 1), font_size='18sp'
        )
        main_layout.add_widget(header)

        # Scrollable Monitor
        self.scroll = ScrollView(size_hint=(1, 0.85), bar_width=5)
        self.chat_history = Label(
            text="[color=8b949e][SYSTEM][/color] Initializing Probability Engines...\n"
                 "[color=3fb950][SYSTEM][/color] Forensic Node Active on Port 8080\n"
                 "----------------------------------------------------------------\n",
            markup=True, size_hint_y=None, halign='left', valign='top', font_size='15sp', font_name='Roboto'
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll.add_widget(self.chat_history)
        main_layout.add_widget(self.scroll)

        # Manual Entry for Local Testing
        self.local_input = TextInput(
            hint_text="Manual Injection (Type here...)", 
            multiline=False, size_hint_y=0.08,
            background_color=(0.1, 0.13, 0.17, 1), foreground_color=(1, 1, 1, 1),
            cursor_color=(0.35, 0.65, 1, 1), padding=[10, 10]
        )
        self.local_input.bind(on_text_validate=self.send_local)
        main_layout.add_widget(self.local_input)

        threading.Thread(target=self.run_server, daemon=True).start()
        return main_layout

    def load_models(self):
        try:
            with open("saved_model/email_model.pkl", "rb") as f:
                self.email_model, self.email_vec = pickle.load(f)
            with open("saved_model/hate_model.pkl", "rb") as f:
                self.hate_model, self.hate_vec = pickle.load(f)
            print("✅ Memory Loaded Successfully.")
        except Exception as e:
            print(f"❌ Initialization Failed: {e}")

    def analyze_text(self, text):
        raw_text = text.lower().strip()
        
        # 1. Trusted Domain Whitelist (Fix for uits.edu.bd)
        trusted = [".edu.bd", ".gov.bd", "google.com", "uits.edu.bd"]
        if any(domain in raw_text for domain in trusted):
            return "SAFE"

        # 2. Contextual Social Whitelist (Fix for 'Come to my house')
        social = ["house", "home", "lunch", "meet", "dinner", "university"]
        if len(raw_text.split()) < 7 and any(w in raw_text for w in social):
            return "SAFE"

        # 3. Enhanced Malicious URL Detection (Fix for google.xyz)
        if is_malicious_url(text):
            return "MALICIOUS LINK"

        # 4. Violence Rules
        if any(word in raw_text for word in ["kill", "murder", "bomb", "attack"]):
            return "VIOLENT THREAT"
        
        try:
            # 5. Probabilistic ML Models
            h_score = self.hate_model.predict_proba(self.hate_vec.transform([text]))[0][1]
            if h_score > 0.50: return f"HATE/THREAT ({int(h_score*100)}%)"

            e_score = self.email_model.predict_proba(self.email_vec.transform([text]))[0][1]
            if e_score > 0.75: return f"PHISHING ({int(e_score*100)}%)"
                
        except:
            pass
            
        return "SAFE"

    def update_chat(self, sender, message, threat):
        timestamp = Clock.get_time() # Generic timestamp simulation
        
        if threat == "SAFE":
            color = "3fb950" # Green
            status_text = "PASSED"
            display_msg = message
        else:
            color = "f85149" # Red
            status_text = f"BLOCKED: {threat}"
            display_msg = f"[SENSITIVE DATA REDACTED]"

        entry = (f"[color=8b949e][{sender}][/color] "
                 f"[color={color}][{status_text}][/color] -> {display_msg}\n")
        
        self.chat_history.text += entry

    def send_local(self, instance):
        msg = self.local_input.text.strip()
        if msg:
            threat = self.analyze_text(msg)
            self.update_chat("ADMIN", msg, threat)
            self.local_input.text = ""

    def run_server(self):
        global chat_instance
        chat_instance = self
        webapp.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == "__main__":
    PhishGuardApp().run()