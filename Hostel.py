import tkinter as tk
from tkinter import messagebox
import paramiko


class SSHClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel")
        self.root.geometry("400x200")

        self.connect_button = tk.Button(self.root, text="Подключиться к компу",
                                        command=self.connect_ssh, bg="green")
        self.connect_button.pack(fill=tk.BOTH, expand=True)

        self.mute_button = tk.Button(self.root, text="Играть Muter",
                                     command=self.muter)
        self.mute_button.pack(fill=tk.BOTH, expand=True)

        self.stop_button = tk.Button(self.root, text="Остановить музыку",
                                     command=self.stop_playback)
        self.stop_button.pack(fill=tk.BOTH, expand=True)

        self.intro_button = tk.Button(self.root, text="Играть Intro",
                                      command=self.play_intro)
        self.intro_button.pack(fill=tk.BOTH, expand=True)

        # Добавляем пустое место между кнопками
        self.empty_label = tk.Label(self.root, text="")
        self.empty_label.pack(fill=tk.BOTH, expand=True)

        self.shutdown_button = tk.Button(self.root, text="Выключить компьютер",
                                         command=self.shutdown, bg="red")
        self.shutdown_button.pack(fill=tk.BOTH, expand=True)

        self.ssh_client = None

    def play_intro(self):
        if self.ssh_client:
            try:
                # Выполняем команду воспроизведения аудио через SSH
                stdin, stdout, stderr = self.ssh_client.exec_command("nvlc intro.mp3")
            except Exception as e:
                messagebox.showerror("Ошибка SSH",
                                     f"Произошла ошибка при выполнении команды: {str(e)}")
        else:
            messagebox.showerror("Ошибка SSH",
                                 "Пожалуйста, сначала установите SSH соединение.")

    def muter(self):
        if self.ssh_client:
            try:
                # Выполняем команду воспроизведения аудио muter через SSH
                stdin, stdout, stderr = self.ssh_client.exec_command("nvlc muter.mp3 -R")
            except Exception as e:
                messagebox.showerror("Ошибка SSH",
                                     f"Произошла ошибка при выполнении команды: {str(e)}")
        else:
            messagebox.showerror("Ошибка SSH",
                                 "Пожалуйста, сначала установите SSH соединение.")

    def stop_playback(self):
        if self.ssh_client:
            try:
                # Выполняем команду остановки воспроизведения аудио через SSH
                stdin, stdout, stderr = self.ssh_client.exec_command("pkill nvlc")
            except Exception as e:
                messagebox.showerror("Ошибка SSH",
                                     f"Произошла ошибка при выполнении команды: {str(e)}")
        else:
            messagebox.showerror("Ошибка SSH",
                                 "Пожалуйста, сначала установите SSH соединение.")

    def shutdown(self):
        result = messagebox.askokcancel("Выключение",
                                        "Вы уверены, что хотите выключить компьютер?")
        if result:
            if self.ssh_client:
                try:
                    # Выполняем команду выключения компьютера через SSH
                    stdin, stdout, stderr = self.ssh_client.exec_command("sudo shutdown -h now")
                except Exception as e:
                    messagebox.showerror("Ошибка SSH",
                                         f"Произошла ошибка при выполнении команды: {str(e)}")
            else:
                messagebox.showerror("Ошибка SSH",
                                     "Пожалуйста, сначала установите SSH соединение.")

    def connect_ssh(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect('192.168.1.125', username='hostel', password='hostel123')
            messagebox.showinfo("Соединение", "Соединение успешно установлено!")
        except Exception as e:
            messagebox.showerror("Ошибка соединения", f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClientApp(root)
    root.mainloop()
