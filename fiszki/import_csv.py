import os
import django
import csv
import glob

# Konfiguracja Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fiszki.settings')
django.setup()

from slowka.models import Slowko


def importuj_wszystko():
    folder_skryptu = os.path.dirname(os.path.abspath(__file__))
    sciezka_do_plikow = os.path.join(folder_skryptu, 'date', '*.csv')
    pliki = glob.glob(sciezka_do_plikow)

    print(f"✅ Znaleziono {len(pliki)} plików CSV. Rozpoczynam import...\n")

    lacznie_dodano = 0

    for plik in pliki:
        nazwa_pliku = os.path.basename(plik)
        print(f"--- Przetwarzam: {nazwa_pliku} ---")

        try:
            with open(plik, 'r', encoding='utf-8-sig') as f:
                pierwsza_linia = f.readline()
                separator = ';' if ';' in pierwsza_linia else ','
                f.seek(0)

                reader = csv.DictReader(f, delimiter=separator)
                # Czyścimy nazwy kolumn ze spacji
                reader.fieldnames = [name.strip() for name in reader.fieldnames]

                licznik_pliku = 0
                for row in reader:
                    try:
                        # --- SEKJA DETEKTYWA ---
                        # Skrypt szuka angielskiego słowa pod różnymi nazwami kolumn:
                        angielski = ""
                        for opcja in ['Forma podstawowa (Infinitive)', 'Przymiotnik (Adjective)', 'Rzeczownik (Noun)',
                                      'Angielski', 'Word', 'Słówko']:
                            if row.get(opcja):
                                angielski = row.get(opcja).strip()
                                break

                        # Skrypt szuka polskiego słowa pod różnymi nazwami:
                        polski = ""
                        for opcja in ['Tłumaczenie angielsko-polskie', 'Tłumaczenie', 'Polski', 'Meaning', 'Znaczenie']:
                            if row.get(opcja):
                                polski = row.get(opcja).strip()
                                break
                        # -----------------------

                        if angielski and polski:
                            Slowko.objects.create(
                                angielski=angielski,
                                polski=polski
                            )
                            licznik_pliku += 1
                    except Exception:
                        pass

                print(f"   -> Dodano {licznik_pliku} słówek.")

                if licznik_pliku == 0:
                    print(f"   ⚠️ UWAGA: 0 słówek! Widoczne kolumny: {reader.fieldnames}")

                lacznie_dodano += licznik_pliku

        except Exception as e:
            print(f"   -> BŁĄD PLIKU: {e}")

    print(f"\n=========================================")
    print(f"🚀 KONIEC! Łącznie w bazie masz teraz {lacznie_dodano} nowych słówek!")


if __name__ == '__main__':
    importuj_wszystko()