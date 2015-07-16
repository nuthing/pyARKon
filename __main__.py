import srcds as rcon
import time
import ConfigParser
import os.path
import getpass

cmd_ran = False
rcon_return = None
connectedPlayers = []
chatHistory = []
cmdHistory = []
cmdList = []
conf = {}

# # # # # # # # # # # # # # #
#  ADVANCED CONFIGURATION   #
# # # # # # # # # # # # # # #
# [syntax]: cmdList.append([<RconCommand>, <SanityVariable>, <Description>])
# player commands
cmdList.append(['listplayers', '', 'list current players in the server'])
cmdList.append(['kickplayer', '<Steam64ID>', 'kick player from server, cmd>>listplayers'])
cmdList.append(['allowplayertojoinnocheck', '<playername>', 'whitelist player to re-join even if server locked, cmd>>listplayers'])
cmdList.append(['disallowplayertojoinnocheck', '<playername>', 'removes user from whitelist, cmd>>listplayers'])
cmdList.append(['banplayer', '<Steam64ID>', 'ban player by steam id from server, cmd>>listplayers'])
cmdList.append(['unbanplayer', '<Steam64ID>', 'unban player from server'])
cmdList.append(['playersonly', '', 'stop/pause craft&creature movement'])
# server commands
cmdList.append(['slomo', '<0.0>', 'speeds up server time, uses float max of 5.0?'])
cmdList.append(['pause', '', 'Pause server.'])
cmdList.append(['destroyallenemies', '', 'WARNING(death): destroy all enemy/dino'])
cmdList.append(['saveworld', '', 'CAUTION(lag): force world save'])
cmdList.append(['quit', '', 'WARNING(corruption): kill server!! in rcon cmd>>pause cmd>>saveworld cmd>>quit'])
cmdList.append(['settimeofday', '<06:00:00>', 'set time of day, 24hr seperated by hrs:min:sec'])
# chat commands
cmdList.append(['setmessageoftheday', '<message>', 'sets the MOTD for everyone in the server'])
cmdList.append(['showmessageoftheday', '<seconds>', 'displays the current MOTD for everyone in the server'])
cmdList.append(['broadcast', '<message>', 'broadcast your message in the MOTD window to all the players currently online'])
cmdList.append(['getchat', '', 'gets chat logs from ark server'])
cmdList.append(['serverchat', '<message>', 'send a message from rcon to the entire server in chat window'])
cmdList.append(['serverchatto', '<user> <message>', 'send a message to a specific user through the in-game chat window'])
# program commands
cmdList.append(['man', '<cmd>', 'man <cmd>    info about command'])
cmdList.append(['help', '', 'prints back this list of commands'])
# TODO: store history in a file
cmdList.append(['history', '[cmd|chat]', 'show history of cmd or chat (use getchat to save chat history), in non selected will show cmd history'])
cmdList.append(['clear', '[cmd|chat]', 'clear cmd or chat history, in non selected will clear cmd history'])

