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

# Import your helper
from utils import is_malicious_url

# --- FLASK WEB SERVER ---
webapp = Flask(__name__)
chat_instance = None

@webapp.route('/')
def index():
    return "<h1>Client Connected</h1>"

@webapp.route('/send')
def receive_from_web():
    msg = request.args.get('msg')
    if msg and chat_instance:
        threat = chat_instance.analyze_text(msg)
        Clock.schedule_once(lambda dt: chat_instance.update_chat("iPhone", msg, threat))
    return "Data Processed"

# --- KIVY MONITOR APP ---
class PhishApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        self.title = "Forensic Monitoring System"
        self.load_models()

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Monitor Display
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_history = Label(
            text="[SYSTEM] Forensic Engine Online...\n[SYSTEM] Ready for Input...\n",
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
        self.local_input = TextInput(hint_text="Test locally...", multiline=False, size_hint_y=0.1)
        self.local_input.bind(on_text_validate=self.send_local)
        layout.add_widget(self.local_input)

        threading.Thread(target=self.run_server, daemon=True).start()
        return layout

    def load_models(self):
        try:
            with open("saved_model/email_model.pkl", "rb") as f:
                self.email_model, self.email_vec = pickle.load(f)
            with open("saved_model/hate_model.pkl", "rb") as f:
                self.hate_model, self.hate_vec = pickle.load(f)
            print("✅ Models loaded.")
        except Exception as e:
            print(f"❌ Load Error: {e}")

    def analyze_text(self, text):
        text_lower = text.lower().strip()
        
        # --- LAYER 1: TRUSTED WHITELIST (The "Safe" exception) ---
        # This fixes 'uits.edu.bd' being marked as spam
        trusted = [".edu.bd", ".gov.bd", "google.com", "microsoft.com"]
        if any(domain in text_lower for domain in trusted):
            return "SAFE"

        # --- LAYER 2: CONTEXTUAL SOCIAL WHITELIST ---
        # This fixes 'Come to my house'
        safe_words = ["house", "home", "lunch", "dinner", "meet", "study"]
        if len(text_lower.split()) < 7 and any(w in text_lower for w in safe_words):
            return "SAFE"

        # --- LAYER 3: MALICIOUS URLS (The "xyz" fix) ---
        if is_malicious_url(text):
            return "MALICIOUS LINK"

        # --- LAYER 4: VIOLENCE CHECK ---
        critical = ["kill", "murder", "bomb", "attack", "dead"]
        if any(word in text_lower for word in critical):
            return "VIOLENT THREAT"
        
        try:
            # --- LAYER 5: ML ANALYSIS ---
            # Hate Model (0.4 threshold)
            h_prob = self.hate_model.predict_proba(self.hate_vec.transform([text]))[0][1]
            if h_prob > 0.40: return "HATE/THREAT"

            # Email Model (0.75 threshold)
            e_prob = self.email_model.predict_proba(self.email_vec.transform([text]))[0][1]
            if e_prob > 0.75: return "PHISHING/SPAM"
                
        except:
            pass
            
        return "SAFE"

    def update_chat(self, sender, message, threat_type):
        color = "ffffff" 
        msg_out = message
        if threat_type != "SAFE":
            color = "ff4444" 
            msg_out = f"*** [BLOCKED: {threat_type}] ***"
        
        self.chat_history.text += f"[b][{sender}][/b]: [color={color}]{msg_out}[/color]\n"

    def send_local(self, instance):
        msg = self.local_input.text.strip()
        if msg:
            threat = self.analyze_text(msg)
            self.update_chat("Local", msg, threat)
            self.local_input.text = ""

    def run_server(self):
        global chat_instance
        chat_instance = self
        webapp.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == "__main__":
    PhishApp().run()