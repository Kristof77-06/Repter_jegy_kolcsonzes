import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_PATH = os.path.join(BASE_DIR, "repter.sql")

with open(SQL_PATH, "r", encoding="utf-8", errors="ignore") as f:
    sql_text = f.read()


def parse_insert(table):
    pattern = rf"INSERT INTO `{table}`.*?VALUES(.*?);"
    m = re.search(pattern, sql_text, re.S)
    if not m:
        return []
    block = m.group(1)
    rows = re.findall(r"\((.*?)\)", block)
    parsed = []
    for r in rows:
        parts = [p.strip().strip("'") for p in r.split(",")]
        parsed.append(parts)
    return parsed


repulo_rows    = parse_insert("repulo")
jaratok_rows   = parse_insert("jaratok")
menetrend_rows = parse_insert("menetrend")


class Plane:
    def __init__(self, pid, tipus, kapacitas):
        self.id = pid
        self.tipus = tipus
        self.kapacitas = int(kapacitas)


class Flight:
    def __init__(self, fid, jaratszam, plane, varos, jegyar):
        self.id = fid
        self.jaratszam = jaratszam
        self.plane = plane
        self.varos = varos
        self.jegyar = int(jegyar)


class ScheduleEntry:
    def __init__(self, nap, indul, erkezik, kapu_id, jegyar_adoval, flight):
        self.nap = nap
        self.indul = indul
        self.erkezik = erkezik
        self.kapu_id = int(kapu_id)
        self.jegyar_adoval = int(jegyar_adoval)
        self.flight = flight


planes = {
    int(pid): Plane(int(pid), tipus, befogado)
    for pid, tipus, befogado in repulo_rows
}

fohaven = "Főhaven"


def jarat_torzs(jaratszam: str) -> str:
    return jaratszam[:-1] if jaratszam.endswith("R") else jaratszam


JARAT_VAROS_MAP = {
    "BF101": "Várkút", "BF104": "Várkút", "BF107": "Várkút", "BF110": "Várkút",
    "BF102": "Délmező", "BF105": "Délmező", "BF108": "Délmező",
    "BF103": "Kővár",  "BF106": "Kővár",  "BF109": "Kővár",
    "KF201": "Aérilon", "KF206": "Aérilon",
    "KF202": "Nordhaven", "KF207": "Nordhaven",
    "KF203": "Solméra", "KF208": "Solméra",
    "KF209": "Valderin", "KF204": "Valderin",
    "KF205": "Elystria", "KF210": "Elystria",
}


def jarat_varos(jaratszam: str) -> str:
    return JARAT_VAROS_MAP[jarat_torzs(jaratszam)]


def jarat_utvonal(flight: Flight) -> str:
    if flight.jaratszam.endswith("R"):
        return f"{flight.varos} → {fohaven}"
    else:
        return f"{fohaven} → {flight.varos}"


BETELT_JARATOK = {"BF104", "BF105", "KF203", "BF103R", "KF202R", "KF209R"}


flights = {}
for fid, jaratszam, repulo_id, jegyar in jaratok_rows:
    flights[int(fid)] = Flight(
        int(fid),
        jaratszam,
        planes[int(repulo_id)],
        jarat_varos(jaratszam),
        jegyar
    )


schedule_entries = []
for mid, jarat_id, nap, indul, erkezik, kapu_id, jegyar_adoval in menetrend_rows:
    schedule_entries.append(
        ScheduleEntry(nap, indul, erkezik, kapu_id, jegyar_adoval, flights[int(jarat_id)])
    )


napok = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat", "Vasárnap"]
cel_varosok = sorted(set(JARAT_VAROS_MAP.values()))

varos_nap_jarat = {v: {n: [] for n in napok} for v in cel_varosok}
for s in schedule_entries:
    varos_nap_jarat[s.flight.varos][s.nap].append(s)


