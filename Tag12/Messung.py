import random 
random.seed(14)
# ==== break - Suche nach erstem Fehlerteil ====
# ..... Symbole .....
warnung = chr(0x26D4)
ok = chr(0x2714)
# ...................

for teil_nr in range(1,21):
    durchmesser = random.uniform(9.7, 10.3)
    if abs(durchmesser - 10.0) > 0.1:
        print(f"{warnung } Teil {teil_nr} : {durchmesser:.3f} mm - FEHLER GEFUNDEN!")
        print(f"-> Fließband angehalten bei Teil {teil_nr}")
        break
    print(f"{ok} Teil {teil_nr}:{durchmesser:.3f} mm - OK")

print("\n\n==== Vollständige Prüfung - defekte Teile überspringen ====")
random.seed(14)
gut_teile = 0
ausschuss_teile = 0

for teil_nr in range(1,11):
    durchmesser = random.uniform(9.7, 10.3)
    if abs(durchmesser - 10.0) > 0.1:
        print(f"{warnung} Teil {teil_nr} : {durchmesser: .3f} mm - verworfen")
        ausschuss_teile +=1
        continue
    print(f"{ok} {teil_nr}: {durchmesser:.3f} mm - OK")
    gut_teile +=1
print(f"\n Ergebnis: {gut_teile}: OK, {ausschuss_teile} verworfen (von 10)")