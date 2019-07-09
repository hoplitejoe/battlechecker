import re


def statfind(log, j, leng, name):
    k = 0
    while j < leng:
        find = "(-status).+" + name
        y = re.search(find, log[j])
        if y:
            k = j
            break
        else:
            j = j + 1
            continue
    ability_check1 = re.search("ability", log[k])
    if ability_check1:  # finds which pokemon's ability caused the pokemon to be poisoned (doesn't find sync)
        split = re.split("(\|)", log[k])  # separates the log up to find where the setter is name
        split = re.split(":", split[-1])
        split = split[-1].strip()
        result = list((" died from the ability of ", split))
        return result

    item_check = re.search("item", log[k])
    if item_check:  # finds if a pokemon was poisoned by an item, and who gave the item
        while k < leng:
            find = name + ".+(flame|toxic) orb.+from.+move"
            item_switch = re.search(find, log[k])
            if item_switch:
                k = k + 1
                split = re.split("(\|)", log[k])  # separates the log up to find where the setter is name
                split = re.split(":", split[4])
                split = split[-1].strip()
                result = list((" died from the item tricked by ", split))
                return result
            else:
                result = list((" died from it's own item", None))
                return result
    k = k + 1
    while k < leng:
        if re.search(name, log[k]):
            break
        else:
            k = k + 1
        continue
    move_check = re.search("^.move", log[k])  # looks if a move caused the status
    if move_check:  # checks if the status was from a status move
        split = re.split("(\|)", log[k])  # separates the log up to find where the setter is name
        split = re.split(":", split[4])
        split = split[-1].strip()
        result = list((" died from being statused by", split))
        return result

    effect_check = re.search("^..damage.+100$", log[k])  # looks if a move effect caused the status
    if effect_check:  # checks if the status is from a move effect
        k = k + 1
        split = re.split("(\|)", log[k])  # separates the log up to find where the setter is name
        split = re.split(":", split[4])
        split = split[-1].strip()
        result = list((" died from being statused by the move effect of ", split))
        return result

    switch_check = re.search("(^.switch)|((Rock|Spikes)$)", log[k])
    if switch_check:  # checks if the status is from t-spikes
        team = re.search("[12]", log[k])  # finds where the team num is mentioned
        team = team.group()  # splits the team num into the variable "team"
        while k < leng:
            find = "(sidestart.p" + team + ").+Toxic Spikes"  # finds the last time the hazard was set by the other team
            y = re.search(find, log[k])
            if y:
                k = k + 1  # if found, the loop cycles along one to find the setter
                split = re.split("(\|)", log[k])  # separates the log up to find where the setter is name
                split = re.split(":", split[4])
                split = split[-1].strip()
                result = list((" died from the t-spikes set by ", split))
                return result  # returns the hazard setters nickname
            else:
                k = k + 1
                continue
    ability_check2 = re.search("ability", log[k])
    if ability_check2:  # checks if the status is from an ability
        split = re.split("(\|)", log[k])  # separates the log up to find where the setter is name
        split = re.split(":", split[4])
        split = split[-1].strip()
        result = list((" died from being statused by ability of ", split))
        return result

    result = list((" died from being statused in a way i can't find", None))  # generic message if death cause not found
    return result


def suifind(log, j, leng, name):
    find = "^(.move).+" + name + "\|(Explosion|Memento|Self-Destruct|Healing Wish|Lunar Dance|Final Gambit)"
    while j < leng:
        if re.search(find, log[j]):
            result = list((True, j))
            return result
        else:
            j = j + 1
    result = list((False, 0))
    return result


def spikefind(log, j, leng):
    team = re.search("[12]", log[j])  # finds where the team num is mentioned
    team = team.group()  # splits the team num into the variable "team"
    death = log[j].split()  # splits the log so death[-1] can be found, which always gives the hazard the mon died too
    while j < leng:
        find = "(sidestart.p" + team + ").+" + death[-1]  # finds the last time the hazard was set by the other team
        y = re.search(find, log[j])
        if y:
            toxic = re.search(" Toxic Spikes", log[j])
            if toxic:
                continue
            j = j + 1  # if found, the loop cycles along one to find the setter
            split = re.split("(\|)", log[j])  # separates the log up to find where the setter is name
            split = re.split(":", split[4])
            split = split[-1].strip()
            return split  # returns the hazard setters nickname
        else:
            j = j + 1
            continue

