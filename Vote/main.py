import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import base64
import os
import json
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import datetime
import uuid


class ElectronicVotingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem demonstrativ de vot electronic")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Date pentru simulare
        self.candidates = ["Candidat A", "Candidat B", "Candidat C", "Candidat D"]
        self.votes = {candidate: 0 for candidate in self.candidates}
        self.voters = {}  # {voter_id: {public_key, has_voted}}
        self.ballots = []  # [[encrypted_vote, signature, timestamp]]
        self.election_authority_private_key = None
        self.election_authority_public_key = None

        # Generare chei pentru autoritatea electorală
        self.generate_election_authority_keys()

        # Creare interfață
        self.create_interface()

        # Încărcare date salvate (dacă există)
        self.load_data()

    def generate_election_authority_keys(self):
        """Generează perechea de chei pentru autoritatea electorală"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.election_authority_private_key = private_key
        self.election_authority_public_key = private_key.public_key()

    def create_interface(self):
        """Creează interfața aplicației"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Notebook pentru taburi
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab pentru înregistrare votanți
        self.registration_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.registration_tab, text="Înregistrare Votanți")
        self.setup_registration_tab()

        # Tab pentru votare
        self.voting_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.voting_tab, text="Votare")
        self.setup_voting_tab()

        # Tab pentru statistici și rezultate
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Statistici și Rezultate")
        self.setup_stats_tab()

        # Tab pentru verificare și audit
        self.verification_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.verification_tab, text="Verificare și Audit")
        self.setup_verification_tab()

        # Tab pentru demonstrație criptografică
        self.crypto_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.crypto_tab, text="Demonstrație Criptografică")
        self.setup_crypto_tab()

    def setup_registration_tab(self):
        """Configurare tab de înregistrare votanți"""
        frame = ttk.LabelFrame(self.registration_tab, text="Înregistrare Alegător Nou")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Formulare pentru înregistrare
        ttk.Label(frame, text="Nume:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(frame, text="CNP:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cnp_entry = ttk.Entry(frame, width=30)
        self.cnp_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        register_btn = ttk.Button(frame, text="Înregistrează Alegător", command=self.register_voter)
        register_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # Afișare alegători înregistrați
        voters_frame = ttk.LabelFrame(self.registration_tab, text="Alegători Înregistrați")
        voters_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.voters_tree = ttk.Treeview(voters_frame, columns=("ID", "Nume", "Status"))
        self.voters_tree.heading("ID", text="ID Alegător")
        self.voters_tree.heading("Nume", text="Nume")
        self.voters_tree.heading("Status", text="Status")
        self.voters_tree.column("#0", width=0, stretch=tk.NO)
        self.voters_tree.column("ID", width=150)
        self.voters_tree.column("Nume", width=150)
        self.voters_tree.column("Status", width=100)
        self.voters_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_voting_tab(self):
        """Configurare tab de votare"""
        frame = ttk.LabelFrame(self.voting_tab, text="Cabină de Vot")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Autentificare alegător
        auth_frame = ttk.Frame(frame)
        auth_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(auth_frame, text="ID Alegător:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.voter_id_entry = ttk.Entry(auth_frame, width=30)
        self.voter_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        auth_btn = ttk.Button(auth_frame, text="Autentificare", command=self.authenticate_voter)
        auth_btn.grid(row=0, column=2, padx=5, pady=5)

        # Frame pentru selecția candidaților
        candidates_frame = ttk.LabelFrame(frame, text="Selectează Candidatul")
        candidates_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.candidate_var = tk.StringVar()

        for i, candidate in enumerate(self.candidates):
            rb = ttk.Radiobutton(candidates_frame, text=candidate, value=candidate, variable=self.candidate_var)
            rb.pack(anchor=tk.W, padx=20, pady=5)

        # Buton de vot
        vote_btn = ttk.Button(frame, text="Votează", command=self.cast_vote)
        vote_btn.pack(pady=20)

    def setup_stats_tab(self):
        """Configurare tab pentru statistici"""
        # Frame pentru grafic de tip bară
        bar_frame = ttk.LabelFrame(self.stats_tab, text="Rezultate Vot")
        bar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig_bar, self.ax_bar = plt.subplots(figsize=(8, 4))
        self.canvas_bar = FigureCanvasTkAgg(self.fig_bar, master=bar_frame)
        self.canvas_bar.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Frame pentru grafic de tip pie
        pie_frame = ttk.LabelFrame(self.stats_tab, text="Distribuția Voturilor")
        pie_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig_pie, self.ax_pie = plt.subplots(figsize=(6, 4))
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, master=pie_frame)
        self.canvas_pie.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Buton pentru actualizare statistici
        refresh_btn = ttk.Button(self.stats_tab, text="Actualizează Statistici", command=self.update_stats)
        refresh_btn.pack(pady=10)

        # Inițializare statistici
        self.update_stats()

    def setup_verification_tab(self):
        """Configurare tab pentru verificare și audit"""
        # Frame pentru verificare individuală a voturilor
        verify_frame = ttk.LabelFrame(self.verification_tab, text="Verifică Votul Tău")
        verify_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(verify_frame, text="ID Alegător:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.verify_id_entry = ttk.Entry(verify_frame, width=30)
        self.verify_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        verify_btn = ttk.Button(verify_frame, text="Verifică", command=self.verify_vote)
        verify_btn.grid(row=0, column=2, padx=5, pady=5)

        # Frame pentru log-uri de audit
        audit_frame = ttk.LabelFrame(self.verification_tab, text="Log-uri de Audit")
        audit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.audit_text = tk.Text(audit_frame, height=10, width=80)
        self.audit_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Buton pentru export date de audit
        export_btn = ttk.Button(self.verification_tab, text="Exportă Date Audit", command=self.export_audit_data)
        export_btn.pack(pady=10)

        # Inițializare log-uri de audit
        self.update_audit_logs()

    def setup_crypto_tab(self):
        """Configurare tab pentru demonstrație criptografică"""
        # Frame pentru explicații criptografice
        crypto_info_frame = ttk.LabelFrame(self.crypto_tab, text="Principii Criptografice în Votul Electronic")
        crypto_info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        info_text = """
        Sistemul nostru demonstrativ utilizează următoarele mecanisme criptografice:

        1. Criptare cu cheie publică (RSA) - protejează conținutul voturilor
           • Fiecare vot este criptat cu cheia publică a autorității electorale
           • Doar autoritatea electorală poate decripta voturile cu cheia privată

        2. Semnături digitale - asigură autenticitatea voturilor
           • Fiecare alegător are o pereche de chei (publică și privată)
           • Votul este semnat cu cheia privată a alegătorului
           • Oricine poate verifica semnătura cu cheia publică a alegătorului

        3. Hash-uri criptografice - asigură integritatea datelor
           • Hash-urile sunt folosite pentru a verifica că datele nu au fost modificate
           • Orice modificare a votului ar schimba valoarea hash-ului

        4. Verificabilitate end-to-end
           • Alegătorii pot verifica că votul lor a fost înregistrat corect
           • Sistemul păstrează anonimitatea, dar oferă dovezi criptografice
        """

        info_label = ttk.Label(crypto_info_frame, text=info_text, wraplength=900, justify=tk.LEFT)
        info_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame pentru demonstrație interactivă
        demo_frame = ttk.LabelFrame(self.crypto_tab, text="Demonstrație Interactivă")
        demo_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Demonstrație de criptare/decriptare
        ttk.Label(demo_frame, text="Mesaj pentru criptare:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.demo_message = ttk.Entry(demo_frame, width=40)
        self.demo_message.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.demo_message.insert(0, "Votul meu pentru candidatul X")

        encrypt_btn = ttk.Button(demo_frame, text="Criptează", command=self.demo_encrypt)
        encrypt_btn.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(demo_frame, text="Mesaj criptat:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.encrypted_text = tk.Text(demo_frame, height=5, width=60)
        self.encrypted_text.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)

        decrypt_btn = ttk.Button(demo_frame, text="Decriptează", command=self.demo_decrypt)
        decrypt_btn.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(demo_frame, text="Mesaj decriptat:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.decrypted_text = ttk.Entry(demo_frame, width=40)
        self.decrypted_text.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    def register_voter(self):
        """Înregistrează un nou alegător"""
        name = self.name_entry.get().strip()
        cnp = self.cnp_entry.get().strip()

        if not name or not cnp:
            messagebox.showerror("Eroare", "Completați toate câmpurile!")
            return

        if len(cnp) != 13 or not cnp.isdigit():
            messagebox.showerror("Eroare", "CNP-ul trebuie să aibă 13 cifre!")
            return

        # Generare ID alegător (în practică ar trebui să fie mai securizat)
        voter_id = str(uuid.uuid4())[:8]

        # Generare cheie privată și publică pentru alegător
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Salvare date alegător
        self.voters[voter_id] = {
            "name": name,
            "cnp_hash": hashlib.sha256(cnp.encode()).hexdigest(),  # Stocăm doar hash-ul CNP-ului
            "public_key": public_key,
            "private_key": private_key,  # În realitate, cheia privată ar rămâne la alegător
            "has_voted": False,
            "registration_time": datetime.datetime.now().isoformat()
        }

        # Adăugare în interfață
        self.voters_tree.insert("", tk.END, values=(voter_id, name, "Neexprimat"))

        # Resetare formulare
        self.name_entry.delete(0, tk.END)
        self.cnp_entry.delete(0, tk.END)

        # Salvare date
        self.save_data()

        messagebox.showinfo("Succes",
                            f"Alegător înregistrat cu succes!\nID Alegător: {voter_id}\n\nPăstrați acest ID pentru a putea vota!")

    def authenticate_voter(self):
        """Autentifică un alegător existent"""
        voter_id = self.voter_id_entry.get().strip()

        if not voter_id:
            messagebox.showerror("Eroare", "Introduceți ID-ul alegătorului!")
            return

        if voter_id not in self.voters:
            messagebox.showerror("Eroare", "ID alegător invalid!")
            return

        if self.voters[voter_id]["has_voted"]:
            messagebox.showerror("Eroare", "Acest alegător a votat deja!")
            return

        # Simulare autentificare cu PIN/CNP (în realitate ar fi mai complex)
        pin = simpledialog.askstring("Autentificare", "Introduceți ultimele 4 cifre din CNP:", parent=self.root)
        if not pin:
            return

        messagebox.showinfo("Succes",
                            f"Autentificare reușită pentru alegătorul {self.voters[voter_id]['name']}.\nPuteți vota acum.")

    def cast_vote(self):
        """Înregistrează votul alegătorului"""
        voter_id = self.voter_id_entry.get().strip()
        selected_candidate = self.candidate_var.get()

        if not voter_id:
            messagebox.showerror("Eroare", "Vă rugăm să vă autentificați mai întâi!")
            return

        if voter_id not in self.voters:
            messagebox.showerror("Eroare", "ID alegător invalid!")
            return

        if self.voters[voter_id]["has_voted"]:
            messagebox.showerror("Eroare", "Acest alegător a votat deja!")
            return

        if not selected_candidate:
            messagebox.showerror("Eroare", "Vă rugăm să selectați un candidat!")
            return

        # Criptare vot
        vote_data = selected_candidate.encode()
        encrypted_vote = self.election_authority_public_key.encrypt(
            vote_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Semnare vot (pentru a dovedi autenticitatea)
        signature = self.voters[voter_id]["private_key"].sign(
            encrypted_vote,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Înregistrare vot
        timestamp = datetime.datetime.now().isoformat()
        ballot = {
            "encrypted_vote": base64.b64encode(encrypted_vote).decode(),
            "signature": base64.b64encode(signature).decode(),
            "voter_id": voter_id,
            "timestamp": timestamp
        }
        self.ballots.append(ballot)

        # Actualizare status alegător
        self.voters[voter_id]["has_voted"] = True
        self.voters[voter_id]["vote_time"] = timestamp

        # Decodificare vot pentru simulare (în realitate s-ar face la numărarea voturilor)
        decrypted_vote = self.election_authority_private_key.decrypt(
            encrypted_vote,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

        # Actualizare numărătoare voturi
        self.votes[decrypted_vote] += 1

        # Actualizare interfață
        for item in self.voters_tree.get_children():
            if self.voters_tree.item(item)["values"][0] == voter_id:
                self.voters_tree.item(item, values=(voter_id, self.voters[voter_id]["name"], "Exprimat"))
                break

        # Actualizare statistici
        self.update_stats()
        self.update_audit_logs()

        # Salvare date
        self.save_data()

        # Resetare formular
        self.voter_id_entry.delete(0, tk.END)
        self.candidate_var.set("")

        messagebox.showinfo("Succes", "Vot înregistrat cu succes!")

    def update_stats(self):
        """Actualizează graficele statistice"""
        # Curățare grafice existente
        self.ax_bar.clear()
        self.ax_pie.clear()

        # Pregătire date
        candidates = list(self.votes.keys())
        vote_counts = list(self.votes.values())

        # Grafic de tip bară
        self.ax_bar.bar(candidates, vote_counts, color='skyblue')
        self.ax_bar.set_ylabel('Număr de voturi')
        self.ax_bar.set_title('Rezultate Alegeri')

        # Adăugare etichete cu valori
        for i, count in enumerate(vote_counts):
            self.ax_bar.text(i, count + 0.1, str(count), ha='center')

        # Grafic de tip pie
        if sum(vote_counts) > 0:  # Verificare dacă există voturi
            self.ax_pie.pie(vote_counts, labels=candidates, autopct='%1.1f%%', startangle=90,
                            colors=plt.cm.tab10.colors)
            self.ax_pie.set_title('Distribuția Voturilor')
        else:
            self.ax_pie.text(0.5, 0.5, 'Nu există voturi înregistrate', ha='center', va='center')
            self.ax_pie.set_title('Distribuția Voturilor')

        # Actualizare grafice
        self.canvas_bar.draw()
        self.canvas_pie.draw()

    def verify_vote(self):
        """Verifică dacă votul unui alegător a fost înregistrat corect"""
        voter_id = self.verify_id_entry.get().strip()

        if not voter_id:
            messagebox.showerror("Eroare", "Introduceți ID-ul alegătorului!")
            return

        if voter_id not in self.voters:
            messagebox.showerror("Eroare", "ID alegător invalid!")
            return

        if not self.voters[voter_id]["has_voted"]:
            messagebox.showinfo("Verificare", "Acest alegător nu a votat încă.")
            return

        # Căutare buletin de vot
        voter_ballot = None
        for ballot in self.ballots:
            if ballot["voter_id"] == voter_id:
                voter_ballot = ballot
                break

        if not voter_ballot:
            messagebox.showerror("Eroare", "Nu s-a găsit buletinul de vot pentru acest alegător!")
            return

        # Verificare semnătură
        try:
            encrypted_vote = base64.b64decode(voter_ballot["encrypted_vote"])
            signature = base64.b64decode(voter_ballot["signature"])

            self.voters[voter_id]["public_key"].verify(
                signature,
                encrypted_vote,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            # Afișare timestamp vot
            vote_time = datetime.datetime.fromisoformat(voter_ballot["timestamp"])

            messagebox.showinfo(
                "Verificare reușită",
                f"Votul alegătorului {self.voters[voter_id]['name']} a fost înregistrat corect.\n\n"
                f"Data și ora votului: {vote_time.strftime('%d-%m-%Y %H:%M:%S')}\n\n"
                "Votul dvs. este criptat și confidențial, dar este înregistrat în sistem."
            )

        except Exception as e:
            messagebox.showerror("Eroare de verificare", f"Votul nu poate fi verificat: {str(e)}")

    def update_audit_logs(self):
        """Actualizează log-urile de audit"""
        self.audit_text.delete(1.0, tk.END)

        # Statistici generale
        total_registered = len(self.voters)
        total_voted = sum(1 for voter in self.voters.values() if voter["has_voted"])
        participation_rate = (total_voted / total_registered * 100) if total_registered > 0 else 0

        audit_text = f"--- STATISTICI GENERALE ---\n"
        audit_text += f"Alegători înregistrați: {total_registered}\n"
        audit_text += f"Voturi exprimate: {total_voted}\n"
        audit_text += f"Rata de participare: {participation_rate:.2f}%\n\n"

        audit_text += f"--- REZULTATE ALEGERI ---\n"
        for candidate, count in self.votes.items():
            percentage = (count / total_voted * 100) if total_voted > 0 else 0
            audit_text += f"{candidate}: {count} voturi ({percentage:.2f}%)\n"

        audit_text += f"\n--- ISTORIC EVENIMENTE ---\n"
        # Sortare buletine de vot după timestamp
        sorted_ballots = sorted(self.ballots, key=lambda x: x["timestamp"])

        for ballot in sorted_ballots:
            timestamp = datetime.datetime.fromisoformat(ballot["timestamp"])
            voter_id = ballot["voter_id"]
            voter_name = self.voters[voter_id]["name"]
            audit_text += f"{timestamp.strftime('%d-%m-%Y %H:%M:%S')} - Vot înregistrat pentru {voter_name} (ID: {voter_id[:4]}...)\n"

        self.audit_text.insert(tk.END, audit_text)

    def export_audit_data(self):
        """Exportă datele de audit într-un fișier"""
        # Pregătire date pentru export
        export_data = {
            "election_info": {
                "title": "Simulare Vot Electronic",
                "timestamp": datetime.datetime.now().isoformat(),
                "total_registered": len(self.voters),
                "total_voted": sum(1 for voter in self.voters.values() if voter["has_voted"])
            },
            "results": self.votes,
            "ballots": [
                {
                    "timestamp": ballot["timestamp"],
                    "voter_id": ballot["voter_id"][:4] + "..."  # Trunchiere ID pentru confidențialitate
                }
                for ballot in self.ballots
            ]
        }

        # Salvare în fișier JSON
        try:
            with open("audit_export.json", "w") as f:
                json.dump(export_data, f, indent=4)
            messagebox.showinfo("Export", "Datele de audit au fost exportate în fișierul audit_export.json")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la exportul datelor: {str(e)}")

    def demo_encrypt(self):
        """Demonstrație de criptare"""
        message = self.demo_message.get().strip()
        if not message:
            messagebox.showerror("Eroare", "Introduceți un mesaj pentru criptare!")
            return

        # Criptare mesaj
        encrypted = self.election_authority_public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Afișare mesaj criptat (în format base64)
        self.encrypted_text.delete(1.0, tk.END)
        self.encrypted_text.insert(tk.END, base64.b64encode(encrypted).decode())

        # Salvare mesaj criptat pentru decriptare ulterioară
        self.demo_encrypted = encrypted

    def demo_decrypt(self):
        """Demonstrație de decriptare"""
        if not hasattr(self, 'demo_encrypted'):
            messagebox.showerror("Eroare", "Criptați mai întâi un mesaj!")
            return

        # Decriptare mesaj
        decrypted = self.election_authority_private_key.decrypt(
            self.demo_encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

        # Afișare mesaj decriptat
        self.decrypted_text.delete(0, tk.END)
        self.decrypted_text.insert(0, decrypted)

    def save_data(self):
        """Salvează datele aplicației"""
        # În această implementare demonstrativă, datele nu sunt persistente între sesiuni
        # Într-o aplicație reală, ar trebui utilizată o bază de date securizată
        pass

    def load_data(self):
        """Încarcă datele aplicației"""
        # În această implementare demonstrativă, datele nu sunt persistente între sesiuni
        pass


def main():
    root = tk.Tk()
    app = ElectronicVotingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()