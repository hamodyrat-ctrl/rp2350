import serial
import serial.tools.list_ports
import threading
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class UniversalDisplay(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widgets = {}
        self.rect_graphics = {}
        self.ser = None
        self.connect_serial()

    def auto_find_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            return p.device
        return None

    def connect_serial(self):
        port = self.auto_find_port()
        if port:
            try:
                self.ser = serial.Serial(port, 115200, timeout=0.05)
                print(f"Connected to {port}")
                threading.Thread(target=self.read_serial, daemon=True).start()
                Clock.schedule_once(lambda dt: self.send_event("REQ_UI"), 1.0)
            except Exception as e:
                print(f"Connection Error: {e}")
        else:
            print("No Serial Port Found!")

    def read_serial(self):
        while True:
            if self.ser and self.ser.is_open:
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        Clock.schedule_once(lambda dt, l=line: self.parse_command(l))
                except Exception:
                    pass

    def parse_command(self, cmd):
        parts = cmd.split(',')
        action = parts[0]

        if action == "CLEAR":
            self.clear_widgets()
            self.canvas.before.clear()
            self.widgets.clear()
            self.rect_graphics.clear()

        elif action == "BTN" and len(parts) >= 7:
            # BTN,id,text,x,y,w,h,[r,g,b]
            w_id, text = parts[1], parts[2]
            x, y, w, h = float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6])
            
            btn = Button(text=text, pos=(x, y), size_hint=(None, None), size=(w, h))
            if len(parts) >= 10:
                r, g, b = float(parts[7])/255.0, float(parts[8])/255.0, float(parts[9])/255.0
                btn.background_color = (r, g, b, 1)
                
            btn.bind(on_press=lambda inst, b_id=w_id: self.send_event(f"CLICK:{b_id}"))
            
            if w_id in self.widgets:
                self.remove_widget(self.widgets[w_id])
            self.add_widget(btn)
            self.widgets[w_id] = btn

        elif action == "TXT" and len(parts) >= 6:
            # TXT,id,text,x,y,size,[r,g,b]
            w_id, text = parts[1], parts[2]
            x, y, size = float(parts[3]), float(parts[4]), float(parts[5])
            
            if w_id in self.widgets:
                self.widgets[w_id].text = text
                self.widgets[w_id].pos = (x, y)
            else:
                lbl = Label(text=text, pos=(x, y), font_size=size, size_hint=(None, None))
                if len(parts) >= 9:
                    r, g, b = float(parts[6])/255.0, float(parts[7])/255.0, float(parts[8])/255.0
                    lbl.color = (r, g, b, 1)
                self.add_widget(lbl)
                self.widgets[w_id] = lbl

        elif action == "RECT" and len(parts) >= 6:
            # RECT,id,x,y,w,h,[r,g,b]
            w_id = parts[1]
            x, y, w, h = float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
            r, g, b = 1.0, 1.0, 1.0
            if len(parts) >= 9:
                r, g, b = float(parts[6])/255.0, float(parts[7])/255.0, float(parts[8])/255.0
                
            with self.canvas.before:
                Color(r, g, b)
                rect = Rectangle(pos=(x, y), size=(w, h))
                self.rect_graphics[w_id] = rect

    def send_event(self, data):
        if self.ser and self.ser.is_open:
            self.ser.write(f"{data}\n".encode('utf-8'))

class ControllerApp(App):
    def build(self):
        return UniversalDisplay()

if __name__ == '__main__':
    ControllerApp().run()