import os
import re
import collections

# --- CONFIGURAZIONE ---
# Modifica questa riga con il percorso completo della cartella contenente i tuoi giochi.
# Esempio per Windows: "C:\\Users\\TuoNome\\Documents\\ROMs\\PS1"
# Esempio per Linux/Mac: "/home/TuoNome/ROMs/PS1"
cartella_rom = "." # Il punto "." indica la cartella corrente in cui si trova lo script

# Imposta su True per simulare l'operazione senza modificare i file.
# Verrà creato un file "report_simulazione.txt" con le azioni previste.
# Imposta su False per eseguire effettivamente la creazione dei file e la ridenominazione.
simulazione = True

# --- SCRIPT (non modificare sotto questa linea se non sai cosa stai facendo) ---

def crea_playlist_m3u(directory, simulare=False):
    """
    Scansiona una directory, identifica i giochi multi-disco, crea i file .m3u
    e rinomina i file dei dischi individuali.
    Può operare in modalità reale o di simulazione.
    """
    # Regex aggiornata per trovare "(Disc X)" in qualsiasi punto del nome del file.
    # Funziona con "Disc", "Disk", spazi variabili e non è sensibile alle maiuscole/minuscole.
    pattern_multidisco = re.compile(r'^(.*?)\s*\((?:Disc|Disk)\s*(\d+)\)(.*)\.(chd|cue)$', re.IGNORECASE)

    # Dizionario per raggruppare i dischi per nome del gioco
    giochi = collections.defaultdict(list)
    log_simulazione = []

    if simulare:
        print("--- MODALITÀ SIMULAZIONE ATTIVA ---")
        print("Nessun file verrà modificato. Verrà generato un report.")
    
    print(f"\n--- Scansione della cartella: {os.path.abspath(directory)} ---")

    # 1. Raccoglie e raggruppa tutti i file dei dischi
    for nome_file in os.listdir(directory):
        percorso_completo = os.path.join(directory, nome_file)
        if os.path.isfile(percorso_completo):
            match = pattern_multidisco.match(nome_file)
            if match:
                parte1 = match.group(1).strip()
                numero_disco = int(match.group(2))
                parte2 = match.group(3).strip()
                estensione = match.group(4)
                
                nome_base = f"{parte1} {parte2}".strip()
                nome_base = re.sub(r'\s+', ' ', nome_base)
                
                giochi[nome_base].append({
                    'numero_disco': numero_disco,
                    'nome_file_originale': nome_file,
                    'estensione': estensione
                })

    if not giochi:
        print("Nessun file di gioco multi-disco trovato. Assicurati che i file seguano il formato 'Nome Gioco (Disc X).chd'.")
        return

    print(f"\nTrovati {len(giochi)} potenziali giochi multi-disco. Inizio l'elaborazione...\n")

    # 2. Elabora ogni gioco raggruppato
    giochi_elaborati = 0
    for nome_base, dischi in giochi.items():
        if len(dischi) > 1:
            giochi_elaborati += 1
            messaggio_elaborazione = f"--- Elaborazione di: {nome_base} ---"
            print(messaggio_elaborazione)
            if simulare:
                log_simulazione.append(messaggio_elaborazione)

            dischi_ordinati = sorted(dischi, key=lambda d: d['numero_disco'])
            nome_file_m3u = f"{nome_base}.m3u"
            
            # Prepara la lista dei nuovi nomi file che verranno usati sia per l'm3u sia per la ridenominazione
            nuovi_nomi_file = [f"{d['nome_file_originale']}.cd{d['numero_disco']}" for d in dischi_ordinati]

            # 3. Crea il file .m3u o registra l'azione per la simulazione
            if simulare:
                log_simulazione.append(f"[CREAZIONE PLAYLIST] -> {nome_file_m3u}")
                for nuovo_nome in nuovi_nomi_file:
                    log_simulazione.append(f"  -> Aggiunta riga: {nuovo_nome}")
            else:
                percorso_file_m3u = os.path.join(directory, nome_file_m3u)
                try:
                    with open(percorso_file_m3u, 'w', encoding='utf-8') as f_m3u:
                        for nuovo_nome in nuovi_nomi_file:
                            f_m3u.write(nuovo_nome + '\n')
                    print(f"[OK] Creato file playlist: {nome_file_m3u}")
                except IOError as e:
                    print(f"[ERRORE] Impossibile creare il file {nome_file_m3u}: {e}")
                    continue

            # 4. Rinomina i file o registra l'azione per la simulazione
            for i, disco in enumerate(dischi_ordinati):
                vecchio_nome = disco['nome_file_originale']
                nuovo_nome = nuovi_nomi_file[i] # Prende il nome corrispondente dalla lista preparata
                if simulare:
                    log_simulazione.append(f"[RIDENOMINAZIONE FILE] -> Da '{vecchio_nome}' a '{nuovo_nome}'")
                else:
                    vecchio_percorso = os.path.join(directory, vecchio_nome)
                    nuovo_percorso = os.path.join(directory, nuovo_nome)
                    try:
                        if os.path.exists(vecchio_percorso):
                            os.rename(vecchio_percorso, nuovo_percorso)
                            print(f"  -> Rinominato: '{vecchio_nome}' in '{nuovo_nome}'")
                        else:
                            print(f"  -> Avviso: File '{vecchio_nome}' non trovato, potrebbe essere già stato rinominato.")
                    except OSError as e:
                        print(f"[ERRORE] Impossibile rinominare {vecchio_nome}: {e}")
            
            print("-" * (len(nome_base) + 20) + "\n")
            if simulare:
                log_simulazione.append("-" * (len(nome_base) + 20) + "\n")

    if giochi_elaborati == 0:
        print("Nessun set di giochi con più di un disco è stato trovato per creare una playlist.")
    elif simulare:
        nome_file_report = "report_simulazione.txt"
        percorso_report = os.path.join(directory, nome_file_report)
        try:
            with open(percorso_report, 'w', encoding='utf-8') as f_report:
                f_report.write('\n'.join(log_simulazione))
            print(f"--- SIMULAZIONE COMPLETATA ---")
            print(f"Creato report con le azioni previste in: {os.path.abspath(percorso_report)}")
        except IOError as e:
            print(f"[ERRORE] Impossibile creare il file di report: {e}")
    else:
        print(f"--- Elaborazione completata. Creati {giochi_elaborati} file .m3u. ---")

if __name__ == "__main__":
    if os.path.isdir(cartella_rom):
        crea_playlist_m3u(cartella_rom, simulazione)
    else:
        print(f"ERRORE: La cartella specificata non esiste: '{os.path.abspath(cartella_rom)}'")
        print("Per favore, controlla la variabile 'cartella_rom' nello script.")
