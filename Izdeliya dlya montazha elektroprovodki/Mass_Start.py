import os
import subprocess

def run_scripts_in_folder():

    current_path = os.path.dirname(os.path.abspath(__file__))


    scripts_to_run = [

        #"Nakonechniki-gilzy-razemy.py",
        #"Samokleyaschiesya-ploschadki-dlya-homutov.py",
        #"Silovye-nakonechniki-i-gilzy.py",
        "Skoby-plastikovye.py",
        "Spiral-montazhnaya.py",
        "Termousazhivaemye-izdeliya.py",
        "Zazhimy.py"
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