import tkinter as tk
import socket
import threading

class App:
    def __init__(self):
        self.stop_flag = False
        self.root = tk.Tk()
        self.root.title("Приложение")
        self.root.geometry("500x500")

        # Создание полей ввода
        self.ip_label = tk.Label(self.root, text="IP-адрес:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        self.port_label = tk.Label(self.root, text="Номер порта:")
        self.port_label.pack()
        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        self.device_label = tk.Label(self.root, text="Номер прибора:")
        self.device_label.pack()
        self.device_entry = tk.Entry(self.root)
        self.device_entry.pack()

        # Создание кнопок "Старт" и "Стоп"
        self.start_button = tk.Button(self.root, text="Старт", command=self.start_scanning)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Стоп", command=self.stop_scanning, state=tk.DISABLED)
        self.stop_button.pack()

        # Создание окна логгирования
        self.log_window = tk.Text(self.root)
        self.log_window.pack()

        self.root.mainloop()

    def start_scanning(self):
        self.stop_flag = False
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        device = self.device_entry.get()

        self.log_window.insert(tk.END, f"Начало сканирования порта {port} для прибора {device} на IP-адресе {ip}\n")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((ip, port))
        except Exception as e:
            self.log_window.insert(tk.END, f"Ошибка при соединении с портом: {e}\n")
            self.stop_scanning()
            return

        sock.send(device.encode())
        response = sock.recv(1024).decode()

        if response != "OK":
            self.log_window.insert(tk.END, f"Ошибка получения ответа: {response}\n")
            self.stop_scanning()
            return

        while not self.stop_flag:
            try:
                data = sock.recv(1024).decode()
                self.log_window.insert(tk.END, f"Получено сообщение: {data}\n")
            except socket.timeout:
                pass

        sock.close()

    def stop_scanning(self):
        self.log_window.insert(tk.END, "Остановка сканирования порта...\n")
        self.stop_flag = True
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = App()
