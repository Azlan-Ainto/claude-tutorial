# =============================================================================
# KREDITRECHNER MIT TILGUNGSPLAN
# Angewandte Mathematik in Python — Analysis im Alltag
#
# Themen:
#   - Geometrische Reihen (Annuitätenformel)
#   - Differentialrechnung (Ableitung der Restschuld)
#   - Numerische Iteration (Tilgungsplan)
#   - Visualisierung mit matplotlib
# =============================================================================

import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# =============================================================================
# 1. MATHEMATISCHE GRUNDLAGEN — DIE ANNUITÄTENFORMEL
# =============================================================================
#
# Ein Annuitätenkredit hat eine konstante monatliche Rate (Annuität).
# Die Rate setzt sich aus zwei Teilen zusammen:
#
#   Rate = Zinsanteil + Tilgungsanteil
#
# Am Anfang ist der Zinsanteil hoch (große Restschuld),
# am Ende ist er niedrig (kleine Restschuld).
#
# Herleitung der Formel:
# ----------------------
# Gesucht: konstante Rate R, sodass nach n Monaten die Schuld = 0
#
# Restschuld nach Monat k:
#   S_k = S_(k-1) * (1 + r) - R
#
# Das ist eine rekursive Folge. Ihre geschlossene Lösung (geometrische Reihe):
#   S_n = P * (1+r)^n - R * ((1+r)^n - 1) / r = 0
#
# Auflösen nach R ergibt die ANNUITÄTENFORMEL:
#
#         P * r * (1+r)^n
#   R = ─────────────────────
#         (1+r)^n - 1
#
# Dabei ist:
#   P = Kreditsumme (Anfangsschuld)
#   r = monatlicher Zinssatz = Jahreszins / 12
#   n = Anzahl der Monate (Laufzeit)

def berechne_monatsrate(P: float, jahreszins: float, n_monate: int) -> float:
    """
    Berechnet die konstante monatliche Kreditrate (Annuität).
    Mathematik: geometrische Reihe
    Formel: R = P * r * (1+r)^n / ((1+r)^n - 1)
    Parameter:
        P           : Kreditsumme in Euro
        jahreszins  : Zinssatz pro Jahr als Dezimalzahl (z.B. 0.045 für 4,5 %)
        n_monate    : Laufzeit in Monaten
    Rückgabe:
        Monatliche Rate in Euro
    """
        # Monatszins: Jahreszins gleichmäßig auf 12 Monate verteilt
    r = jahreszins / 12
        # Sonderfall: Zinsloser Kredit → einfache Division
    if r == 0:
        return P / n_monate
        # Berechne (1+r)^n mit dem Exponentialoperator
        # Dies ist der Zinseszins-Faktor nach n Monaten
    faktor = (1 + r) ** n_monate
        # Annuitätenformel anwenden
    rate = P * r * faktor / (faktor - 1)
    return rate


# =============================================================================
# 2. TILGUNGSPLAN — MONATLICHE ITERATION
# =============================================================================
#
# Der Tilgungsplan zeigt für jeden Monat:
#   - Wie viel der Rate als Zinsen abgeht      → Zinsanteil  = Restschuld * r
#   - Wie viel wirklich getilgt wird           → Tilgung     = Rate - Zinsanteil
#   - Wie hoch die Restschuld danach noch ist  → neu_schuld  = alt_schuld - Tilgung
#
# Wichtige Beobachtung (mathematisches Prinzip):
#   Da die Rate konstant bleibt, aber der Zinsanteil mit sinkender
#   Restschuld abnimmt, STEIGT der Tilgungsanteil jeden Monat leicht.
#   → Exponentieller Effekt: am Ende tilgt man viel mehr als am Anfang.

