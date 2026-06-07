# --- Testing the type of the user input
print(type(input("Wert: ")))
r = input("R in Ohm:")
print(r*2) # --> Fehler --> verkettet r 
# --- Konvertiere r in float ----
r = float(r)
print(r*2)