if __name__ == '__main__':
    print '         pyARKon'

    config = ConfigParser.RawConfigParser()
    if os.path.isfile('settings.cfg'):
        config.read('settings.cfg')
        conf['host'] = config.get('pyARKon', 'host')
        conf['port'] = int(config.get('pyARKon', 'port'))
        conf['pass'] = config.get('pyARKon', 'pass')
        conf['timeout'] = int(config.get('pyARKon', 'timeout'))
        conf['sleep'] = int(config.get('pyARKon', 'sleep'))
        conf['debug'] = config.getboolean('pyARKon', 'debug')

        try:
            con = rcon.SourceRcon(conf['host'], conf['port'], conf['pass'], conf['timeout'])
            con.rcon('listplayers')
            test_pass = True

        except:
            print 'Unable to connect to RCON!'
            test_pass = False

    else:
        test_pass = False

    if not test_pass:
        print 'You need to configure your settings before using this program.'

        while 1:
            cfg_input = {}
            cfg_input['host'] = raw_input('ARK RCON IP>>')
            cfg_input['port'] = raw_input('ARK RCON PORT>>')
            cfg_input['pass'] = getpass.getpass('ARK RCON Password>>')
            cfg_input['timeout'] = 15
            cfg_input['sleep'] = 3
            cfg_input['debug'] = False

            try:
                con = rcon.SourceRcon(cfg_input['host'], int(cfg_input['port']), cfg_input['pass'], int(cfg_input['timeout']))
                con.rcon('listplayers')
                test_pass = True

            except:
                print 'Unable to connect to RCON!'
                test_pass = False

            if test_pass:
                config.add_section('pyARKon')
                config.set('pyARKon', 'host', cfg_input['host'])
                config.set('pyARKon', 'port', int(cfg_input['port']))
                config.set('pyARKon', 'pass', cfg_input['pass'])
                config.set('pyARKon', 'timeout', cfg_input['timeout'])
                config.set('pyARKon', 'sleep', cfg_input['sleep'])
                config.set('pyARKon', 'debug', cfg_input['debug'])
                conf['host'] = cfg_input['host']
                conf['port'] = int(cfg_input['port'])
                conf['pass'] = cfg_input['timeout']
                conf['timeout'] = cfg_input['timeout']
                conf['sleep'] = cfg_input['sleep']
                conf['debug'] = cfg_input['debug']

                with open('settings.cfg', 'w') as configfile:
                    config.write(configfile)
                break

    try:
        con = rcon.SourceRcon(conf['host'], conf['port'], conf['pass'], conf['timeout'])
    except:
        print 'Unable to connect to RCON!'

    if conf['debug']:
        print 'Debug: ENABLED'

    print 'help, for a list of commands'
    print 'man <cmd>, for info about the command'

    while 1:
        cmd_input = raw_input('CMD>>')
        cmdHistory.append('[H]>CMD>'+cmd_input)

        if cmd_input.split(' ', 1)[0] == 'help':
            for x in range(len(cmdList)):
                print cmdList[x][0]
                cmd_ran = True

        elif len(cmd_input.split(' ', 1)) == 1 and cmd_input.split(' ', 1)[0] == 'history':
            for x in range(len(cmdHistory)):
                print cmdHistory[x]
                cmd_ran = True

        elif len(cmd_input.split(' ', 1)) == 1 and cmd_input.split(' ', 1)[0] == 'clear':
            for x in range(len(cmdHistory)):
                cmdHistory.remove(x)
                print 'History of cmd has been cleared.'
                cmd_ran = True

        elif cmd_input.split(' ', 1)[0] == 'man':
            if len(cmd_input.split(' ', 1)) > 1:
                for x in range(len(cmdList)):
                    if cmdList[x][0] == cmd_input.split(' ', 1)[1]:
                        print 'syntax: ' + cmdList[x][0] + ' ' + cmdList[x][1]
                        print 'Description: ' + cmdList[x][2]
                        cmd_ran = True
                        break
            else:
                print '-bash: Missing cmd argument. Type man man for help.'
                cmd_ran = True

        elif cmd_input.split(' ')[0] == 'exit':
            con.disconnect()
            break

        else:
            for x in range(len(cmdList)):
                if cmdList[x][0] == cmd_input.split(' ', 1)[0]:
                    cmd_ran = True

                    if conf['debug']:
                        print 'cmdlist: '+ cmdList[x][0]
                        print 'cmd_input.split: '+ cmd_input.split(' ', 1)[0]
                        print 'len(cmd_input.split): '+ str(len(cmd_input.split(' ')))

                    if len(cmd_input.split(' ', 1)) > 1 and cmdList[x][0] == 'history':
                        if cmd_input.split(' ', 1)[1] == 'cmd':
                            for y in range(len(cmdHistory)):
                                print cmdHistory[y]

                        elif cmd_input.split(' ', 1)[1] == 'chat':
                            for y in range(len(chatHistory)):
                                print chatHistory[y]

                        else:
                            print '-bash: Unknown cmd argument. Type man history for help.'

                    elif len(cmd_input.split(' ', 1)) > 1 and cmd_input.split(' ', 1)[0] == 'clear':
                        if cmd_input.split(' ', 1)[1] == 'cmd':
                            for y in range(len(cmdHistory)):
                                cmdHistory.remove(y)
                                print 'History for cmd has been cleared.'

                        elif cmd_input.split(' ', 1)[1] == 'chat':
                            for y in range(len(chatHistory)):
                                chatHistory.remove(y)
                                print 'History for chat has been cleared.'

                        else:
                            print '-bash: Unknown cmd argument. Type man clear for help.'

                    elif cmdList[x][0] == 'quit':
                        print 'Are you sure you want to KILL your server?'
                        print 'Note: Unless you CMD>>saveworld, you may loose progress in your world!'
                        quit_input = raw_input('KillServer [y/N]')
                        cmdHistory.append('[H]>KillServer [y/N]>' + quit_input)

                        if quit_input.split(' ', 1)[0] == ('y' or 'Y'):
                             rcon_return = con.rcon(cmdList[x][0])
                        else:
                            break

                    elif len(cmd_input.split(' ', 1)) == 1 and cmdList[x][0] == 'broadcast':
                        print '-bash: Missing cmd argument. Type man broadcast for help.'

                    elif len(cmd_input.split(' ')) == 1 and cmdList[x][0] == 'getchat':
                        rcon_return = con.rcon(cmdList[x][0])

                        for chatline in rcon_return.splitlines():
                           chatHistory.append(chatline)
                        rcon_ran = True

                        if range(len(rcon_return.splitlines())) == 0:
                            print 'There are currently no messages to retrieve on the server.'
                            break

                    elif len(cmd_input.split(' ')) == 1 and cmdList[x][0] == 'listplayers':
                        rcon_return = con.rcon(cmdList[x][0])
                        conPlayerAppend = []
                        connectedPlayers = []
                        for player in rcon_return.splitlines():
                            if player != '' and player != ' ':
                                player_array = []
                                player_array.append(player)
                                player_array[0] = player_array[0].replace(' ', '')
                                comArray2 = player_array[0].replace('.', ',', 1)
                                playerData = comArray2.split(',')
                                connectedPlayers.append(playerData)
                        rcon_ran = True
                        if range(len(connectedPlayers)) == 0:
                            print 'There are currently no players on the server.'
                            break

                    elif len(cmd_input.split(' ')) == 1 and (cmdList[x][0] is 'kickplayer' or cmdList[x][0] is 'banplayer'):
                        rcon_return = con.rcon('listplayers')
                        conPlayerAppend = []
                        connectedPlayers = []
                        for player in rcon_return.splitlines():
                            if player != '' and player != ' ':
                                player_array = []
                                player_array.append(player)
                                player_array[0] = player_array[0].replace(' ', '')
                                comArray2 = player_array[0].replace('.', ',', 1)
                                playerData = comArray2.split(',')
                                connectedPlayers.append(playerData)
                        if range(len(connectedPlayers)) == 0:
                            print 'There are currently no players on the server.'
                            break

                        print 'Select a player by ID Number'
                        print rcon_return

                        player_input = raw_input('PlayerID>>')
                        cmdHistory.append('[H]>PayerID>' + player_input)
                        if player_input.split(' ')[0] is not None:
                            playerSteam = connectedPlayers[int(player_input.split(' ', 1)[0])][2]
                            rcon_return = con.rcon(cmdList[x][0] + ' ' + playerSteam)
                        else:
                            print 'No player selected.'
                            break

                    elif len(cmd_input.split(' ')) > 1 and cmdList[x][0] is 'kickplayer':
                        rcon_return = con.rcon('listplayers')
                        conPlayerAppend = []
                        connectedPlayers = []
                        player_found = False
                        for player in rcon_return.splitlines():
                            if player is not '' and player is not ' ' and player is cmd_input.split(' ', 1)[1]:
                                player_array = []
                                player_array.append(player)
                                player_array[0] = player_array[0].replace(' ', '')
                                comArray2 = player_array[0].replace('.', ',', 1)
                                playerData = comArray2.split(',')
                                rcon_return = con.rcon(cmdList[x][0] + ' ' + playerData[2])
                                player_found = True
                        if not player_found:
                            print 'That player is currently not in the server.'
                            break

                    elif len(cmd_input.split(' ')) > 1:
                        rcon_return = con.rcon(cmdList[x][0] + ' ' + cmd_input.split(' ', 1)[1])

                    else:
                        rcon_return = con.rcon(cmdList[x][0])

        if cmd_ran:
            if rcon_return is not None:
                if rcon_return == 'Server received, But no response!!':
                    pass
                else:
                    print rcon_return
                time.sleep(conf['sleep'])
                rcon_return = None
            cmd_ran = False
        else:
            print '-bash: That command is not support. Type help after CMD>> for a list of commands.'

    print 'Disconnected from ARK Server RCON'
