from django.shortcuts import render, HttpResponse, redirect
import random, datetime
# Create your views here.


def index(request):
    if "balance" in request.session and "winend" in request.session:
        #must fulfill this to win, turns less than condition, money over condition
        if (int(request.session["balance"]) >= int(request.session["winend"]) and int(request.session["turn"]) < int(request.session["turnend"])):
            request.session["win"] = True
        #lose conditions are above 
        elif (int(request.session["turn"])>=int(request.session["turnend"])):
            request.session["lose"]=True
    else:  # we need to make a new session
        request.session["balance"] = 0
        request.session["turn"] = 0
    return render(request, "index.html")


def process_money(request):
    choice = request.POST["building"]
    request.session["turn"] += 1
    # list of the ranges based on location selected to work
    outcomes = {"farm": [10, 20], "cave": [5, 10],
                "home": [2, 5], "casino": [-50, 50]}
    # assign the range then use it in the random int next line
    resultrange = outcomes[choice]
    amountearned = random.randint(resultrange[0], resultrange[1])
    # session balance will always exist by this point
    request.session["balance"] += amountearned
    print(f"balance is {request.session['balance']}")
    date = (datetime.datetime.now()).strftime("%b %d %Y %H:%M:%S")
    activitylog = ''
    if "activity" in request.session:
        pass
    else:
        request.session["activity"] = []
    if amountearned > 0:  # this is how to change the CSS for the good or bad events but i will save this for last
        activitylog = f"<li class='good'>Earned {amountearned} from the {choice}! ({date})</li>"
    else:  # if you fucked up at the casino
        activitylog = f"<li class='bad'>Yikes... you lost {amountearned} from the {choice}! ({date})</li>"
    request.session["activity"].append(activitylog)

    return redirect("/")


# uses the input conditions unless they are blank then it will default
def setWinConditions(request):
    if request.POST["wincondition"] is not None:
        request.session["winend"] = request.POST["wincondition"]
    else:
        request.session["winend"] = 100
    if request.POST["turnend"]:
        request.session["turnend"] = request.POST["turnend"]
    return redirect("/")


def reset(request):
    if ("activity" in request.session):
        del request.session["activity"]
        del request.session["balance"]
    if ("winend" in request.session):
        del request.session["winend"]
        del request.session["turnend"]
    if "win" in request.session:
        del request.session["win"]
    if "lose" in request.session:
        del request.session["lose"]
    return redirect("/")
