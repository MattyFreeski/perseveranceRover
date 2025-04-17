import customtkinter as ctk
from pyfirmata2 import Arduino
import serial.tools.list_ports
import threading
import time

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def find_hc05_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'cu.HC-05' in port.device:
            return port.device
    return None


class MotorControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HW-095 Motor Controller")
        self.geometry("550x420")

        self.board = None
        self.pins = {}
        self.speed = 1.0  # Default speed = 100%

        self.status_label = ctk.CTkLabel(self, text="Connecting to HC-05...", font=("Arial", 16))
        self.status_label.pack(pady=20)

        # Control Buttons
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.pack(pady=10)

        self.forward_btn = ctk.CTkButton(self.controls_frame, text="↑ Forward", command=self.move_forward, state="disabled", width=120)
        self.forward_btn.grid(row=0, column=1, padx=5, pady=5)

        self.rotate_left_btn = ctk.CTkButton(self.controls_frame, text="⟲ Rotate CCW", command=self.rotate_ccw, state="disabled", width=120)
        self.rotate_left_btn.grid(row=1, column=0, padx=5, pady=5)

        self.stop_btn = ctk.CTkButton(self.controls_frame, text="■ Stop", command=self.stop, state="disabled", width=120)
        self.stop_btn.grid(row=1, column=1, padx=5, pady=5)

        self.rotate_right_btn = ctk.CTkButton(self.controls_frame, text="⟳ Rotate CW", command=self.rotate_cw, state="disabled", width=120)
        self.rotate_right_btn.grid(row=1, column=2, padx=5, pady=5)

        self.backward_btn = ctk.CTkButton(self.controls_frame, text="↓ Backward", command=self.move_backward, state="disabled", width=120)
        self.backward_btn.grid(row=2, column=1, padx=5, pady=5)

        # Speed Control Buttons
        self.speed_frame = ctk.CTkFrame(self)
        self.speed_frame.pack(pady=10)

        ctk.CTkLabel(self.speed_frame, text="Speed Control:").grid(row=0, column=0, padx=10)

        self.speed_30_btn = ctk.CTkButton(self.speed_frame, text="30%", command=lambda: self.set_speed(0.3), width=80)
        self.speed_30_btn.grid(row=0, column=1, padx=5)

        self.speed_60_btn = ctk.CTkButton(self.speed_frame, text="60%", command=lambda: self.set_speed(0.6), width=80)
        self.speed_60_btn.grid(row=0, column=2, padx=5)

        self.speed_100_btn = ctk.CTkButton(self.speed_frame, text="100%", command=lambda: self.set_speed(1.0), width=80)
        self.speed_100_btn.grid(row=0, column=3, padx=5)

        self.exit_btn = ctk.CTkButton(self, text="Exit", command=self.on_close)
        self.exit_btn.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Connect in background
        threading.Thread(target=self.connect_to_board, daemon=True).start()

    def connect_to_board(self):
        port = find_hc05_port()
        if port:
            self.board = Arduino(port)

            self.pins = {
                'ENA': self.board.get_pin('d:11:p'),  # PWM
                'ENB': self.board.get_pin('d:6:p'),   # PWM
                'IN1': self.board.get_pin('d:13:o'),
                'IN2': self.board.get_pin('d:12:o'),
                'IN3': self.board.get_pin('d:10:o'),
                'IN4': self.board.get_pin('d:9:o'),
            }

            self.status_label.configure(text=f"Connected: {port}")
            for btn in [self.forward_btn, self.backward_btn, self.rotate_left_btn,
                        self.rotate_right_btn, self.stop_btn]:
                btn.configure(state="normal")
        else:
            self.status_label.configure(text="⚠️ HC-05 not found")

    def set_speed(self, value):
        self.speed = value
        self.status_label.configure(text=f"Speed set to {int(self.speed * 100)}%")

    def ramp_up_pwm(self, target_speed, step=0.05, delay=0.05):
        """Gradually increase PWM to target_speed."""
        current_speed = 0.0
        while current_speed < target_speed:
            current_speed = min(current_speed + step, target_speed)
            self.pins['ENA'].write(current_speed)
            self.pins['ENB'].write(current_speed)
            time.sleep(delay)

    def move_forward(self):
        self.pins['IN1'].write(1)
        self.pins['IN2'].write(0)
        self.pins['IN3'].write(1)
        self.pins['IN4'].write(0)
        threading.Thread(target=self.ramp_up_pwm, args=(self.speed,), daemon=True).start()

    def move_backward(self):
        self.pins['IN1'].write(0)
        self.pins['IN2'].write(1)
        self.pins['IN3'].write(0)
        self.pins['IN4'].write(1)
        threading.Thread(target=self.ramp_up_pwm, args=(self.speed,), daemon=True).start()

    def rotate_cw(self):
        self.pins['IN1'].write(1)
        self.pins['IN2'].write(0)
        self.pins['IN3'].write(0)
        self.pins['IN4'].write(1)
        threading.Thread(target=self.ramp_up_pwm, args=(self.speed,), daemon=True).start()

    def rotate_ccw(self):
        self.pins['IN1'].write(0)
        self.pins['IN2'].write(1)
        self.pins['IN3'].write(1)
        self.pins['IN4'].write(0)
        threading.Thread(target=self.ramp_up_pwm, args=(self.speed,), daemon=True).start()

    def stop(self):
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
