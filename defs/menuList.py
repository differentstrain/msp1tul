import os
import time
import platform
from defs.amfCall import AmfCall
from defs.checksumCalc import ticketHeader

#ver.0.4.2

# Cls/Clear.
def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


# Wheel Spin.
def wheel_spins(server, actorId, ticket, lisa_hack_mode=False):
    clear()
    for _ in range(8):
        status_code, response_amf = AmfCall(server, "MovieStarPlanet.WebService.Awarding.AMFAwardingService.claimDailyAward",
                         [ticketHeader(anyAttribute=None, ticket=ticket), "starwheel", 120, actorId])

    for _ in range(8):
        status_code, response_amf = AmfCall(server,
                                    "MovieStarPlanet.WebService.Awarding.AMFAwardingService.claimDailyAward",
                                    [ticketHeader(anyAttribute=None, ticket=ticket), "starVipWheel", 200, actorId])

    for _ in range(4):
        status_code, response_amf = AmfCall(server,
                                    "MovieStarPlanet.WebService.Awarding.AMFAwardingService.claimDailyAward",
                                    [ticketHeader(anyAttribute=None, ticket=ticket), "advertWheelDwl", 240, actorId])

    for _ in range(4):
        status_code, response_amf = AmfCall(server,
                                    "MovieStarPlanet.WebService.Awarding.AMFAwardingService.claimDailyAward",
                                    [ticketHeader(anyAttribute=None, ticket=ticket), "advertWheelVipDwl", 400, actorId])

    if lisa_hack_mode:
        print("Wheel Spin Success >:)")
    else:
        print("Success >:) [Auto redirect in 2 seconds]")
        time.sleep(2)


# Lisa Hack tool, w/o creating bots.
def lisa_hack(server, actorId, ticket):
    
    wheel_spins(server, actorId, ticket, lisa_hack_mode=True)
    
    #Wywołania AMF.
    AmfCall(server, "MovieStarPlanet.WebService.Awarding.AMFAwardingService.RequestIntroductionAward",
            [ticketHeader(anyAttribute=None, ticket=ticket), actorId])
    
    AmfCall(server, "MovieStarPlanet.WebService.AMFAwardService.RequestIntroductionAward",
            [ticketHeader(anyAttribute=None, ticket=ticket), actorId])
            
    AmfCall(server, "MovieStarPlanet.WebService.AMFAwardService.claimDailyAward",
            [ticketHeader(anyAttribute=None, ticket=ticket), "firstRetentionSC", 300, actorId])

    flag2 = False

    for k in range(100):
        AmfCall(server, "MovieStarPlanet.WebService.AMFAwardService.claimDailyAward", 
                [ticketHeader(anyAttribute=None, ticket=ticket), "twoPlayerFame", 50, actorId])
        print("Generated 50 fame")

        AmfCall(server, "MovieStarPlanet.WebService.AMFAwardService.claimDailyAward", 
                [ticketHeader(anyAttribute=None, ticket=ticket), "twoPlayerMoney", 50, actorId])
        print("Generated 50 starcoins")

        if k == 99:
            flag2 = True

    for l in range(3):
        AmfCall(server, "MovieStarPlanet.WebService.Achievement.AMFAchievementWebService.ClaimReward", 
                [ticketHeader(anyAttribute=None, ticket=ticket), "LUCKY_YOU", actorId])

        if flag2:
            print("Success >:) [Auto redirect in 2 seconds]")

# Remove Pixie, Zac and other bots.
def block_defaults(server, actorId, ticket):
    clear()
    for item in [3, 4, 414]:
        AmfCall(server, "MovieStarPlanet.WebService.ActorService.AMFActorServiceForWeb.BlockActor",
                        [ticketHeader(anyAttribute=None, ticket=ticket), actorId, item])
        print(f"Blocked: {item}. Auto redirect in 2 seconds.")
        time.sleep(1)


    