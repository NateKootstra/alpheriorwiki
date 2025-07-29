import random

from flask import Flask, redirect, render_template, render_template_string, make_response, request, send_from_directory, url_for, send_file
import os.path

from info import turrets, perks
import jester

app = Flask(__name__)

links = {
    "coming-soon" : "comingSoon.html",
    "mintmc" : "mintmc.html"
}

replace = {
    "#X" : "<img alt='None' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/X.png' )}}\"/></span>",
    
    "#DPS": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/DPS.png' )}}\"/><span style=\"color: #ffffff; font-weight: bold;\">",
    "#DMG": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/DMG.png' )}}\"/><span style=\"color: #ffa040; font-weight: bold;\">",
    "#KB": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/KB.png' )}}\"/><span style=\"color: #40ffcf; font-weight: bold;\">",
    "#PRJ": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/PRJ.png' )}}\"/><span style=\"color: #ffffff; font-weight: bold;\">",
    "#FRT": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/FRT.png' )}}\"/><span style=\"color: #ff40cf; font-weight: bold;\">",
    "#CRT": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/CRT.png' )}}\"/><span style=\"color: #ff7040; font-weight: bold;\">",
    "#ACC": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/ACC.png' )}}\"/><span style=\"color: #40a0ff; font-weight: bold;\">",
    "#RNG": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/RNG.png' )}}\"/><span style=\"color: #ffcf40; font-weight: bold;\">",
    "#SPD": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SPD.png' )}}\"/><span style=\"color: #40ff70; font-weight: bold;\">",
    "#SZE": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SZE.png' )}}\"/><span style=\"color: #cfff40; font-weight: bold;\">",
    "#PWR": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/PWR.png' )}}\"/><span style=\"color: #ffffff; font-weight: bold;\">",
    
    "#HP": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/HP.png' )}}\"/><span style=\"color: #ff4040; font-weight: bold;\">",
    "#SP": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SP.png' )}}\"/><span style=\"color: #4040ff; font-weight: bold;\">",
    "#HM": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/MH.png' )}}\"/><span style=\"color: #40cfff; font-weight: bold;\">",
    "#CR": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/CR.png' )}}\"/><span style=\"color: #40cfff; font-weight: bold;\">",
    "#CD": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/CD.png' )}}\"/><span style=\"color: #40cfff; font-weight: bold;\">",
    "#TS": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SCL.png' )}}\"/><span style=\"color: #cfff40; font-weight: bold;\">",
    "#MS": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/MS.png' )}}\"/><span style=\"color: #40ff70; font-weight: bold;\">",
    "#RR": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/RR.png' )}}\"/><span style=\"color: #ffffff; font-weight: bold;\">",
    "#BN": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/BN.png' )}}\"/><span style=\"color: #a0a0ff; font-weight: bold;\">",
    
    "#Explosive": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Explosive.png' )}}\"/><span style=\"color: #ffff00; font-weight: bold;\">",
    "#Area": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Area.png' )}}\"/><span style=\"color: #dfff00; font-weight: bold;\">",
    "#Bounce": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Bounce.png' )}}\"/><span style=\"color: #95aaaa; font-weight: bold;\">",
    "#Burn": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Burn.png' )}}\"/><span style=\"color: #df8080; font-weight: bold;\">",
    "#Pierce": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Pierce.png' )}}\"/><span style=\"color: #00ffff; font-weight: bold;\">",
    "#Homing": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Homing.png' )}}\"/><span style=\"color: #ffff00; font-weight: bold;\">",
    "#Sticky": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Sticky.png' )}}\"/><span style=\"color: #ff8080; font-weight: bold;\">",
    "#Split": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Split.png' )}}\"/><span style=\"color: #95ff55; font-weight: bold;\">",
    "#Flak": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Flak.png' )}}\"/><span style=\"color: #dfff00; font-weight: bold;\">",
    "#Burst": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Burst.png' )}}\"/><span style=\"color: #8080ff; font-weight: bold;\">",
    "#Proximity": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Proximity.png' )}}\"/><span style=\"color: #aaaaaa; font-weight: bold;\">",
    "#Hitscan": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Hitscan.png' )}}\"/><span style=\"color: #00ffff; font-weight: bold;\">",
    
    "#Microbe": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Microbe.png' )}}\"/><span style=\"color: #ff4070; font-weight: bold;\">",
    "#Offspring": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Offspring.png' )}}\"/><span style=\"color: #ffa0b8; font-weight: bold;\">",
    
    "#Biomass": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Biomass.png' )}}\"/><span style=\"color: #ffff40; font-weight: bold;\">",
    "#Research": "<img alt='' class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Research.png' )}}\"/><span style=\"color: #bf80ff; font-weight: bold;\">",
    
    "#Abyss": "<span alt='' style=\"color: #a040ff; font-weight: bold;\">",
    "#Mark": "<spanalt=''  style=\"color: #ff4040; font-weight: bold;\">",
    
    "#B": "<span alt='' style=\"font-weight: bold\">",
    
    "#A": "<img alt='' class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/A.png' )}}\"/><span style=\"color: #ff40ff; font-weight: bold;\">",
    "#C": "<img alt='' class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/C.png' )}}\"/><span style=\"color: #40ffff; font-weight: bold;\">",
    "#G": "<img alt='' class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/G.png' )}}\"/><span style=\"color: #a0ff40; font-weight: bold;\">",
    "#T": "<img alt='' class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/T.png' )}}\"/><span style=\"color: #ffff40; font-weight: bold;\">",
}

