import json
import urllib.request
import re
from checkfunc import spikefind, statfind, suifind


def replaychecker(url):
    # user inputs replay to check
    print(url)
    url = url + ".json"
    # reads the json string from the website
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)
    json_st = con.read()
    # converts the json to a dict
    data = json.loads(json_st)
    # takes the log data from the dict
    log = data["log"]
    # splits the log line by line creating a list
    log = str.splitlines(log)
    # creates a new list with only relevant log lines, also removes special chars
    log_simple = []
    for i in log:
        # finds and removes chat, and any unneeded logs
        y = re.findall("^.[cljrwu]|^..(boost|super|resisted|hitcount|heal|unboost|enditem|crit)", i)
        if y:
            continue
        else:
            i = re.sub("[?().^$+\[\]*{}]", "", i)
            log_simple.append(i)  # adds the new lines into a new log
            continue
    # creates a list of all pokemon used in a battle
    pkmn = []
    print(log_simple)
    for i in log_simple:
        y = re.search("^.poke.p", i)  # looks for where the pokemon are listed at the front of the log
        if y:
            z = re.search("[A-Z].+", i)  # finds the specific name of the pokemon
            s = z.group()  # takes the found name and adds it to a list of pkmn names
            s = re.sub("item", "", s)
            s = re.sub("F.$|M.$|", "", s)
            s = re.sub("(\|)|,|", "", s)
            s = s.strip()
            pkmn.append(s)
        else:
            continue
    # Prints both of the teams used
    name1 = re.split("\|", log_simple[0])
    name2 = re.split("\|", log_simple[1])
    pkmnno1 = re.split("\|", log_simple[2])
    pkmnno2 = re.split("\|", log_simple[3])
    pkmnno1 = int(pkmnno1[-1])
    pkmnno2 = int(pkmnno2[-1]) + pkmnno1
    pkmnlist1 = []
    pkmnlist2 = []
    x = 0
    while x < pkmnno1:
        pkmnlist1.append(pkmn[x])
        x = x + 1
    while x < pkmnno2:
        pkmnlist2.append(pkmn[x])
        x = x + 1
    end = []
    print(pkmnlist1)
    print("Teams:")
    print(name1[3] + "'s team: ")
    print(*pkmnlist1, sep=", ")
    print(name2[3] + "'s team: ")
    print(*pkmnlist2, sep=", ")
    print("")
    #  aaa = *pkmnlist1, sep=", "
    #  aaa2 = *pkmnlist2, sep = ", "
    #  end.append(f"Teams:\n{name1[3]}'s team",aaa,)
    # loops through each pokemon then the log to find the pokemon's nickname
    replacements = {}
    for i in pkmn:
        find = "(switch).+(" + i + ")"  # sets the search criteria for pokemon i
        for j in log_simple:
            y = re.search(find, j)  # looks for the pokemon switching in, as this is when nick + name are displayed
            if y:
                # find = "p1a!|p2a!|" + i  # finds the specific point the nick is mentioned
                nick_split = re.split("(\|)", j)
                nick = nick_split[4].strip()  # removes whitespace
                nick = re.sub("p.a: ", "", nick)
                replacements[nick] = i  # creates a dictionary of pkmn names and nicknames to allow converting
                break
            else:
                continue
    log_nickless = []
    for i in log_simple:
        for j in replacements:
            find = " " + j + "((\|)|$)"
            if re.search(find, i):
                i = re.sub(j, replacements[j], i)
        log_nickless.append(i)

    log_reverse = log_nickless.copy()
    log_reverse.reverse()  # copies the log and reverses it
    length = len(log_reverse) - 3
    for i in pkmn:
        find = "faint.+" + i  # sets the search criteria
        look = i + "\|0 fnt"  #
        j = 0
        faint_true = False
        fnt_true = False
        while j < length:
            if re.search(find, log_reverse[j]):
                faint_point = j
                faint_true = True
                while j < length:
                    if re.search(look, log_reverse[j]):
                        fnt_point = j
                        fnt_true = True
                        break
                    else:
                        j = j + 1
                        continue
            else:
                j = j + 1
                continue
        if faint_true and fnt_true:
            fro = re.search("from", log_reverse[fnt_point])  # checks if a pokemon has died from a move, or other damage
            if fro:  # if y then it died from something other than damage
                death = re.split("\|",
                                 log_reverse[fnt_point])  # last word is always the cause, so splits to find the word
                death = re.sub("from ", "", death[-1])
                if death[-1] == "Spikes" or death == "Stealth Rock":
                    setter = spikefind(log_reverse, fnt_point, length)
                    print(f"{i} died from {death} set by {setter}")
                    end.append(f"{i} died from {death} set by {setter}")
                elif death[-1] == "brn" or death == "psn":
                    cause = statfind(log_reverse, fnt_point, length, i)
                    if cause[1] is None:
                        print(i + cause[0])
                        end.append(f"{i} {cause[0]}")
                    else:
                        print(i + cause[0] + " " + cause[1])
                        end.append(f"{i} {cause[0]} {cause[1]}")
                else:
                    print(f"{i} died from {death}")
                    end.append(f"{i} died from {death}")
            else:
                fnt_point = fnt_point + 1
                killer = re.split("\|", log_reverse[fnt_point])
                killer = re.split(":", killer[2])
                killer = killer[-1].strip()
                print(f"{i} was killed by {killer} !")
                end.append(f"{i} was killed by {killer}!")
        elif faint_true and not fnt_true:
            self_own = suifind(log_reverse, faint_point, length, i)
            if self_own[0] is True:
                death = re.split("\|", log_reverse[self_own[1]])
                print(f"{i} killed itself using {death[3]}")
                end.append(f"{i} killed itself using {death[3]}")
            else:
                print(f"{i} died in an unusual way i've not coded for, sorry!")
                end.append(f"{i} died in an unusual way i've not coded for, sorry!")
        else:
            continue
    # for x in log_reverse:
    # print(x)
    print(end)
    return end
