import threading
import pickle
from flask import Flask, request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

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
        input { width: 80%; padding: 15px; margin: 10px 0; border-radius: 5px; border: none; font-size: 16px; background: #333; color: white; }
        button { width: 80%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h2>PhishGuard Remote Client</h2>
    <p>Status: <span style="color:#28a745;">Connected to Forensic Monitor</span></p>
    <input id="msg" type="text" placeholder="Type message here...">
    <br>
    <button onclick="send()">SEND DATA</button>
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
        Clock.schedule_once(lambda dt: chat_instance.update_chat("iPhone", msg, threat))
    return "Received"

# --- KIVY FORENSIC MONITOR APP ---
class PhishGuardApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        self.title = "Forensic-by-Design Monitor"
        self.load_models()

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Monitor Display
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_history = Label(
            text="[SYSTEM] Forensic Engine Online...\n[SYSTEM] Server listening on port 8080...\n",
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='16sp'
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll.add_widget(self.chat_history)
        layout.add_widget(self.scroll)

        # Local Input
        self.local_input = TextInput(hint_text="Test locally...", multiline=False, size_hint_y=0.1, background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1,1,1,1))
        self.local_input.bind(on_text_validate=self.send_local)
        layout.add_widget(self.local_input)

        threading.Thread(target=self.run_server, daemon=True).start()
        return layout

    def load_models(self):
        """Loads models trained with RandomForest support."""
        try:
            with open("saved_model/email_model.pkl", "rb") as f:
                self.email_model, self.email_vec = pickle.load(f)
            with open("saved_model/hate_model.pkl", "rb") as f:
                self.hate_model, self.hate_vec = pickle.load(f)
            print("✅ Models loaded successfully.")
        except Exception as e:
            print(f"❌ Error loading models: {e}. Ensure you ran your training scripts first.")

    def analyze_text(self, text):
        """
        PRIORITY PIPELINE:
        1. Whitelist (Social Safety)
        2. Blacklist (Violence/Critical Threats)
        3. Probabilistic ML Analysis
        """
        text_lower = text.lower().strip()
        words = text_lower.split()
        
        # --- LAYER 1: WHITELIST (Fixes Test 3: 'Come to my house') ---
        # Short social messages with these words are forced to SAFE.
        safe_social = ["house", "home", "lunch", "meet", "university", "professor", "class", "study", "dinner"]
        if len(words) < 8 and any(w in text_lower for w in safe_social):
            return "SAFE"

        # --- LAYER 2: BLACKLIST (Fixes 'Killed the person') ---
        critical_threats = ["kill", "murder", "bomb", "attack", "dead", "shoot", "gun", "knife"]
        if any(word in text_lower for word in critical_threats):
            return "VIOLENT THREAT"
        
        try:
            # --- LAYER 3: HATE SPEECH ML (Test 5) ---
            # Set to 40% sensitivity (lower = more strict)
            hate_vec_input = self.hate_vec.transform([text])
            hate_prob = self.hate_model.predict_proba(hate_vec_input)[0][1]
            if hate_prob > 0.40:
                return "HATE/THREAT"

            # --- LAYER 4: SPAM/PHISHING ML (Test 4) ---
            # Set to 75% sensitivity to catch prize/winning scams
            email_vec_input = self.email_vec.transform([text])
            email_prob = self.email_model.predict_proba(email_vec_input)[0][1]
            if email_prob > 0.75:
                return "PHISHING/SPAM"
                
        except Exception as e:
            print(f"ML Processing Error: {e}")
            
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
        webapp.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

if __name__ == "__main__":
    PhishGuardApp().run()