def erstelle_tilgungsplan(P: float, jahreszins: float, n_monate: int) -> list[dict]:
    """
    Erstellt den vollständigen Tilgungsplan Monat für Monat.
    Parameter:
        P           : Kreditsumme in Euro
        jahreszins  : Jahreszins als Dezimalzahl
        n_monate    : Laufzeit in Monaten

    Rückgabe:
        Liste von Dictionaries, je ein Eintrag pro Monat:
        [{'monat': 1, 'rate': ..., 'zinsen': ..., 'tilgung': ..., 'restschuld': ...}, ...]
    """
    r = jahreszins / 12                           # Monatszins
    rate = berechne_monatsrate(P, jahreszins, n_monate)
    restschuld = P                                # Startwert: volle Kreditsumme
    plan = []

    for monat in range(1, n_monate + 1):

        # ZINSANTEIL: proportional zur aktuellen Restschuld
        # Je kleiner die Restschuld, desto weniger Zinsen — lineare Abhängigkeit
        zinsen = restschuld * r
        # TILGUNGSANTEIL: was nach den Zinsen von der Rate übrig bleibt
        # Zu Beginn klein, am Ende fast die volle Rate
        tilgung = rate - zinsen
        # NEUE RESTSCHULD: Restschuld wird um den Tilgungsanteil reduziert
        restschuld = restschuld - tilgung
        # Rundungsfehler im letzten Monat abfangen (floating point)
        # Mathematisch sollte restschuld nach n Monaten exakt 0 sein
        if abs(restschuld) < 0.01:
            restschuld = 0.0

        # Monatsdaten speichern
        plan.append({
            'monat':      monat,
            'rate':       round(rate, 2),
            'zinsen':     round(zinsen, 2),
            'tilgung':    round(tilgung, 2),
            'restschuld': round(restschuld, 2),
        })

    return plan


# =============================================================================
# 3. ZUSAMMENFASSUNG BERECHNEN
# =============================================================================

def berechne_zusammenfassung(P: float, jahreszins: float, n_monate: int) -> dict:
    """
    Berechnet die wichtigsten Kenngrössen des Kredits.
    Nutzt den vollständigen Tilgungsplan für exakte Werte.
    """
    rate = berechne_monatsrate(P, jahreszins, n_monate)
    plan = erstelle_tilgungsplan(P, jahreszins, n_monate)
    # Gesamtkosten = Summe aller Raten (Rate × Monate, aber letzte Rate kann abweichen)
    gesamtkosten = sum(eintrag['rate'] for eintrag in plan)
    # Gesamtzinsen = Gesamtkosten minus zurückgezahlte Kreditsumme
    gesamtzinsen = gesamtkosten - P
    # Effektiver Zinsanteil: Wie viel Prozent der Gesamtkosten sind Zinsen?
    zinsanteil_pct = (gesamtzinsen / gesamtkosten) * 100
    # Halbwertszeit: Nach wie vielen Monaten ist die Hälfte getilgt?
    halbzeit = next(
        (e['monat'] for e in plan if e['restschuld'] <= P / 2),
        n_monate
    )

    return {
        'P':              P,
        'jahreszins_pct': jahreszins * 100,
        'n_monate':       n_monate,
        'n_jahre':        n_monate / 12,
        'monatsrate':     round(rate, 2),
        'gesamtkosten':   round(gesamtkosten, 2),
        'gesamtzinsen':   round(gesamtzinsen, 2),
        'zinsanteil_pct': round(zinsanteil_pct, 2),
        'halbzeit_monate':halbzeit,
    }


# =============================================================================
# 4. VISUALISIERUNG
# =============================================================================
#
# Drei Diagramme zeigen den Kredit aus unterschiedlichen Blickwinkeln:
#
#   (a) Gestapeltes Balkendiagramm — Zins- vs. Tilgungsanteil pro Monat
#       → Zeigt visuell, wie die Aufteilung sich über die Zeit verschiebt
#
#   (b) Liniendiagramm — Restschulden-Verlauf
#       → Zeigt den exponentiellen Rückgang (flach am Anfang, steil am Ende)
#
#   (c) Kuchendiagramm — Gesamtkosten aufgeteilt
#       → Zeigt, wie viel vom Gesamtbetrag Zinsen sind

