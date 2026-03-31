from myBot import MyBot

def main():
    commands_channels = [866907725463289926] # comandos

    adm_roles = [867875024193978368, # ADM
                 861808601421185034, # VICE
                 933768048865853501, # DONA
                 868847569336426546, # DONO
                 ]
    guild = 859442271908266034

    myBot = MyBot(guild=guild,
                  adm_roles=adm_roles,
                  commands_channels=commands_channels)
    myBot.run(myBot.token)

if __name__ == "__main__":
    main()