html = """
<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<title>Főhaven – Városnaptárak</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f6fb;
    margin: 0;
    padding: 0 0 40px 0;
}

h1 {
    text-align: center;
    margin-top: 10px;
    color: #1a2a4f;
}

.logo-container {
    text-align: center;
    margin-top: 10px;
}

.logo-container img {
    height: 60px;
}

.city-calendar {
    max-width: 1100px;
    margin: 25px auto;
    background: white;
    border-radius: 0px;
    padding: 18px 20px 22px 20px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    border: 1px solid #dde3f0;
}

.city-title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 14px;
    color: #1a2a4f;
}

.day-row {
    display: flex;
    gap: 10px;
    justify-content: space-between;
}

.day-card {
    flex: 1;
    background: #f0f3ff;
    border-radius: 0px;
    padding: 10px 8px;
    text-align: center;
    cursor: pointer;
    border: 1px solid #c7d2ff;
    transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.1s ease;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.day-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    background: #e4e9ff;
}

.day-card.betelt {
    background: #fbe4e4;
    border-color: #f5b5b5;
    color: #a33a3a;
}

.day-card.no-flight {
    background: #f1f1f1;
    border-style: dashed;
    border-color: #cccccc;
    color: #777;
    cursor: default;
}

.day-name {
    font-weight: bold;
    font-size: 15px;
}

.ticket-container {
    margin-top: 12px;
}

.ticket-box {
    display: flex;
    justify-content: space-between;
    border-radius: 0px;
    padding: 12px 14px;
    margin-bottom: 10px;
    background: #ffffff;
    border: 1px solid #d0d7f2;
}

.left-block {
    flex: 2;
}

.route {
    font-size: 17px;
    font-weight: bold;
    color: #1a2a4f;
    margin-bottom: 4px;
}

.time {
    font-size: 14px;
    color: #333;
    margin-bottom: 4px;
}

.jarat {
    font-size: 13px;
    color: #555;
    margin-bottom: 2px;
}

.repulo {
    font-size: 13px;
    color: #777;
}

.right-top {
    flex: 0.8;
    text-align: right;
    font-size: 14px;
    color: #333;
}

.right-bottom {
    flex: 1;
    text-align: right;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
}

.kapu {
    font-weight: bold;
    margin-bottom: 6px;
}

.szabad {
    font-size: 13px;
    margin-bottom: 6px;
}

.ar-button {
    display: inline-block;
    padding: 6px 10px;
    background: #1f6feb;
    color: white;
    border-radius: 0px;
    font-weight: bold;
    font-size: 13px;
    cursor: pointer;
}

.ar-button:hover {
    background: #1554b8;
}

.ar-betelt {
    display: inline-block;
    padding: 6px 10px;
    background: #c0392b;
    color: white;
    border-radius: 0px;
    font-weight: bold;
    font-size: 13px;
}

.ticket-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 0px;
    padding: 20px 22px 24px 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    z-index: 9999;
    width: 420px;
    max-width: 90%;
    border: 1px solid #d0d7f2;
}

.popup-back {
    font-size: 18px;
    cursor: pointer;
    margin-bottom: 10px;
    color: #1f6feb;
    font-weight: bold;
}

.popup-next {
    margin-top: 14px;
    text-align: right;
    font-size: 14px;
    color: #1f6feb;
    cursor: pointer;
    font-weight: bold;
}

#popup {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.35);
    display: none;
    z-index: 9998;
}
</style>

<script>
var varosLista = [];
"""

for v in cel_varosok:
    html += f"varosLista.push('{v}');\n"

