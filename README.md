# Vilniaus nekilnojamojo turto (butų) prognozė
## Prieš pradedant
Čia yra sukelti visi reikalingi failai susiję su projektu, įskaitant ir naudotus duomenis (jų šaltinius), bei notebookus kuriuose buvo testuojami ML modeliai ir atliekamos duomenų analizės.

Taip pat projekte esančiame `app.py`faile yra sukurtas API, bei vartojo forma naudojant FLASK, siekiant surinkti duomenis reikalingus buto kainos prognozei atlikti.
***
`app.py` naudojami ML modeliai **skirasi**:
+ **FORM** naudojomas paprastesnis modelis, kurio paklaida ir tikslumas yra žemesni.
+ **JSON** naudojamas efektyvesnis modelis, dėl techninių galimybių įtraukti daugiau kintamųjų.

## Reikalingos bibliotekos

Visame projekte naudojamos šios bibliotekos:
```
pandas
numpy
seaborn
matplotlib
sklearn
re
joblib
flask
wtforms
```
Tačiau, kadangi modeliai jau yra pridėti, kuriant VENV užteks naudoti bibliotekas esančias `requirements.txt` naudojant:
```
pip install -r requirements.txt
```
## Naudojimas
#### Su ML bei naudotais duomenimis:
Vietoj **Jupyter Notebook** šiam projektui aš naudojau [Google Colab](https://colab.research.google.com/) atliekančią ne tik visas reikalingas Jupyter funkcijas, tačiau ir patogiai leidžiančiai:
+ Dalintis projektu su kitais.
+ Patogiai įkelti, parsisiųsti visus reikalingus failus.

Visi **notebooks** gali būti rasti [notebooks](https://github.com/simado/busto-kainos/tree/master/notebooks) aplankale.
+ `Formos_modelis.ipynb` yra tik modelis paruoštas **FORM** gavimui.
+ `JSON_modelis.ipynb` yra pilnas notebook kuriame yra visa duomenų analizė, bei ML **JSON** naudojimui.

#### Su `app.py`:
Reikalingi įrankiai:
```
Python 3
pip
virtualenv
```
1. Nusiklonuokite/parsisiųskite [projektą](https://github.com/simado/busto-kainos.git)
2. Projekte sukurkite VENV:
Iš pradžių nueikite į projekto direktoriją naudojant terminalą:
```
cd desktop/busto-kainos-master
```
Tada sukurkite VENV naudojant tolimesnę komandą:
```
python -m venv venv
```
**Čia venv reikš jūsų VENV pavadinimą**

3. Paleiskite virtualią aplinką naudojant tolimesnę komandą:
```
source venv/bin/activate
```
4. Parsisiųskite reikalingas bibliotekas
```
pip install -r requirements.txt
```
5. Dirbkite naudojant jums patinkantį IDE
Savo darbams aš naudojau [Visual Studio Code](https://code.visualstudio.com/)

## Autorius
**Simonas Adomavičius** [LinkedIn](https://www.linkedin.com/in/simon-adomavicius/)
