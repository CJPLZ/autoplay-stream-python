import tkinter as tk
from tkinter import simpledialog
from player import StreamPlayer
from connection import ConnectionManager
from storage import URLStorage
import threading

class StreamPlayerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reproductor de Streaming")
        self.root.geometry("400x300")
        self.root.configure(bg="#2E2E2E")

        self.player = StreamPlayer()
        self.stream_url = URLStorage.load_url()

        self.create_widgets()
        self.setup_connection_manager()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Reproductor de Streaming", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 18))
        title_label.pack(pady=10)

        self.connection_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.connection_frame.pack(pady=10)

        self.connection_indicator = tk.Label(self.connection_frame, width=2, height=1, bg="red")
        self.connection_indicator.pack(side=tk.LEFT)

        self.connection_status_label = tk.Label(self.connection_frame, text="Sin conexión a Internet", bg="#2E2E2E", fg="red", font=("Helvetica", 12))
        self.connection_status_label.pack(side=tk.LEFT, padx=5)

        self.stream_status_label = tk.Label(self.root, text="Desconectado del stream", bg="#2E2E2E", fg="red", font=("Helvetica", 12))
        self.stream_status_label.pack(pady=5)

        if self.stream_url:
            self.player.play_stream(self.stream_url)
        else:
            url_input = simpledialog.askstring("Input", "Por favor, ingresa la URL del stream:", parent=self.root)
            if url_input:
                URLStorage.save_url(url_input)
                self.player.play_stream(url_input)

        control_frame = tk.Frame(self.root, bg="#2E2E2E")
        control_frame.pack(pady=10)

        # Inicializa el botón de play/pause como "Pause"
        self.play_pause_button = tk.Button(control_frame, text="Pause", command=self.toggle_play_pause, bg="#4CAF50", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        stop_button = tk.Button(control_frame, text="Stop", command=self.close_app, bg="#FF0000", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
        stop_button.pack(side=tk.LEFT, padx=5)

        volume_slider = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.player.set_volume, bg="#2E2E2E", fg="#FFFFFF")
        volume_slider.set(50)
        volume_slider.pack(side=tk.LEFT, padx=5)

    def setup_connection_manager(self):
        self.connection_manager = ConnectionManager(self.player, self.stream_url)
        self.connection_thread = threading.Thread(target=self.connection_manager.monitor_connection, args=(self.update_connection_status,))
        self.connection_thread.daemon = True
        self.connection_thread.start()

    def update_connection_status(self, internet_connected, stream_connected):
        if internet_connected:
            self.connection_indicator.config(bg="green")
            self.connection_status_label.config(text="Conectado a Internet", fg="green")
        else:
            self.connection_indicator.config(bg="red")
            self.connection_status_label.config(text="Sin conexión a Internet", fg="red")
            stream_connected = False  # Si no hay internet, el stream no puede estar conectado

        if stream_connected:
            self.stream_status_label.config(text="Conectado al stream", fg="green")
        else:
            self.stream_status_label.config(text="Desconectado del stream", fg="red")

    def toggle_play_pause(self):
        new_text = self.player.toggle_play_pause()
        self.play_pause_button.config(text=new_text)

    def change_url(self):
        url_input = simpledialog.askstring("Input", "Por favor, ingresa la URL del stream:", parent=self.root)
        if url_input:
            URLStorage.save_url(url_input)
            self.player.play_stream(url_input)

    def close_app(self):
        self.player.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()