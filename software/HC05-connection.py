# ADD SERVO MOVEMENT
import customtkinter as ctk
from pyfirmata2 import Arduino
import serial.tools.list_ports
import threading
import time

# Appearance setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def find_hc05_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'HC-05' in port.device:
            return port.device
    return None


class MotorControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HW-095 Motor Controller")
        self.geometry("700x500")
        self.board = None
        self.pins = {}
        self.speed = 0.3  # Default PWM speed
        self.motion_thread = None
        self.stop_motion = False

        self.bind("<KeyPress>", self.key_pressed)

        self.status_label = ctk.CTkLabel(self, text="Connecting to HC-05...", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(pady=10)

        self.btn_w = ctk.CTkButton(self.controls_frame, text="↑ W", width=80)
        self.btn_w.grid(row=0, column=1, padx=10, pady=5)
        self.btn_w.bind('<ButtonPress-1>', lambda e: self.motion_start('W'))
        self.btn_w.bind('<ButtonRelease-1>', lambda e: self.motion_stop())

        self.btn_z = ctk.CTkButton(self.controls_frame, text="↓ Z", width=80)
        self.btn_z.grid(row=2, column=1, padx=10, pady=5)
        self.btn_z.bind('<ButtonPress-1>', lambda e: self.motion_start('Z'))
        self.btn_z.bind('<ButtonRelease-1>', lambda e: self.motion_stop())

        self.btn_a = ctk.CTkButton(self.controls_frame, text="← A", width=80)
        self.btn_a.grid(row=1, column=0, padx=10, pady=5)
        self.btn_a.bind('<ButtonPress-1>', lambda e: self.motion_start('A'))
        self.btn_a.bind('<ButtonRelease-1>', lambda e: self.motion_stop())

        self.btn_d = ctk.CTkButton(self.controls_frame, text="→ D", width=80)
        self.btn_d.grid(row=1, column=2, padx=10, pady=5)
        self.btn_d.bind('<ButtonPress-1>', lambda e: self.motion_start('D'))
        self.btn_d.bind('<ButtonRelease-1>', lambda e: self.motion_stop())

        self.btn_q = ctk.CTkButton(self.controls_frame, text="← Q", width=80)
        self.btn_q.grid(row=0, column=0, padx=10, pady=5)
        self.btn_q.bind('<ButtonPress-1>', lambda e: self.motion_start('Q'))
        self.btn_q.bind('<ButtonRelease-1>', lambda e: self.motion_stop())

        self.btn_e = ctk.CTkButton(self.controls_frame, text="→ E", width=80)
        self.btn_e.grid(row=0, column=2, padx=10, pady=5)
        self.btn_e.bind('<ButtonPress-1>', lambda e: self.motion_start('E'))
        self.btn_e.bind('<ButtonRelease-1>', lambda e: self.motion_stop())

        self.btn_stop = ctk.CTkButton(self.controls_frame, text="■ Stop", command=self.stop, width=80)
        self.btn_stop.grid(row=1, column=1, padx=10, pady=5)
        self.bind('<KeyPress-s>', lambda e: self.motion_stop())
        self.btn_stop.bind('<ButtonPress-1>', lambda e: self.motion_stop())

        self.speed_slider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=10, command=self.set_speed)
        self.speed_slider.set(self.speed)
        self.speed_slider.pack(pady=10)

        self.exit_btn = ctk.CTkButton(self, text="Exit", command=self.on_close)
        self.exit_btn.pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        threading.Thread(target=self.connect_to_board, daemon=True).start()

    def connect_to_board(self):
        port = find_hc05_port()
        if port:
            self.board = Arduino(port)
            self.pins = {
                'ENA': self.board.get_pin('d:11:p'),
                'ENB': self.board.get_pin('d:6:p'),
                'IN1': self.board.get_pin('d:13:o'),
                'IN2': self.board.get_pin('d:12:o'),
                'IN3': self.board.get_pin('d:10:o'),
                'IN4': self.board.get_pin('d:9:o'),
            }
            self.status_label.configure(text=f"Connected to {port}")
        else:
            self.status_label.configure(text="⚠️ HC-05 not found")

    def set_speed(self, val):
        self.speed = float(val)
        self.status_label.configure(text=f"Speed set to {int(self.speed * 100)}%")

    def key_pressed(self, event):
        if event.char and event.char.lower() in 'wsqez':
            print("Pressed", event.char.upper())
            self.motion_start(event.char.upper())
        if event.char and event.char.lower() in 'ad':
            print("Pressed", event.char.upper())


    def motion_start(self, direction):
        if self.board is None or self.pins == {}:
            return
        if self.motion_thread and self.motion_thread.is_alive():
            return
        self.stop_motion = False
        self.motion_thread = threading.Thread(target=self._move, args=(direction,), daemon=True)
        self.motion_thread.start()

    def _move(self, direction):
        self.ramp_up_pwm(self.speed)
        if direction == 'W':  # Forward
            self.pins['IN1'].write(1)
            self.pins['IN2'].write(0)
            self.pins['IN3'].write(1)
            self.pins['IN4'].write(0)
        elif direction == 'Z':  # Backward
            self.pins['IN1'].write(0)
            self.pins['IN2'].write(1)
            self.pins['IN3'].write(0)
            self.pins['IN4'].write(1)
        elif direction == 'Q':  # Rotate CCW
            self.pins['IN1'].write(0)
            self.pins['IN2'].write(1)
            self.pins['IN3'].write(1)
            self.pins['IN4'].write(0)
        elif direction == 'E':  # Rotate CW
            self.pins['IN1'].write(1)
            self.pins['IN2'].write(0)
            self.pins['IN3'].write(0)
            self.pins['IN4'].write(1)

    def motion_stop(self):
        self.stop()
        self.stop_motion = True

    def ramp_up_pwm(self, target_speed, step=0.05, delay=0.05):
        current_speed = 0.0
        while current_speed < target_speed and not self.stop_motion:
            current_speed = min(current_speed + step, target_speed)
            self.pins['ENA'].write(current_speed)
            self.pins['ENB'].write(current_speed)
            time.sleep(delay)

    def stop(self):
        if self.pins:
            for pin in ['IN1', 'IN2', 'IN3', 'IN4']:
                self.pins[pin].write(0)
            self.pins['ENA'].write(0)
            self.pins['ENB'].write(0)

    def on_close(self):
        if self.board:
            self.stop()
            self.board.exit()
        self.destroy()


if __name__ == "__main__":
    app = MotorControlApp()
    app.mainloop()