def visualisiere_kredit(P: float, jahreszins: float, n_monate: int):
    """
    Erstellt drei Diagramme zur Visualisierung des Kredits.

    Parameter:
        P           : Kreditsumme in Euro
        jahreszins  : Jahreszins als Dezimalzahl
        n_monate    : Laufzeit in Monaten
    """
    # Daten berechnen
    plan = erstelle_tilgungsplan(P, jahreszins, n_monate)
    info = berechne_zusammenfassung(P, jahreszins, n_monate)

    # Daten aus dem Plan extrahieren (für die Diagramme)
    # Wir nehmen jeden n-ten Monat, damit das Diagramm übersichtlich bleibt
    schritt = max(1, n_monate // 24)              # max. 24 Datenpunkte im Diagramm

    monate     = [e['monat']      for e in plan[::schritt]]
    zinsen     = [e['zinsen']     for e in plan[::schritt]]
    tilgungen  = [e['tilgung']    for e in plan[::schritt]]
    restschuld = [e['restschuld'] for e in plan[::schritt]]

    # Letzten Monat immer einschließen (kann durch schritt ausgelassen werden)
    if plan[-1]['monat'] not in monate:
        monate.append(plan[-1]['monat'])
        zinsen.append(plan[-1]['zinsen'])
        tilgungen.append(plan[-1]['tilgung'])
        restschuld.append(plan[-1]['restschuld'])

    # ── FIGURE EINRICHTEN ────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        f"Kreditanalyse: {P:,.0f} € | {jahreszins*100:.1f} % p.a. | "
        f"{n_monate} Monate ({n_monate/12:.0f} Jahre)",
        fontsize=13, fontweight='bold', y=1.02
    )

    # Farben
    FARBE_ZINSEN   = '#f09595'   # Rot  → Zinsen (Kosten)
    FARBE_TILGUNG  = '#85b7eb'   # Blau → Tilgung (Vermögensaufbau)
    FARBE_SCHULD   = '#7F77DD'   # Lila → Restschuld

    # ── DIAGRAMM (a): Gestapeltes Balkendiagramm ─────────────────────────────
    ax1 = axes[0]

    # Gestapeltes Balkendiagramm: Zinsen unten, Tilgung oben gestapelt
    ax1.bar(monate, zinsen,    color=FARBE_ZINSEN,  label='Zinsanteil',   width=schritt*0.8)
    ax1.bar(monate, tilgungen, color=FARBE_TILGUNG, label='Tilgungsanteil',
            bottom=zinsen,     width=schritt*0.8)

    ax1.set_title('Ratenaufteilung über die Laufzeit', fontsize=11)
    ax1.set_xlabel('Monat')
    ax1.set_ylabel('Euro pro Monat')
    ax1.legend(fontsize=9)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f} €'))
    ax1.grid(axis='y', alpha=0.3)

    # Annotation: Wendepunkt markieren (wenn Tilgung > Zinsen)
    wendepunkt = next(
        (e['monat'] for e in plan if e['tilgung'] > e['zinsen']), None
    )
    if wendepunkt:
        ax1.axvline(wendepunkt, color='gray', linestyle='--', alpha=0.6, linewidth=1)
        ax1.text(wendepunkt + 1, max(zinsen) * 0.8,
                 f'Tilgung > Zinsen\nab Monat {wendepunkt}',
                 fontsize=8, color='gray')

    # ── DIAGRAMM (b): Restschuld-Verlauf ─────────────────────────────────────
    ax2 = axes[1]

    ax2.fill_between(monate, restschuld, alpha=0.15, color=FARBE_SCHULD)
    ax2.plot(monate, restschuld, color=FARBE_SCHULD, linewidth=2, label='Restschuld')

    # Horizontale Linie bei 50 % der ursprünglichen Schuld
    ax2.axhline(P / 2, color='orange', linestyle=':', alpha=0.7, linewidth=1)
    ax2.text(n_monate * 0.02, P / 2 + P * 0.02, '50 % getilgt', fontsize=8, color='orange')

    # Vertikale Linie beim Halbierungszeitpunkt
    ax2.axvline(info['halbzeit_monate'], color='orange', linestyle=':', alpha=0.7, linewidth=1)
    ax2.text(info['halbzeit_monate'] + n_monate * 0.01, P * 0.1,
             f"Monat {info['halbzeit_monate']}", fontsize=8, color='orange')

    ax2.set_title('Restschuld-Verlauf', fontsize=11)
    ax2.set_xlabel('Monat')
    ax2.set_ylabel('Restschuld (€)')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f} €'))
    ax2.set_ylim(bottom=0)
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    # ── DIAGRAMM (c): Kuchendiagramm ─────────────────────────────────────────
    ax3 = axes[2]

    werte  = [P, info['gesamtzinsen']]
    labels = [
        f"Kreditsumme\n{P:,.0f} €",
        f"Zinsen gesamt\n{info['gesamtzinsen']:,.0f} €"
    ]
    farben = [FARBE_TILGUNG, FARBE_ZINSEN]

    # explode: Zinsscheibe leicht herausziehen für Betonung
    explode = (0, 0.05)

    wedges, texts, autotexts = ax3.pie(
        werte,
        labels=labels,
        colors=farben,
        explode=explode,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 9}
    )
    autotexts[0].set_fontweight('bold')
    autotexts[1].set_fontweight('bold')

    ax3.set_title(
        f"Gesamtkosten: {info['gesamtkosten']:,.0f} €",
        fontsize=11
    )

    # ── LAYOUT UND SPEICHERN ─────────────────────────────────────────────────
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/kreditrechner_diagramme.png',
                dpi=150, bbox_inches='tight')
    plt.show()
    print("Diagramme gespeichert: kreditrechner_diagramme.png")


