# Oddílový systém - webový projekt 

Tento projekt byl vyvinut pro kurz *Vývoj webových aplikací* na Mendelově univerzitě v Brně, v zimním semestru 2022-2023, což byl kurz pro začátečníky, který seznamuje s vývojem webových aplikací.

Zadaným úkolem bylo vytvořit malý systém pro skautský oddíl, který by umožňoval správu akcí (jako správce systému nebo vedoucí skupiny), sledování jednotlivých akcí (jako rodič nebo dítě), sledování docházky dětí a propagaci činnosti skautského oddílu.

## Použité nástroje

- HTML5
- CSS3
- Python a webový framework Flask
- SQLite3

Vzhledem k tomu, že tento projekt byl implementován v rámci kurzu pro začátečníky a pouze pro představení vývoje webových aplikací (zejména práce s databázemi a backend frameworkem jako je Flask), nebyl použít JavaScript a jeho knihovny, resp. frameworky.

## Příprava projektu a spuštění aplikace

```bash
git clone https://github.com/h0ldemslav/high-school-projects.git

cd ./high-school-projects/oddilovy-system

python3 -m venv venv
pip3 install -r "requirements.txt"

# Spusteni virtualniho prostredi v OS Windows
./venv/Scripts/Activate

# Inicializace databaze
flask init-db
flask --debug run
```

## Přihlašovací údaje pro testování funkčnosti webu

Admin:
- login: xnavra18
- heslo: password

## Autoři

- Filip Adámek
- Daniil Astapenko
- Pavol Faško
- Martin Navrátil