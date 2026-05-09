import threading
from flask import Flask, request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Import your existing forensic and ML logic
from model import load_spam_model, load_hate_model, load_email_model
from utils import is_malicious_url

# --- FLASK WEB SERVER CONFIGURATION ---
webapp = Flask(__name__)
chat_instance = None

HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; padding: 20px; background: #121212; color: white; text-align: center; }
        input { width: 80%; padding: 15px; margin: 10px 0; border-radius: 5px; border: none; font-size: 16px; }
        button { width: 80%; padding: 15px; background: #007bff; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h2>PhishGuard Web Client</h2>
    <p>Connected to Forensic Monitor</p>
    <input id="msg" type="text" placeholder="Type message to test...">
    <br>
    <button onclick="send()">SEND MESSAGE</button>
    <script>
        function send() {
            var val = document.getElementById('msg').value;
            if(!val) return;
            fetch('/send?msg=' + encodeURIComponent(val));
            document.getElementById('msg').value = '';
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
        Clock.schedule_once(lambda dt: chat_instance.update_chat("iPhone/Remote", msg, threat))
    return "Received"

# --- KIVY FORENSIC MONITOR APP ---
class PhishGuardApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        self.title = "Forensic-by-Design Monitor"
        self.load_models()

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Chat Log
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_history = Label(
            text="[System] Monitoring station initialized...\n",
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='16sp'
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll.add_widget(self.chat_history)
        layout.add_widget(self.scroll)

        # Local Testing Box
        self.local_input = TextInput(hint_text="Test locally here...", multiline=False, size_hint_y=0.1)
        self.local_input.bind(on_text_validate=self.send_local)
        layout.add_widget(self.local_input)

        threading.Thread(target=self.run_server, daemon=True).start()
        return layout

    def load_models(self):
        try:
            self.spam_model, self.spam_vec = load_spam_model()
            self.hate_model, self.hate_vec = load_hate_model()
            self.email_model, self.email_vec = load_email_model()
        except Exception as e:
            print(f"Loading Error: {e}")

    def analyze_text(self, text):
        """Enhanced Detection with Probability Thresholds and Whitelist"""
        text_lower = text.lower()
        
        # 1. Forensic Whitelist: Fixes "Come to my house" and common phrases
        safe_words = ["house", "home", "university", "student", "lunch", "meet", "exam", "class"]
        if len(text.split()) < 6 and any(w in text_lower for w in safe_words):
            return "SAFE"
        
        try:
            # 2. Probability Analysis (Avoids aggressive false positives)
            # Only block if model is more than 85% certain
            #
            spam_prob = self.spam_model.predict_proba(self.spam_vec.transform([text]))[0][1]
            if spam_prob > 0.85: return "SPAM"

            email_prob = self.email_model.predict_proba(self.email_vec.transform([text]))[0][1]
            if email_prob > 0.85: return "PHISHING"

            # 3. Pattern Matching (URL Logic)
            if is_malicious_url(text): return "MALICIOUS LINK"
            
        except Exception as e:
            print(f"Analysis Exception: {e}")
            
        return "SAFE"

    def update_chat(self, sender, message, threat_type):
        color = "ffffff" 
        display_msg = message

        if threat_type != "SAFE":
            color = "ff4444" 
            display_msg = f"*** [BLOCKED: {threat_type}] ***"

        new_entry = f"[b][{sender}][/b]: [color={color}]{display_msg}[/color]\n"
        self.chat_history.text += new_entry

    def send_local(self, instance):
        msg = self.local_input.text.strip()
        if msg:
            threat = self.analyze_text(msg)
            self.update_chat("Local", msg, threat)
            self.local_input.text = ""

    def run_server(self):
        global chat_instance
        chat_instance = self
        # Runs on port 8080. Access via iPhone at http://YOUR_PC_IP:8080
        webapp.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

if __name__ == "__main__":
    PhishGuardApp().run()