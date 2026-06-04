"""
===============================================================================
Projekt        : Messdatenausgabe eines digitalen Multimeters
Datei          : messdatenausgabe.py
Autor          : Azlan Ainto
Version        : 1.0
Python-Version : Python 3.10
Datum          : 04.06.2026

Beschreibung:
    Dieses Python-Programm simuliert die Erfassung, Verarbeitung
    und formatierte Ausgabe elektrischer Messdaten eines digitalen
    Multimeters.

Funktionen:
    - Ausgabe elektrischer Messgrößen
    - Berechnung der elektrischen Leistung (P = U * I)
    - Umrechnung von Ampere in Milliampere
    - Tabellenformatierte Konsolenausgabe

Lernziele:
    - Verwendung von Variablen und Datentypen
    - Formatierte Ausgaben mit print()
    - Anwendung von Formatierungsoptionen:
        * Rundung
        * Ausrichtung
        * sep und end

Einsatzbereich:
    Elektronik, Messtechnik, technische Ausbildung,
    technische Dokumentation und Python-Grundlagen.

Hinweis:
    Dieses Projekt dient ausschließlich Lern-, Demonstrations-
    und Ausbildungszwecken.
===============================================================================
"""

# ---  Messdaten erfassen ---
geraet = " Multimeter Fluke 87V"
messung_nr = 7
U = 230.756  # Spannung in Volt
I = 1.2834  # Stromstärke in Ampere
R = 179.83 # Widerstand in Ohm
temperatur = 25.5  # Temperatur in Grad Celsius
in_betrieb  = True
# --- Ausgabe der Messdaten ---
print("Gerät:", geraet)
print()
# --- Formatierte Ausgabe der Messdaten mit f-Strings ---
print(f"Messung Nr: {messung_nr:03d}")  # -> 007
print(f"Spannung U ={U:.3f} v")         # -> z.B  230.756 V
print(f"Strom I = {I:.2f} A")           # -> z.B  1.28 A
print(f"Strom I = {I*1000:2f} mA")      # -> z.B 1283.400000 mA
print(f"Temperatur = {temperatur:.1f} °C")  # -> z.B 25.5 °C
print(f"In Betrieb = {in_betrieb}")          # -> z.B  True
# --- Tabellenforamt mit der Ausrichtung ---
print("\nMessgröße".ljust(15), "Wert".rjust(15))
print("-" * 30)
print("Spannung U".ljust(15), f"{U:.3f} V".rjust(15))
print("Strom I".ljust(15), f"{I:.2f} A".rjust(15))
print("Widerstand R".ljust(15), f"{R:.2f} Ω".rjust(15))
print("Temperatur".ljust(15), f"{temperatur:.1f} °C".rjust(15))
print(f"Leistung P".ljust(15), f"{U * I:.2f} W".rjust(15))  # Berechnung der Leistung P = U * I

print("\n\n")
print(f"{'Größe':<12} {'Wert':>10} {'Einheit': <10}")  
print("-" * 32)
print(f"{'Spannung':<12}{U:>10.3f}{'V':<8}")
print(f"{'Strom':<12}{I:>10.2f}{'A':<8}")
print(f"{'Widerstand':<12}{R:>10.2f}{'Ohm':<8}")
print(f"{'Leistung':<12} {U*I:>10.2f} {'W':<8}")
# --- sep und end Parameter ---
print("U","I", "R", sep = " | ")
print("Messung läuft", end = "...")
print(" OK")
      
