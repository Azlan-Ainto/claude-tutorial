# === Programm: Widerstandsrechner ===
# === Beschreibung: Berechnet den Gesamtwiderstand von Widerständen in Reihe ===
print("=== Ohmsches Gesetz - Rechner ===\n")
# --- Texteingabe ----------------------------
bauteil = input("Bauteilbezeichnung: ")
# --- Zahleneingaben ----------------------------
U = float(input("Spannung U in Volt: "))
R = float(input("Widerstand R in Ohm: "))
# --- Berechnung ----------------------------
I = U / R;     P = U * I ;      I_mA = I * 1000
# --- Ausgabe als Messprotokoll ----------------------------
print("-" * 35)
print()
print(f" Ergebnis für: {bauteil}")
print("-" * 35)
print(f"{'Spannung U':<15}: {U:>10.2f} V")
print(f"{'Widertand':<15}:{R:>10.2f} Ω")
print(f"{'Strom I':<15}: {I:>10.2f} A")
print(f"{'Strom I':<15}: {I_mA:>10.2f} mA")
print(f"{'Leistung':<15}: {P:>10.2f} W")
print("-" * 35)