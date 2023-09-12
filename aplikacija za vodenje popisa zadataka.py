import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Aplikacija:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacija za vođenje popisa zadataka")

        self.conn = sqlite3.connect('zadaci.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS zadaci (id INTEGER PRIMARY KEY, naziv_zadatka TEXT, rok TEXT)')
        self.conn.commit()

        self.labela_naziv_zadatka = tk.Label(root, text="Naziv zadatka:")
        self.labela_naziv_zadatka.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.unos_naziv_zadatka = tk.Entry(root)
        self.unos_naziv_zadatka.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.labela_rok = tk.Label(root, text="Rok (DD-MM-YYYY):")
        self.labela_rok.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.unos_rok = tk.Entry(root)
        self.unos_rok.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.gumb_dodaj = tk.Button(root, text="Dodaj zadatak", command=self.dodaj_zadatak)
        self.gumb_dodaj.grid(row=2, columnspan=2, padx=10, pady=5)

        self.okvir_zadaci = tk.Frame(root)
        self.okvir_zadaci.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.gumbi_brisi = []
        self.osvjezi_listu()

    def dodaj_zadatak(self):
        naziv_zadatka = self.unos_naziv_zadatka.get()
        rok = self.unos_rok.get()

        if naziv_zadatka and self.rok(rok):
            self.cursor.execute('INSERT INTO zadaci (naziv_zadatka, rok) VALUES (?, ?)', (naziv_zadatka, rok))
            self.conn.commit()
            self.osvjezi_listu()
            self.unos_naziv_zadatka.delete(0, tk.END)
            self.unos_rok.delete(0, tk.END)
        else:
            if not naziv_zadatka:
                messagebox.showwarning("Upozorenje", "Molimo unesite naziv zadatka.")
            else:
                messagebox.showwarning("Upozorenje", "Neispravan format datuma. Format: DD-MM-YYYY")

    def obrisi_zadatak(self, zadatak_id):
        self.cursor.execute('DELETE FROM zadaci WHERE id = ?', (zadatak_id,))
        self.conn.commit()
        self.osvjezi_listu()

    def rok(self, datum_string):
        try:
            datetime.strptime(datum_string, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def osvjezi_listu(self):
        for widget in self.okvir_zadaci.winfo_children():
            widget.destroy()

        self.gumbi_brisi = []

        self.cursor.execute('SELECT * FROM zadaci')
        zadaci = self.cursor.fetchall()
        for redak, zadatak in enumerate(zadaci):
            naziv_zadatka = zadatak[1]
            labela_naziv_zadatka = tk.Label(self.okvir_zadaci, text=naziv_zadatka, fg='green')
            labela_naziv_zadatka.grid(row=redak, column=0, padx=5, pady=2, sticky="w")

            rok = zadatak[2]
            labela_rok = tk.Label(self.okvir_zadaci, text=rok, fg='red')
            labela_rok.grid(row=redak, column=1, padx=5, pady=2, sticky="w")

            gumb_obrisi = tk.Button(self.okvir_zadaci, text="Obriši", command=lambda zadatak_id=zadatak[0]: self.obrisi_zadatak(zadatak_id))
            gumb_obrisi.grid(row=redak, column=2, padx=5, pady=2, sticky="e")

            self.gumbi_brisi.append(gumb_obrisi)

if __name__ == '__main__':
    root = tk.Tk()
    aplikacija = Aplikacija(root)
    root.mainloop()

    aplikacija.conn.close()