html += """
// Következő adott nap dátuma (hétfővel kezdődő hét)
function kovetkezoDatum(napNev) {
    const napok = ["Hétfő","Kedd","Szerda","Csütörtök","Péntek","Szombat","Vasárnap"];
    const mai = new Date();
    const jsDay = mai.getDay(); // 0=V,1=H,...,6=Szo

    const maiIndex = (jsDay === 0 ? 6 : jsDay - 1);
    const celIndex = napok.indexOf(napNev);

    let diff = celIndex - maiIndex;
    if (diff <= 0) diff += 7;

    const celDatum = new Date();
    celDatum.setDate(mai.getDate() + diff);

    return celDatum.toLocaleDateString("hu-HU", {
        year: "numeric",
        month: "long",
        day: "numeric"
    });
}

window.onload = function() {
    var select = document.getElementById("varosvalaszto");
    varosLista.forEach(function(v) {
        var opt = document.createElement("option");
        opt.value = v;
        opt.textContent = v;
        select.appendChild(opt);
    });
};

function filterCity() {
    var val = document.getElementById("varosvalaszto").value;
    document.querySelectorAll(".city-calendar").forEach(function(div) {
        if (val === "" || div.getAttribute("data-varos") === val) {
            div.style.display = "";
        } else {
            div.style.display = "none";
        }
    });
}

function showTicket(elem) {
    var info = elem.getAttribute("data-info");
    var targetId = elem.getAttribute("data-target");
    var container = document.getElementById(targetId);

    if (elem.classList.contains("no-flight")) {
        return;
    }

    document.querySelectorAll(".ticket-container").forEach(function(c) {
        if (c !== container) {
            c.innerHTML = "";
        }
    });

    if (container.innerHTML.trim() !== "") {
        container.innerHTML = "";
        return;
    }

    // <br><br> alapú blokkok
    var blocks = info.split("<br><br>");

    // Rendezés indulási idő szerint
    blocks.sort(function(a, b) {
        var timeA = a.split("Indulás: ")[1].split("<br>")[0].trim();
        var timeB = b.split("Indulás: ")[1].split("<br>")[0].trim();
        return timeA.localeCompare(timeB);
    });

    var html = "";

    blocks.forEach(function(block) {
        var lines = block.split("<br>");

        var jaratszam = lines.find(x => x.startsWith("Járatszám: ")).replace("Járatszám: ", "");
        var utvonal   = lines.find(x => x.startsWith("Útvonal: ")).replace("Útvonal: ", "");
        var indul     = lines.find(x => x.startsWith("Indulás: ")).replace("Indulás: ", "");
        var erkezik   = lines.find(x => x.startsWith("Érkezés: ")).replace("Érkezés: ", "");
        var repulo    = lines.find(x => x.startsWith("Repülő: ")).replace("Repülő: ", "");
        var kapu      = lines.find(x => x.startsWith("Kapu: ")).replace("Kapu: ", "");
        var ar        = lines.find(x => x.startsWith("Jegyár: ")).replace("Jegyár: ", "");
        var szabad    = lines.find(x => x.startsWith("Szabad: ")).replace("Szabad: ", "");
        var napnev    = lines.find(x => x.startsWith("Nap: ")).replace("Nap: ", "");

        html += '<div class="ticket-box">';

        html += '<div class="left-block">';
        html += '<div class="route">' + utvonal + '</div>';
        html += '<div class="time">' + indul + ' → ' + erkezik + '</div>';
        html += '<div class="jarat">' + jaratszam + '</div>';
        html += '<div class="repulo">' + repulo + '</div>';
        html += '</div>';

        html += '<div class="right-top">';
        html += '<div class="kapu">Kapu: ' + kapu + '</div>';
        html += '</div>';

        html += '<div class="right-bottom">';
        html += '<div class="szabad">Szabad hely: ' + szabad + '</div>';

        if (ar === "Betelt") {
            html += '<div class="ar-betelt">Betelt</div>';
        } else {
            html += '<div class="ar-button" onclick="openTicket(\\''
                + jaratszam + '\\', \\''
                + utvonal   + '\\', \\''
                + indul     + '\\', \\''
                + erkezik   + '\\', \\''
                + repulo    + '\\', \\''
                + kapu      + '\\', \\''
                + szabad    + '\\', \\''
                + napnev    + '\\', \\''
                + ar        + '\\')">'
                + ar + '</div>';
        }

        html += '</div>';
        html += '</div>';
    });

    container.innerHTML = html;
}

function openTicket(jaratszam, utvonal, indul, erkezik, repulo, kapu, szabad, napnev, ar) {
    const datumTeljes = kovetkezoDatum(napnev);

    // Csak a számok maradjanak: 2026. május 1. → 2026. 1.
    const datumRovid = datumTeljes.replace().trim();

    var html = "";
    html += '<div class="ticket-popup">';

    // Bal felső visszanyíl
    html += '<div class="popup-back" onclick="closePopup()">←</div>';

    // Dátum az indulás–érkezés fölött
    html += '<div style="font-size:18px; font-weight:bold; margin-bottom:12px; text-align:center;">'
         + datumRovid + " (" + napnev + ") "
         '</div>';

    // Jegy doboz – belső kék keret nélkül
    html += '<div class="ticket-box" style="border:none; margin-top:10px;">';

    html += '  <div class="left-block">';
    html += '    <div class="route">' + utvonal + '</div>';
    html += '    <div class="time">' + indul + ' → ' + erkezik + '</div>';
    html += '    <div class="jarat">' + jaratszam + '</div>';
    html += '    <div class="repulo">' + repulo + '</div>';
    html += '  </div>';

    html += '  <div class="right-top"><div class="kapu">Kapu: ' + kapu + '</div></div>';

    html += '  <div class="right-bottom">';
    html += '    <div class="szabad">Szabad hely: ' + szabad + '</div>';
    html += '    <div class="ar-button">' + ar + '</div>';
    html += '  </div>';

    html += '</div>'; // ticket-box vége

    // Tovább gomb – fehér részen, középen
    html += '<div class="popup-next" style="float:none; margin-top:20px; text-align:center;">Tovább</div>';

    html += '</div>'; // ticket-popup vége

    const popup = document.getElementById("popup");
    popup.innerHTML = html;
    popup.style.display = "block";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

</script>
</head>
<body>

<div class="logo-container">
    <img src="logo.png" alt="Logó">
</div>

<h1>Főhaven ↔ Városok – Heti naptár</h1>

<label><b>Város választása:</b></label>
<select id="varosvalaszto" onchange="filterCity()">
    <option value="">Mind</option>
</select>

<p>Kattints egy napra a részletes járatinfóhoz, majd a jegyárra a nagy jegy nézethez.</p>

<div id="popup" style="display:none;"></div>
"""