replaceFull = {
    "Health": replace["#HP"] + "Health",
    "MaxHealth": replace["#HP"] + "Max Health",
    "Shield": replace["#SP"] + "Shield",
    "MaxShield": replace["#SP"] + "Max Shield",
    "HeatMax": replace["#HM"] + "Heat Max",
    "FuelMax": replace["#HM"] + "Fuel Max",
    "ElectricityMax": replace["#HM"] + "Electricity Max",
    "ChargeMax": replace["#HM"] + "Charge Max",
    "GasMax": replace["#HM"] + "Gas Max",
    "ShadeMax": replace["#HM"] + "Shade Max",
    "HeatR": replace["#CR"] + "Cooling Rate",
    "FuelR": replace["#CR"] + "Refuel Rate",
    "RipR": replace["#CR"] + "Refuel Amount",
    "ElectricityR": replace["#CR"] + "Recharge Rate",
    "ChargeR": replace["#CR"] + "Charge Rate",
    "GasR": replace["#CR"] + "Harvest Rate",
    "ShadeR": replace["#CR"] + "Drain Rate",
    "HeatD": replace["#CD"] + "Cooling Delay",
    "FuelD": replace["#CD"] + "Refuel Delay",
    "RipD": replace["#CD"] + "Drain Rate",
    "ElectricityD": replace["#CD"] + "Recharge Delay",
    "ChargeD": replace["#CD"] +"Charge Delay",
    "GasD": replace["#CD"] + "Gas Usage",
    "ShadeD": replace["#CD"] + "Drain Delay",
    "Heat": replace["#HM"] + "Heat",
    "Fuel": replace["#HM"] + "Fuel",
    "Electricity": replace["#HM"] + "Electricity",
    "Charge": replace["#HM"] + "Charge",
    "Gas": replace["#HM"] + "Gas",
    "Shade": replace["#HM"] + "Shade",
    "TurretScale": replace["#TS"] + "Turret Scale",
    "Movespeed": replace["#MS"] + "Movespeed",
    
    "DPS": replace["#DPS"] + "DPS",
    "Damage": replace["#DMG"] + "Damage",
    "Knockback": replace["#KB"] + "Knockback",
    "Projectiles": replace["#PRJ"] + "Projectiles",
    "Firerate": replace["#FRT"] + "Firerate",
    "CriticalHits": replace["#CRT"] + "Critical Hits",
    "CriticalChance": replace["#CRT"] + "Critical Chance",
    "CriticalDamage": replace["#CRT"] + "Critical " + replace["#DMG"] + "</span></span><span style=\"color: #ff7040; font-weight: bold;\">Damage",
    "Accuracy": replace["#ACC"] + "Accuracy",
    "Range": replace["#RNG"] + "Range",
    "Speed": replace["#SPD"] + "Speed",
    "Size": replace["#SZE"] + "Size",
    "Power-upChance": replace["#PWR"] + "Power-up Chance",
    "Power-upDuration": replace["#PWR"] + "Power-up Duration",
    
    "Explosive": replace["#Explosive"] + "Explosive",
    "Area": replace["#Area"] + "Area",
    "Bounce": replace["#Bounce"] + "Bounce",
    "Burn": replace["#Burn"] + "Burn",
    "Pierce": replace["#Pierce"] + "Pierce",
    "Homing": replace["#Homing"] + "Homing",
    "Sticky": replace["#Sticky"] + "Sticky",
    "Split": replace["#Split"] + "Split",
    "Flak": replace["#Flak"] + "Flak",
    "Burst": replace["#Burst"] + "Burst",
    "Proximity": replace["#Proximity"] + "Proximity",
    "Hitscan": replace["#Hitscan"] + "Hitscan",
    
    "Microbe": replace["#Microbe"] + "Microbe",
    "Offspring": replace["#Offspring"] + "Offspring",
    
    "Reroll": replace["#RR"] + "Reroll",
    "Banish": replace["#BN"] + "Banish",
    
    "Depth": replace["#Abyss"] + "Depth",
    "Mark": replace["#Mark"] + "Mark",
    
    "Biomass": replace["#Biomass"] + "Biomass",
    "Research": replace["#Research"] + "Research",
}

