import flet as ft
import serial
import serial.tools.list_ports
import threading
import time

def main(page: ft.Page):
    page.title = "RP2350 CyberDeck"
    page.bgcolor = ft.colors.BLACK
    page.padding = 0

    # شاشة برسم مطلق لتحديد مواقع العناصر بدقة (Stack)
    canvas_stack = ft.Stack(expand=True)
    page.add(canvas_stack)

    widgets_dict = {}
    ser_ref = [None]

    def send_event(data):
        if ser_ref[0] and ser_ref[0].is_open:
            try:
                ser_ref[0].write(f"{data}\n".encode('utf-8'))
            except Exception as e:
                print("Send error:", e)

    def parse_command(cmd):
        parts = cmd.split(',')
        action = parts[0]

        if action == "CLEAR":
            canvas_stack.controls.clear()
            widgets_dict.clear()
            page.update()

        elif action == "BTN" and len(parts) >= 7:
            # BTN,id,text,x,y,w,h,[r,g,b]
            w_id, text = parts[1], parts[2]
            x, y, w, h = float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6])
            
            bg_color = ft.colors.BLUE
            if len(parts) >= 10:
                r, g, b = int(parts[7]), int(parts[8]), int(parts[9])
                bg_color = f"#{r:02x}{g:02x}{b:02x}"

            btn = ft.Container(
                content=ft.ElevatedButton(
                    text=text,
                    on_click=lambda e, b_id=w_id: send_event(f"CLICK:{b_id}"),
                    style=ft.ButtonStyle(
                        bgcolor=bg_color,
                        color=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                left=x,
                top=y,
                width=w,
                height=h,
            )
            canvas_stack.controls.append(btn)
            widgets_dict[w_id] = btn
            page.update()

        elif action == "TXT" and len(parts) >= 6:
            # TXT,id,text,x,y,size,[r,g,b]
            w_id, text = parts[1], parts[2]
            x, y, size = float(parts[3]), float(parts[4]), float(parts[5])
            
            txt_color = ft.colors.WHITE
            if len(parts) >= 9:
                r, g, b = int(parts[6]), int(parts[7]), int(parts[8])
                txt_color = f"#{r:02x}{g:02x}{b:02x}"

            txt = ft.Container(
                content=ft.Text(value=text, size=size, color=txt_color, weight=ft.FontWeight.BOLD),
                left=x,
                top=y,
            )
            canvas_stack.controls.append(txt)
            widgets_dict[w_id] = txt
            page.update()

        elif action == "RECT" and len(parts) >= 6:
            # RECT,id,x,y,w,h,[r,g,b]
            w_id = parts[1]
            x, y, w, h = float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
            
            rect_color = ft.colors.WHITE
            if len(parts) >= 9:
                r, g, b = int(parts[6]), int(parts[7]), int(parts[8])
                rect_color = f"#{r:02x}{g:02x}{b:02x}"

            rect = ft.Container(
                left=x,
                top=y,
                width=w,
                height=h,
                bgcolor=rect_color,
                border_radius=4,
            )
            canvas_stack.controls.append(rect)
            widgets_dict[w_id] = rect
            page.update()

    def read_serial():
        while True:
            ports = list(serial.tools.list_ports.comports())
            if ports and (not ser_ref[0] or not ser_ref[0].is_open):
                try:
                    ser_ref[0] = serial.Serial(ports[0].device, 115200, timeout=0.05)
                    time.sleep(1)
                    send_event("REQ_UI")
                except Exception:
                    pass
            
            if ser_ref[0] and ser_ref[0].is_open:
                try:
                    line = ser_ref[0].readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        parse_command(line)
                except Exception:
                    pass
            time.sleep(0.01)

    threading.Thread(target=read_serial, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)
