import random

from flask import Flask, redirect, render_template, render_template_string, make_response, request, send_from_directory, url_for
from info import turrets
import jester
import os.path

app = Flask(__name__)

links = {
    "coming-soon" : "comingSoon.html",
    "mintmc" : "mintmc.html"
}

replace = {
    "#X" : "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/X.png' )}}\"/></span>",
    
    "#DPS": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/DPS.png' )}}\"/><span style=\"color: #ffffff; font-weight: 550;\">",
    "#DMG": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/DMG.png' )}}\"/><span style=\"color: #ffa040; font-weight: 550;\">",
    "#KB": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/KB.png' )}}\"/><span style=\"color: #40ffcf; font-weight: 550;\">",
    "#PRJ": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/PRJ.png' )}}\"/><span style=\"color: #ffffff; font-weight: 550;\">",
    "#FRT": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/FRT.png' )}}\"/><span style=\"color: #ff40cf; font-weight: 550;\">",
    "#CRT": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/CRT.png' )}}\"/><span style=\"color: #ff7040; font-weight: 550;\">",
    "#ACC": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/ACC.png' )}}\"/><span style=\"color: #40a0ff; font-weight: 550;\">",
    "#RNG": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/RNG.png' )}}\"/><span style=\"color: #ffcf40; font-weight: 550;\">",
    "#SPD": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SPD.png' )}}\"/><span style=\"color: #40ff70; font-weight: 550;\">",
    "#SZE": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SZE.png' )}}\"/><span style=\"color: #cfff40; font-weight: 550;\">",
    "#PWR": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/PWR.png' )}}\"/><span style=\"color: #ffffff; font-weight: 550;\">",
    
    "#HP": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/HP.png' )}}\"/><span style=\"color: #ff4040; font-weight: 550;\">",
    "#SP": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SP.png' )}}\"/><span style=\"color: #4040ff; font-weight: 550;\">",
    "#HM": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/MH.png' )}}\"/><span style=\"color: #40cfff; font-weight: 550;\">",
    "#CR": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/CR.png' )}}\"/><span style=\"color: #40cfff; font-weight: 550;\">",
    "#CD": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/CD.png' )}}\"/><span style=\"color: #40cfff; font-weight: 550;\">",
    "#TS": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/SCL.png' )}}\"/><span style=\"color: #cfff40; font-weight: 550;\">",
    "#MS": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/MS.png' )}}\"/><span style=\"color: #40ff70; font-weight: 550;\">",
    "#RR": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/RR.png' )}}\"/><span style=\"color: #ffffff; font-weight: 550;\">",
    
    "#Explosive": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Explosive.png' )}}\"/><span style=\"color: #ffff00; font-weight: 550;\">",
    "#Area": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Area.png' )}}\"/><span style=\"color: #dfff00; font-weight: 550;\">",
    "#Bounce": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Bounce.png' )}}\"/><span style=\"color: #95aaaa; font-weight: 550;\">",
    "#Burn": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Burn.png' )}}\"/><span style=\"color: #df8080; font-weight: 550;\">",
    "#Pierce": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Pierce.png' )}}\"/><span style=\"color: #00ffff; font-weight: 550;\">",
    "#Homing": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Homing.png' )}}\"/><span style=\"color: #ffff00; font-weight: 550;\">",
    "#Sticky": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Sticky.png' )}}\"/><span style=\"color: #ff8080; font-weight: 550;\">",
    "#Split": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Split.png' )}}\"/><span style=\"color: #95ff55; font-weight: 550;\">",
    "#Flak": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Flak.png' )}}\"/><span style=\"color: #dfff00; font-weight: 550;\">",
    "#Burst": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Burst.png' )}}\"/><span style=\"color: #8080ff; font-weight: 550;\">",
    "#Proximity": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Proximity.png' )}}\"/><span style=\"color: #aaaaaa; font-weight: 550;\">",
    "#Hitscan": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Hitscan.png' )}}\"/><span style=\"color: #00ffff; font-weight: 550;\">",
    
    "#Microbe": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Microbe.png' )}}\"/><span style=\"color: #ff4070; font-weight: 550;\">",
    "#Offspring": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Offspring.png' )}}\"/><span style=\"color: #ffa0b8; font-weight: 550;\">",
    
    "#Biomass": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Biomass.png' )}}\"/><span style=\"color: #ffff40; font-weight: 550;\">",
    "#Research": "<img class=\"symbol\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/stats/Research.png' )}}\"/><span style=\"color: #bf80ff; font-weight: 550;\">",
    
    "#Abyss": "<span style=\"color: #a040ff; font-weight: 550;\">",
    "#Mark": "<span style=\"color: #ff4040; font-weight: 550;\">",
    
    "#B": "<span style=\"font-weight: 550\">",
    
    "#A": "<img class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/A.png' )}}\"/><span style=\"color: #ff40ff; font-weight: 550;\">",
    "#C": "<img class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/C.png' )}}\"/><span style=\"color: #40ffff; font-weight: 550;\">",
    "#G": "<img class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/G.png' )}}\"/><span style=\"color: #a0ff40; font-weight: 550;\">",
    "#T": "<img class=\"acgt\" style=\"display: inline;\" src=\"{{ url_for('static', filename='images/gg/dna/T.png' )}}\"/><span style=\"color: #ffff40; font-weight: 550;\">",
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
    "CriticalDamage": replace["#CRT"] + "Critical Damage",
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
    
    "Depth": replace["#Abyss"] + "Depth",
    "Mark": replace["#Mark"] + "Mark",
    
    "Biomass": replace["#Biomass"] + "Biomass",
    "Research": replace["#Research"] + "Research",
}

def get_colours():
    colours = {
        "background" : "#000000",
        "navbar-left" : "#ff40ff",
        "navbar-right" : "#a0ff40",
        "border" : "#ff40ff",
        "border-interior" : "#40ffff"
    }
    return colours
app.jinja_env.globals.update(get_colours=get_colours)

def get_turrets():
    return turrets
app.jinja_env.globals.update(get_turrets=get_turrets)

def get_turret_info():
    for i,turret in enumerate(turrets):
        if turret.name == request.path.split("/")[-1]:
            if turret.name == "Jester":
                turret.flavor = jester.getFlavor()
                turret.hp = random.randint(20, 60)
                turret.maxHeat = random.randint(50, 200)
                turret.coolingRate = random.randint(50, 200)
                turret.coolingDelay = round(random.randint(50, 200) * 0.01, 2)
            return turret
    return []
app.jinja_env.globals.update(get_turret_info=get_turret_info)

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
        template = template.replace("Turret Scale +" + str(i), "Turret Scale <span style='color: #fffff; font-weight: 550;'>+" + str(i))
        template = template.replace("Turret Scale -" + str(i), "Turret Scale <span style='color: #fffff; font-weight: 550;'>-" + str(i))
        template = template.replace(" +" + str(i), " <span style='color: #00ff00; font-weight: 550;'>+" + str(i))
        template = template.replace(" -" + str(i), " <span style='color: #ff0000; font-weight: 550;'>-" + str(i))
        template = template.replace(str(i) + "%", str(i) + "%</span>")
    template = template.replace("$", "</span>")
    return render_template_string(template)

# Public facing pages.
@app.route("/")
def index():
    return redirect(request.url_root + "/gg/turrets/Guardian")

@app.route("/gg/turrets/<turretName>")
def other_page(turretName):
    for turret in turrets:
        if turret.name == turretName:
            return get_template('turret.html')
    return "Turret Not Found"


# Start the application.
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)