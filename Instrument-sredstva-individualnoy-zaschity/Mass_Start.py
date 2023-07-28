import os
import subprocess


def run_scripts_in_folder():
    current_path = os.path.dirname(os.path.abspath(__file__))

    scripts_to_run = [

        'Instrument-dlya-opressovki-nakonechnikov.py',
        'Instrument-dlya-prosekaniya-otverstiy.py',
        'Instrument-dlya-rezki-kabelya.py',
        'Instrument-dlya-rezki-materialov.py',
        'Instrument-dlya-snyatiya-izolyatsii-s-kabeley.py',
        'Instrument-dlya-snyatiya-izolyatsii-s-provodov.py',
        'Instrumenty-dlya-homutov.py',
        'Klyuchi-montazhnye.py',
        'Kontrolno-izmeritelnyy-instrument.py',
        'Magnitnye-derzhateli-pozitsionery.py',
        'Nabory-instrumentov.py',
        'Otvertki.py',
        'Sharnirno-gubtsevyy-instrument.py',
        'Universalnyy-instrument.py',

    ]

    for script in scripts_to_run:

        script_path = os.path.join(current_path, script)

        if script != 'main.py':
            print(f"Запуск скрипта: {script}")
            try:
                subprocess.run(["python", script_path], check=True)
                print(f"Скрипт {script} выполнен")
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при выполнении скрипта {script}: {e}")
                break


if __name__ == "__main__":
    run_scripts_in_folder()
