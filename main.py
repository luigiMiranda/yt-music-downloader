import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pytube import YouTube
import threading

# Variabile per memorizzare la cartella di destinazione
cartella_destinazione = ""

# Funzione per selezionare la cartella di destinazione
def seleziona_cartella():
    global cartella_destinazione
    cartella_destinazione = filedialog.askdirectory()
    if cartella_destinazione:
        label_cartella.config(text="Cartella di destinazione selezionata: " + cartella_destinazione)

# Funzione per scaricare il video
def scarica_video():
    global cartella_destinazione
    link_video = entry_link.get()
    
    if not cartella_destinazione:
        messagebox.showerror("Errore", "Seleziona prima la cartella di destinazione.")
        return
    if not link_video:
        messagebox.showerror("Errore", "Inserisci il link del video.")
        return
    try:
        # Disabilita il pulsante Scarica e l'entry durante il download
        btn_scarica.config(state="disabled")
        entry_link.config(state="disabled")
        # Mostra la barra di progresso indeterminata
        progress_bar.start()
        # Avvia il download del video in un thread separato
        threading.Thread(target=effettua_download, args=(link_video,)).start()
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore durante il download: {str(e)}")
        # Riabilita il pulsante Scarica e l'entry in caso di errore
        btn_scarica.config(state="normal")
        entry_link.config(state="normal")
        # Interrompi la barra di progresso
        progress_bar.stop()

# Funzione per effettuare il download del video
def effettua_download(link_video):
    global cartella_destinazione
    try:
        video = YouTube(link_video)
        stream = video.streams.filter(only_audio=True).first()
        stream.download(output_path=cartella_destinazione, filename=f"{video.title}.mp3")
        # Mostra il messaggio di completamento
        messagebox.showinfo("Download completato", "Il video è stato scaricato con successo!")
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore durante il download: {str(e)}")
    finally:
        # Riabilita il pulsante Scarica e l'entry dopo il download
        btn_scarica.config(state="normal")
        entry_link.config(state="normal")
        # Interrompi la barra di progresso
        progress_bar.stop()

# Creazione della finestra principale
root = tk.Tk()
root.geometry("600x600")
root.title("yt-dowloader")

# Creazione del pulsante per selezionare la cartella di destinazione
btn_seleziona_cartella = tk.Button(root, text="Seleziona Cartella", command=seleziona_cartella)
btn_seleziona_cartella.pack(pady=5)

# Label per visualizzare la cartella selezionata
label_cartella = tk.Label(root, text="Cartella di destinazione non selezionata")
label_cartella.pack(pady=5)

# Creazione della label
label_inserisci_link = tk.Label(root, text="Inserisci link del video:")
label_inserisci_link.pack(pady=10)

# Creazione del box di testo per l'inserimento del link
entry_link = tk.Entry(root, width=50)
entry_link.pack(pady=5)

# Creazione del pulsante per scaricare il video
btn_scarica = tk.Button(root, text="Scarica", command=scarica_video)
btn_scarica.pack(pady=10)

# Creazione della barra di progresso indeterminata
progress_bar = ttk.Progressbar(root, mode="indeterminate")
progress_bar.pack(pady=10)

# Esecuzione del loop principale
root.mainloop()
