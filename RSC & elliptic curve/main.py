import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import importlib.util


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicații Criptografice")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Centrul ecranului
        self.center_window()

        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        ttk.Label(main_frame, text="Aplicații Criptografice",
                  font=("Arial", 20, "bold")).pack(pady=20)

        # Descriere
        description = """Acest program conține două aplicații criptografice:
1. Criptosistem exponențial (RSA)
2. Criptografie pe curbe eliptice

Selectați aplicația dorită pentru a începe."""

        desc_label = ttk.Label(main_frame, text=description,
                               font=("Arial", 12), justify=tk.LEFT, wraplength=500)
        desc_label.pack(pady=20)

        # Frame pentru butoane
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Stiluri pentru butoane
        style = ttk.Style()
        style.configure('App.TButton', font=('Arial', 12), padding=10)

        # Butoane pentru aplicații
        ttk.Button(button_frame, text="1. Criptosistem Exponențial (RSA)",
                   style='App.TButton', command=self.open_rsa_app).pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="2. Criptografie pe Curbe Eliptice",
                   style='App.TButton', command=self.open_elliptic_curve_app).pack(fill=tk.X, pady=10)

        # Buton de ieșire
        ttk.Button(main_frame, text="Ieșire", command=root.destroy).pack(side=tk.BOTTOM, pady=10)

    def center_window(self):
        # Centrează fereastra pe ecran
        window_width = 600
        window_height = 500

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def open_rsa_app(self):
        # Importă și lansează aplicația RSA
        try:
            # Ascunde fereastra principală
            self.root.withdraw()

            # Creăm o nouă fereastră pentru aplicația RSA
            rsa_window = tk.Toplevel()

            # Importăm modulul RSA
            from rsa_encryption import RSAApp

            # Inițializăm aplicația RSA
            app = RSAApp(rsa_window)

            # Când se închide fereastra RSA, se redeschide fereastra principală
            rsa_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(rsa_window))

        except Exception as e:
            print(f"Eroare la lansarea aplicației RSA: {str(e)}")
            self.root.deiconify()  # Redeschide fereastra principală în caz de eroare

    def open_elliptic_curve_app(self):
        # Importă și lansează aplicația de criptografie pe curbe eliptice
        try:
            # Ascunde fereastra principală
            self.root.withdraw()

            # Creăm o nouă fereastră pentru aplicația de curbe eliptice
            ec_window = tk.Toplevel()

            # Importăm modulul de curbe eliptice
            from elliptic_curve_cryptography import EllipticCurveApp

            # Inițializăm aplicația de curbe eliptice
            app = EllipticCurveApp(ec_window)

            # Când se închide fereastra de curbe eliptice, se redeschide fereastra principală
            ec_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(ec_window))

        except Exception as e:
            print(f"Eroare la lansarea aplicației de curbe eliptice: {str(e)}")
            self.root.deiconify()  # Redeschide fereastra principală în caz de eroare

    def on_closing(self, window):
        # Închide fereastra aplicației și redeschidem fereastra principală
        window.destroy()
        self.root.deiconify()


if __name__ == "__main__":
    # Verifică dacă fișierele necesare există
    required_files = [
        "rsa_encryption.py",
        "elliptic_curve_cryptography.py"
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"EROARE: Următoarele fișiere lipsesc: {', '.join(missing_files)}")
        print("Vă rugăm să vă asigurați că toate fișierele sunt în același director.")
        sys.exit(1)

    # Inițializează aplicația principală
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()