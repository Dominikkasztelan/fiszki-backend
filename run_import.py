import pandas as pd
from sqlalchemy import create_engine
import os
import json

# ================= 🔴 KONFIGURACJA =================
# Upewnij się, że hasło i link są poprawne
DB_CONNECTION_STR = "postgresql://neondb_owner:npg_sfqktyOAWI50@ep-calm-resonance-agyyd59j-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
TABLE_NAME = "slowka_slowko"


# ===================================================

def get_engine():
    return create_engine(DB_CONNECTION_STR)


def find_file(filename):
    search_paths = ["./", "./fiszki/date/", "./date/", "./csv/", "./pliki_csv/"]
    for path in search_paths:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    return None


def normalize_columns(df):
    df.columns = [str(c).strip().lower() for c in df.columns]

    rename_map = {
        # Angielski
        "słowo (angielski)": "angielski",
        "angielski": "angielski",
        "english": "angielski",
        "word": "angielski",
        "tłumaczenie angielskie": "angielski",
        "tłumaczenie (angielski)": "angielski",
        "słowo": "angielski",  # <--- ZMIANA: "Słowo" w tym pliku to Angielski!

        # Polski
        "tłumaczenie (polski)": "polski",
        "polski": "polski",
        "polish": "polski",
        "tłumaczenie": "polski",
        "słowo polskie": "polski",
        "słowo (polski)": "polski",

        # Wymowa
        "wymowa (ipa)": "wymowa",
        "wymowa": "wymowa",
        "ipa": "wymowa",
        "wymowa uk (ipa)": "wymowa",
        "wymowa uk": "wymowa"
    }

    df = df.rename(columns=rename_map)
    return df


def import_standard_files(engine):
    # 👇 ZAKOMENTOWAŁEM PLIKI, KTÓRE JUŻ MASZ W BAZIE
    files_map = {
        'słownictwo zwierzęta.csv': 'Zwierzęta',
        'słownictwo ogród.csv': 'Ogród',
        'słownictwo emocje i uczucia.csv': 'Emocje',
        'słownictwo czyności.csv': 'Czynności',
        'słownictwo angielskie polskie wymowa.csv': 'Ogólne',
        'słownictwo angielskie polskie wymowa nr 2.csv': 'Ogólne II'
    }

    print("\n--- 🚀 DOGRYWAMY BRAKUJĄCE PLIKI ---")
    for filename, category in files_map.items():
        filepath = find_file(filename)
        if not filepath:
            print(f"⚠️ Brak pliku: {filename}")
            continue

        try:
            try:
                df = pd.read_csv(filepath, sep=',')
                if len(df.columns) < 2: df = pd.read_csv(filepath, sep=';')
            except:
                df = pd.read_csv(filepath, sep=';', encoding='cp1250')

            df = normalize_columns(df)

            if 'angielski' not in df.columns or 'polski' not in df.columns:
                print(f"❌ Błąd mapowania {filename}. Kolumny: {list(df.columns)}")
                continue

            df['kategoria'] = category
            df['details'] = df.apply(lambda x: json.dumps({}), axis=1)  # Fix na błąd 'dict'

            if 'wymowa' not in df.columns: df['wymowa'] = None

            df_final = df[['angielski', 'polski', 'wymowa', 'kategoria', 'details']].copy()

            df_final.to_sql(TABLE_NAME, engine, if_exists='append', index=False, method='multi', chunksize=500)
            print(f"✅ {filename}: Dodano {len(df_final)} rekordów.")

        except Exception as e:
            print(f"❌ Błąd pliku {filename}: {e}")


if __name__ == "__main__":
    eng = get_engine()
    import_standard_files(eng)
    # Funkcję import_irregular_verbs też wyłączyliśmy, bo już weszła poprawnie
    print("🏁 Gotowe! Baza kompletna.")