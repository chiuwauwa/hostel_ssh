import tkinter as tk
from tkinter import messagebox
import paramiko


class SSHClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel")
        self.root.geometry("600x300")

        self.connection_status = tk.StringVar()
        self.connection_status.set("Нет активного подключения")
        self.connection_label = tk.Label(self.root, textvariable=self.connection_status)
        self.connection_label.pack(fill=tk.BOTH, expand=True)

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

        self.disconnect_button = tk.Button(self.root, text="Отключить соединение",
                                           command=self.disconnect_ssh)
        self.disconnect_button.pack(fill=tk.BOTH, expand=True)

        self.shutdown_button = tk.Button(self.root, text="Выключить компьютер",
                                         command=self.shutdown, bg="red")
        self.shutdown_button.pack(fill=tk.BOTH, expand=True)

        self.ssh_client = None

    def set_connection_status(self, status):
        self.connection_status.set(status)

    def play_intro(self):
        if self.ssh_client:
            try:
                # Запускаем воспроизведение аудио intro.mp3 на удаленной машине
                self.ssh_client.exec_command("cvlc intro.mp3")
            except Exception as e:
                messagebox.showerror("Ошибка SSH", f"Произошла ошибка при выполнении команды: {str(e)}")
        else:
            messagebox.showerror("Ошибка SSH", "Пожалуйста, сначала установите SSH соединение.")

    def muter(self):
        if self.ssh_client:
            try:
                # Запускаем воспроизведение аудио muter.mp3 на удаленной машине
                self.ssh_client.exec_command("cvlc muter.mp3 -R")
            except Exception as e:
                messagebox.showerror("Ошибка SSH", f"Произошла ошибка при выполнении команды: {str(e)}")
        else:
            messagebox.showerror("Ошибка SSH", "Пожалуйста, сначала установите SSH соединение.")

    def stop_playback(self):
        if self.ssh_client:
            try:
                # Останавливаем воспроизведение через VLC
                self.ssh_client.exec_command("pkill vlc")
            except Exception as e:
                messagebox.showerror("Ошибка SSH", f"Произошла ошибка при выполнении команды: {str(e)}")
        else:
            messagebox.showerror("Ошибка SSH", "Пожалуйста, сначала установите SSH соединение.")

    def shutdown(self):
        result = messagebox.askokcancel("Выключение", "Вы уверены, что хотите выключить компьютер?")
        if result:
            if self.ssh_client:
                try:
                    # Выполняем команду выключения компьютера через SSH
                    self.ssh_client.exec_command("sudo shutdown -h now")
                except Exception as e:
                    messagebox.showerror("Ошибка SSH", f"Произошла ошибка при выполнении команды: {str(e)}")
            else:
                messagebox.showerror("Ошибка SSH", "Пожалуйста, сначала установите SSH соединение.")

    def disconnect_ssh(self):
        if self.ssh_client:
            try:
                # Закрываем SSH соединение
                self.ssh_client.close()
                self.ssh_client = None
                self.set_connection_status("Нет активного подключения")
            except Exception as e:
                messagebox.showerror("Ошибка SSH", f"Произошла ошибка при отключении: {str(e)}")
        else:
            messagebox.showerror("Ошибка SSH", "Нет активного SSH соединения.")

    def connect_ssh(self):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect('192.168.1.125', username='hostel', password='hostel123')
            self.set_connection_status("Соединение успешно установлено")
        except Exception as e:
            messagebox.showerror("Ошибка соединения", f"Произошла ошибка: {str(e)}")
            self.set_connection_status("Ошибка соединения")

    def get_home_directory(self):
        stdin, stdout, stderr = self.ssh_client.exec_command("echo $HOME")
        return stdout.read().decode().strip()


if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClientApp(root)

    root.iconbitmap("hostel.ico")
    def on_closing():
        if app.ssh_client:
            app.shutdown()
            root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