def get_colours():
    colours = {
        "background" : "#000000",
        "A" : "#ff40ff",
        "C" : "#40ffff",
        "G" : "#a0ff40",
        "T" : "#ffff40",
        "Abyss" : "#a040ff",
    }
    return colours
app.jinja_env.globals.update(get_colours=get_colours)

def get_turrets():
    return turrets
app.jinja_env.globals.update(get_turrets=get_turrets)

def get_perks():
    return perks
app.jinja_env.globals.update(get_perks=get_perks)

def get_section():
    try:
        if request.path == "/gg":
            return "ggt"
        elif request.path == "/cc":
            return "cct"
        elif request.path.split("/")[1] == "gg":
            return "gg"
        elif request.path.split("/")[1] == "cc":
            return "cc"
    except:
        pass
    return "index"
app.jinja_env.globals.update(get_section=get_section)

def get_page_info():
    try:
        if request.path.split("/")[2] == "turrets":
            for i,turret in enumerate(turrets):
                if turret.name == request.path.split("/")[-1]:
                    if turret.name == "Jester":
                        turret.flavor = jester.getFlavor()
                        turret.hp = random.randint(20, 60)
                        turret.maxHeat = random.randint(50, 200)
                        turret.coolingRate = random.randint(50, 200)
                        turret.coolingDelay = round(random.randint(50, 200) * 0.01, 2)
                    return turret, 'turrets', 'gg'
        elif request.path.split("/")[2] == "perks":
            for i,perk in enumerate(perks):
                if perk.name == request.path.split("/")[-1]:
                    return perk, 'perks', 'gg'
    except:
        pass
    return None, '', ''
app.jinja_env.globals.update(get_page_info=get_page_info)

def get_favicon():
    if request.path.split("/")[1] == "gg":
        try:
            if request.path.split("/")[2] == "turrets":
                return "images/gg/turrets/64x64/" + request.path.split("/")[3] + ".png", "images/gg/turrets/32x32/" + request.path.split("/")[3] + ".png"
            elif request.path.split("/")[2] == "perks":
                return "images/gg/perks/64x64/" + request.path.split("/")[3] + ".png", "images/gg/perks/32x32/" + request.path.split("/")[3] + ".png"
        except:
            pass
        return "images/favicons/gg-64x64.png", "images/favicons/gg-32x32.png"
    elif request.path.split("/")[1] == "cc":
        return "images/favicons/cc-64x64.png", "images/favicons/cc-32x32.png"
    return "images/favicons/base-64x64.png", "images/favicons/base-32x32.png"
app.jinja_env.globals.update(get_favicon=get_favicon)

def get_template(path):
    global replace
    global replacei
    template = render_template(path)
    for key in replace.keys():
        template = template.replace(key, replace[key])
    for key in replaceFull.keys():
        template = template.replace("$" + key + "$", replaceFull[key] + "</span>")
    for key in replaceFull.keys():
        template = template.replace("$" + key, replaceFull[key])
    for i in range(10):
        template = template.replace("Health +" + str(i), "Health <span style='color: #ff4040; font-weight: bold;'>+" + str(i))
        template = template.replace("Health -" + str(i), "Health <span style='color: #ff4040; font-weight: bold;'>-" + str(i))
        template = template.replace("Turret Scale +" + str(i), "Turret Scale <span style='color: #fffff; font-weight: bold;'>+" + str(i))
        template = template.replace("Turret Scale -" + str(i), "Turret Scale <span style='color: #fffff; font-weight: bold;'>-" + str(i))
        template = template.replace("Delay +" + str(i), "Delay <span style='color: #ff0000; font-weight: bold;'>+" + str(i))
        template = template.replace("Delay -" + str(i), "Delay <span style='color: #00ff00; font-weight: bold;'>-" + str(i))
        template = template.replace(" +" + str(i), " <span style='color: #00ff00; font-weight: bold;'>+" + str(i))
        template = template.replace(" -" + str(i), " <span style='color: #ff0000; font-weight: bold;'>-" + str(i))
    template = template.replace("$", "</span>")
    return render_template_string(template)

# Public facing pages.
@app.route("/")
def index():
    return get_template('index.html')

@app.route("/gg")
def gg():
    return get_template('gg.html')

@app.route("/cc")
def cc():
    return get_template('cc.html')

@app.route("/gg/turrets/<turretName>")
def turret(turretName):
    for turret in turrets:
        if turret.name == turretName:
            return get_template('turret.html')
    return "Turret Not Found"

@app.route("/gg/perks/<perkName>")
def perk(perkName):
    for perk in perks:
        if perk.name == perkName:
            return get_template('perk.html')
    return "Perk Not Found"

@app.route("/robots.txt")
def robots():
    return send_file('robots.txt', 'text/plain')

@app.route("/sitemap.txt")
def sitemap():
    return send_file('sitemap.txt', 'text/plain')

# Start the application.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)