# =============================================================================
# 5. AUSGABE — KONSOLENREPORT
# =============================================================================

def drucke_report(P: float, jahreszins: float, n_monate: int, max_zeilen: int = 12):
    """
    Gibt einen übersichtlichen Textreport in der Konsole aus.
    Zeigt Zusammenfassung + die ersten und letzten Monate des Tilgungsplans.

    Parameter:
        max_zeilen : Wie viele Monate des Plans gedruckt werden (Anfang + Ende)
    """
    info = berechne_zusammenfassung(P, jahreszins, n_monate)
    plan = erstelle_tilgungsplan(P, jahreszins, n_monate)

    # Trennlinie
    linie = "─" * 65

    print(f"\n{'═'*65}")
    print(f"  KREDITANALYSE")
    print(f"{'═'*65}")
    print(f"  Kreditsumme     : {info['P']:>12,.2f} €")
    print(f"  Jahreszins      : {info['jahreszins_pct']:>11.2f} %")
    print(f"  Laufzeit        : {info['n_monate']:>9} Monate  ({info['n_jahre']:.1f} Jahre)")
    print(f"{linie}")
    print(f"  Monatsrate      : {info['monatsrate']:>12,.2f} €")
    print(f"  Gesamtkosten    : {info['gesamtkosten']:>12,.2f} €")
    print(f"  Gesamtzinsen    : {info['gesamtzinsen']:>12,.2f} €  ← Extrakosten")
    print(f"  Zinsanteil      : {info['zinsanteil_pct']:>11.2f} %  der Gesamtkosten")
    print(f"  50 % getilgt ab : Monat {info['halbzeit_monate']} "
          f"({info['halbzeit_monate']/12:.1f} Jahre) ← Halbwertszeit")
    print(f"{'═'*65}")

    # Tilgungsplan (Kopf)
    print(f"\n  {'Monat':>5}  {'Rate':>10}  {'Zinsen':>10}  {'Tilgung':>10}  {'Restschuld':>12}")
    print(f"  {linie}")

    # Erste max_zeilen/2 Monate
    for eintrag in plan[:max_zeilen // 2]:
        print(f"  {eintrag['monat']:>5}  "
              f"{eintrag['rate']:>9,.2f}€  "
              f"{eintrag['zinsen']:>9,.2f}€  "
              f"{eintrag['tilgung']:>9,.2f}€  "
              f"{eintrag['restschuld']:>11,.2f}€")

    print(f"  {'...':^62}")

    # Letzte max_zeilen/2 Monate
    for eintrag in plan[-(max_zeilen // 2):]:
        print(f"  {eintrag['monat']:>5}  "
              f"{eintrag['rate']:>9,.2f}€  "
              f"{eintrag['zinsen']:>9,.2f}€  "
              f"{eintrag['tilgung']:>9,.2f}€  "
              f"{eintrag['restschuld']:>11,.2f}€")

    print(f"  {linie}")
    print()


# =============================================================================
# 6. VERGLEICHSANALYSE — LAUFZEIT vs. GESAMTZINSEN
# =============================================================================
#
# Hier wenden wir die Analysis direkt an:
# Die Ableitung der Zinskosten nach der Laufzeit ist immer positiv —
# längere Laufzeit bedeutet immer mehr Gesamtzinsen.
# Gleichzeitig sinkt die Monatsrate mit der Laufzeit.
# → Es gibt kein globales Optimum, nur ein persönliches.

def vergleiche_laufzeiten(P: float, jahreszins: float):
    """
    Vergleicht verschiedene Laufzeiten für denselben Kredit.
    Zeigt den Trade-off zwischen Monatsrate und Gesamtzinsen.
    """
    laufzeiten = [12, 24, 36, 48, 60, 84, 120]   # in Monaten

    print(f"\n  LAUFZEITVERGLEICH: {P:,.0f} € bei {jahreszins*100:.1f} % p.a.")
    print(f"  {'─'*65}")
    print(f"  {'Laufzeit':>10}  {'Monatsrate':>12}  {'Gesamtzinsen':>14}  {'Zinsanteil':>12}")
    print(f"  {'─'*65}")

    for n in laufzeiten:
        info = berechne_zusammenfassung(P, jahreszins, n)
        jahre = n // 12
        monate_rest = n % 12

        laufzeit_str = f"{jahre}J" + (f" {monate_rest}M" if monate_rest else "")

        print(f"  {laufzeit_str:>10}  "
              f"{info['monatsrate']:>11,.2f}€  "
              f"{info['gesamtzinsen']:>13,.2f}€  "
              f"{info['zinsanteil_pct']:>11.1f}%")

    print()


# =============================================================================
# 7. HAUPTPROGRAMM
# =============================================================================

if __name__ == "__main__":

    # ── Kreditparameter definieren ───────────────────────────────────────────
    KREDITSUMME  = 20_000   # Euro
    JAHRESZINS   = 0.045    # 4,5 % pro Jahr
    LAUFZEIT     = 60       # 60 Monate = 5 Jahre

    # ── Report in der Konsole ausgeben ──────────────────────────────────────
    drucke_report(KREDITSUMME, JAHRESZINS, LAUFZEIT, max_zeilen=12)

    # ── Laufzeitvergleich ausgeben ───────────────────────────────────────────
    vergleiche_laufzeiten(KREDITSUMME, JAHRESZINS)

    # ── Diagramme erstellen und anzeigen ────────────────────────────────────
    visualisiere_kredit(KREDITSUMME, JAHRESZINS, LAUFZEIT)


# =============================================================================
# MATHEMATISCHES FAZIT
# =============================================================================
#
# Was dieser Code zeigt:
#
# 1. GEOMETRISCHE REIHE
#    Die Annuitätenformel ist die Summenformel einer geometrischen Folge.
#    Jeder Monat wird die Restschuld mit dem Faktor (1+r) multipliziert
#    und die Rate R abgezogen.
#
# 2. EXPONENTIALFUNKTION
#    Die Restschuld-Kurve folgt einer Exponentialfunktion — flach am Anfang,
#    dann rasch abfallend. Das ist der Kern des "Zinseszins-Effekts".
#
# 3. MONOTONIE UND ABLEITUNG
#    - d(Zinsanteil)/dt < 0  → Zinsanteil fällt streng monoton
#    - d(Tilgung)/dt > 0     → Tilgungsanteil wächst streng monoton
#    - Rate bleibt konstant  → die Summe beider ist unveränderlich
#
# 4. HALBWERTSZEIT
#    Die Zeit, bis die Hälfte des Kredits getilgt ist, liegt immer
#    NACH der Hälfte der Laufzeit — wegen des Zinseffekts.
#    Bei 4,5 % und 5 Jahren: Halbierung erst nach ~65 % der Laufzeit.
#
# =============================================================================