for varos in cel_varosok:
    html += f'<div class="city-calendar" data-varos="{varos}">\n'
    html += f'<div class="city-title">{varos}</div>\n'

    html += '<div class="day-row">\n'
    for nap in napok:
        jaratok = varos_nap_jarat[varos][nap]

        if jaratok:
            if all(j.flight.jaratszam in BETELT_JARATOK for j in jaratok):
                css = "day-card betelt"
            else:
                css = "day-card"

            info = "<br><br>".join(
                "<br>".join([
                    f"Járatszám: {j.flight.jaratszam}",
                    f"Útvonal: {jarat_utvonal(j.flight)}",
                    f"Indulás: {j.indul[:-3]}",
                    f"Érkezés: {j.erkezik[:-3]}",
                    f"Repülő: {j.flight.plane.tipus}",
                    f"Kapu: {j.kapu_id}",
                    (
                        "Jegyár: Betelt"
                        if j.flight.jaratszam in BETELT_JARATOK
                        else f"Jegyár: {j.flight.jegyar} Ft"
                    ),
                    (
                        "Szabad: 0"
                        if j.flight.jaratszam in BETELT_JARATOK
                        else f"Szabad: {round(j.flight.plane.kapacitas * 0.35)}"
                    ),
                    f"Nap: {nap}"
                ])
                for j in jaratok
            )
        else:
            css = "day-card no-flight"
            info = ""

        unique_id = f"{varos}_{nap}".replace(" ", "_")

        html += f'''
<div class="{css}" data-info="{info}" data-target="{unique_id}" onclick="showTicket(this)">
    <div class="day-name">{nap}</div>
</div>
'''
    html += "</div>\n"

    for nap in napok:
        unique_id = f"{varos}_{nap}".replace(" ", "_")
        html += f'<div class="ticket-container" id="{unique_id}"></div>\n'

    html += "</div>\n"

html += """
</body>
</html>
"""

with open("varos_naptarak.html", "w", encoding="utf-8-sig") as f:
    f.write(html)

print("KÉSZ: varos_naptarak.html")
