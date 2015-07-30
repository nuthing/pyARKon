import srcds as rcon
import time
import ConfigParser
import os
import errno
import getpass
import sys

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
cmdList.append(['kickplayer', '<Steam64ID>', 'kick player by steamID, cmd>>listplayers'])
cmdList.append(['allowplayertojoinnocheck', '<PlayerName>', 'add user to the whitelist, cmd>>listplayers'])
cmdList.append(['disallowplayertojoinnocheck', '<PlayerName>', 'remove user from whitelist, cmd>>listplayers'])
cmdList.append(['banplayer', '<Steam64ID>', 'ban player by steamID, cmd>>listplayers'])
cmdList.append(['unbanplayer', '<Steam64ID>', 'unban player by steamID'])
cmdList.append(['playersonly', '', 'Freeze crafting and creature movement'])
# server commands
cmdList.append(['slomo', '<0.0 - 5.0>', 'Speed up or slow down server time float multiplier'])
cmdList.append(['pause', '', 'Pauses the server.'])
cmdList.append(['destroyallenemies', '', 'WARNING(death): destroy all enemy/dino'])
cmdList.append(['saveworld', '', 'CAUTION(lag): force world save'])
cmdList.append(['doexit', '', 'WARNING(corruption): kill server!! in rcon cmd>>pause cmd>>saveworld cmd>>doexit'])
cmdList.append(['settimeofday', '<00:00 - 23:59>', 'set time of day, 24hr separated by hrs:min'])
# chat commands
cmdList.append(['setmessageoftheday', '<message>', 'sets the MOTD'])
cmdList.append(['showmessageoftheday', '<seconds>', 'displays the current MOTD'])
cmdList.append(['broadcast', '<message>', 'broadcast a message in the MOTD window to all players'])
cmdList.append(['getchat', '', 'get chat log from server, if chat loggin is set to True, logs to Chat.log'])
cmdList.append(['serverchat', '<message>', 'send a message from rcon to the server in chat window'])
cmdList.append(['serverchatto', '<Steam64ID> <message>', 'msg user by steamID(steamID in quotes)'])
cmdList.append(['serverchattoplayer', '<PlayerName> <message>', 'msg user by playername(playername in quotes)'])
# program commands
cmdList.append(['man', '<cmd>', 'man <cmd>    info about command'])
cmdList.append(['help', '', 'prints back this list of commands'])
cmdList.append(['history', '[(cmd)|chat]', 'show chat/cmd history, use getchat to save chat history'])
cmdList.append(['clear', '[(cmd)|chat]', 'clear chat/cmd history, no argument will clear cmd history'])

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
        if config.has_option('pyARKon', 'logs'):
            conf['logs'] = config.getboolean('pyARKon', 'logs')
        else:
            config.set('pyARKon', 'logs', 'False')

            if os.path.isfile('settings.cfg'):
                with open('settings.cfg', 'w') as configfile:
                    config.write(configfile)
            else:
                with open('settings.cfg', 'wb') as configfile:
                    config.write(configfile)

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
            # cfg_input['pass'] = raw_input('Raw Password>>')
            cfg_input['timeout'] = 15
            cfg_input['sleep'] = 3
            cfg_input['debug'] = False
            cfg_input['logs'] = raw_input('Log chat to file: True/False>>')
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
                config.set('pyARKon', 'ogs', cfg_input['logs'])
                conf['host'] = cfg_input['host']
                conf['port'] = int(cfg_input['port'])
                conf['pass'] = cfg_input['timeout']
                conf['timeout'] = cfg_input['timeout']
                conf['sleep'] = cfg_input['sleep']
                conf['debug'] = cfg_input['debug']
                conf['logs'] = cfg_input['logs']

                if os.path.isfile('settings.cfg'):
                    with open('settings.cfg', 'w') as configfile:
                        config.write(configfile)
                else:
                    with open('settings.cfg', 'wb') as configfile:
                        config.write(configfile)
                break

    if conf['debug']:
        print 'Debug: ENABLED'

    print 'help, for a list of commands'
    print 'man <cmd>, for info about the command'

    while 1:
        if conf['debug']:
            print sys.argv
            print len(sys.argv)

        if len(sys.argv) > 1:
            cmd_input = str(' '.join(sys.argv[1:]))

        else:
            cmd_input = raw_input('CMD>>')

        cmdHistory.append('[H]>CMD>'+cmd_input)
        if conf['logs']:
            try:
                os.makedirs("logs")
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    print 'Unable to create logs folder.'
            cmdHist = open("logs\CMD.log", "a")
            cmdHist.write(time.strftime("[%m/%d/%Y %H:%M:%S %p] ") + cmd_input + '\n')
            cmdHist.close()

        if cmd_input.split(' ', 1)[0] == 'help':
            for x in range(len(cmdList)):
                print cmdList[x][0] + ' ' + cmdList[x][1]
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
                            if conf['logs']:
                                for cmdHist in open("logs\CMD.log").read().splitlines():
                                    print cmdHist
                            else:
                                for y in range(len(cmdHistory)):
                                    print cmdHistory

                        elif cmd_input.split(' ', 1)[1] == 'chat':
                            rcon_return = con.rcon('getchat')
                            if conf['logs']:
                                try:
                                    os.makedirs("logs")
                                except OSError as exception:
                                    if exception.errno != errno.EEXIST:
                                        print 'Unable to create logs folder.'
                                clHist = open("logs\Chat.log", "a")
                            for chatline in rcon_return.splitlines():
                                if len(chatline) > 1 and not chatline.__contains__('Server received, But no response!!'):
                                    chatHistory.append(chatline)
                                    if conf['logs']:
                                        clHist.write(chatline + '\n')
                            if conf['logs']:
                                clHist.close()

                            rcon_return = None
                            if conf['logs']:
                                for chatHist in open("logs\Chat.log").read().splitlines():
                                    print chatHist
                            else:
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

                    elif len(cmd_input.split(' ', 1)) == 1 and cmdList[x][0] == 'broadcast':
                        print '-bash: Missing cmd argument. Type man broadcast for help.'

                    elif len(cmd_input.split(' ')) == 1 and cmdList[x][0] == 'getchat':
                        rcon_return = con.rcon(cmdList[x][0])
                        if conf['logs']:
                            try:
                                os.makedirs("logs")
                            except OSError as exception:
                                if exception.errno != errno.EEXIST:
                                    print 'Unable to create logs folder.'
                            clHist = open("logs\Chat.log", "a")
                        for chatline in rcon_return.splitlines():
                            if len(chatline) > 1 and not chatline.__contains__('Server received, But no response!!'):
                                chatHistory.append(chatline)
                                print chatline
                                if conf['logs']:
                                    clHist.write(chatline + '\n')
                        if conf['logs']:
                            clHist.close()
                        if range(len(rcon_return.splitlines())) == 0:
                            print 'There are currently no messages to retrieve from the server.'
                            break

                        rcon_return = None

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
                        cmdHistory.append('[H]>PlayerID>' + player_input)
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
                            print 'That player is not currently in the server.'
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
            print '-bash: That command is not supported. Type help after CMD>> for a list of commands.'

        if len(sys.argv) > 1:
            break
        else:
            pass

    print 'Disconnected from ARK Server RCON'
