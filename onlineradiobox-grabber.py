# script to grab the current song playing from https://onlineradiobox.com/<radio station name>/
# created on windows 10 using visual studio code and python 3.8.2

import sys
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

'''

'''

print('onlineRadioBox_grabber_v3\n')

# urls we want to open
urlList = [
        'https://onlineradiobox.com/gr/80smania/',  # 80s Music
        'https://onlineradiobox.com/gr/98fm/',      # 80s Music
        'https://onlineradiobox.com/gr/gogof/',     # 80s Music

        'https://onlineradiobox.com/gr/111radio/',      # Blues n Jazz
        'https://onlineradiobox.com/gr/bluesradio/',    # Blues n Jazz
        'https://onlineradiobox.com/gr/jazztunea/',     # Blues n Jazz

        'https://onlineradiobox.com/gr/chillouttreepines/',     # Chillout n Lounge n Tropical
        'https://onlineradiobox.com/gr/eclecticssoundtrac24/',  # Chillout n Lounge n Tropical
        'https://onlineradiobox.com/gr/nissos/',                # Chillout n Lounge n Tropical
        'https://onlineradiobox.com/gr/psyndorachill/',         # Chillout n Lounge n Tropical

        'https://onlineradiobox.com/gr/boem/',          # Eclectic Radios
        'https://onlineradiobox.com/gr/diva916/',       # Eclectic Radios
        'https://onlineradiobox.com/gr/enlefko877/',    # Eclectic Radios
        'https://onlineradiobox.com/gr/pepper/',        # Eclectic Radios
        'https://onlineradiobox.com/gr/active913/',     # Eclectic Radios
        'https://onlineradiobox.com/gr/stoperithorio/', # Eclectic Radios

        'https://onlineradiobox.com/gr/dalkas/',                # Greek
        'https://onlineradiobox.com/gr/faros/',                 # Greek
        'https://onlineradiobox.com/gr/mple/',                  # Greek
        'https://onlineradiobox.com/gr/party971/',              # Greek
        'https://onlineradiobox.com/gr/rempetikogialigous/',    # Greek

        'https://onlineradiobox.com/gr/chill/',     # House
        'https://onlineradiobox.com/gr/fly881/',    # House

        'https://onlineradiobox.com/gr/athensparty/',   # Pop Top40
        'https://onlineradiobox.com/gr/mad/',           # Pop Top40
        'https://onlineradiobox.com/gr/pirate/',        # Pop Top40

        'https://onlineradiobox.com/gr/boombox/',               # Rap
        'https://onlineradiobox.com/gr/boomboxmainstreamrap/',  # Rap
        'https://onlineradiobox.com/gr/boomboxreggae/',         # Rap

        'https://onlineradiobox.com/gr/dust/',                  # Rock
        'https://onlineradiobox.com/gr/theoldschoolproject/',   # Rock
        'https://onlineradiobox.com/gr/red963/',                # Rock
        'https://onlineradiobox.com/gr/rockblade/',             # Rock
        'https://onlineradiobox.com/gr/gogofgr/',               # Rock

        'https://onlineradiobox.com/gr/dioi/',  # Ska n Punk

        'https://onlineradiobox.com/gr/psyndoratrance/',    # Trance
        'https://onlineradiobox.com/gr/tranceathens/']     # Trance

# testing purposes
urlListT = [
    'https://onlineradiobox.com/gr/psyndoratrance/',
    'https://onlineradiobox.com/gr/tranceathens/']

# list to hold the previous song info for every radio station
global previous_SongInfo
previous_SongInfo = []
# initialize the list
for url in urlList: previous_SongInfo.append('')
#print(previous_SongInfo)

# sanitize the radio station name
def sanitizeStationName(url):
    stationName = url.replace('https://onlineradiobox.com/gr/', '')
    stationName = stationName.replace('/', '')
    #print(stationName)
    return stationName

# convert the track to a Spotify search link
def convertToSpotify(stationName, songName):
    # open the txt file where we will store the songs with the spotify link
    spotifyFile = open(stationName + '_spotify.txt', 'a')

    # make the link clickable in notepad++
    songNameClickable = songName.replace('\'', '').replace('"', '').replace('.', '').replace('&amp;', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('/', ' ').replace('|', ' ').replace(',', ' ').replace('-', ' ').replace(' ', '%20')

    # write the name and spotify search url of the song into the spotify file
    spotifyFile.write(songName + ' -> ' + 'https://open.spotify.com/search/' + songNameClickable + '\n')
    #print(songName + ' -> ' + 'https://open.spotify.com/search/' + songNameClickable)

    spotifyFile.close()

def singleSongGrabbing(url, stationID):
    #print('singleSongGrabbing function is working correctly [id:' + str(stationID) + ']')
    
    # sanitize the radio station name
    stationName = sanitizeStationName(url)
    #print(stationName)
    #print(stationID)

    # open the txt file where we store the songs with the correct station name
    txtfile = open(stationName + '_playlist.txt', 'a')

    # exception handler in case the webpage does not respond or there is a network issue
    try:
         # open webpage with get method
        page = requests.get(url)

        # http_response between 200-400 means OK status
        if page.status_code == 200:
            # print('Successfully opened the web page')

            # get current date and time
            now = datetime.now()

            # format it into dd/mm/YY H:M
            dateNtime = now.strftime('%d/%m/%Y %H:%M:%S')

            # we need a parser, Python built-in HTML parser is enough
            soup = BeautifulSoup(page.text,'html.parser')

            # we find the 'active' class section in order to parse the currently playing song info and url
            soup = soup.find_all('tr', class_ = 'active')
            # print(soup)

            # the soup is a list, cast the soup as a list of strings then select
            # the first element. The song info resides at the second line of the string
            songInfo = str(soup[0]).splitlines()[2]

            # compare the newly acquired song info with the previous one already stored
            # if they are the same then do not store it again
            # if they are not then update the previous song info with the newly acquired info
            global previous_SongInfo
            #print(previous_SongInfo[stationID])
            if songInfo != previous_SongInfo[stationID]:
                #print('New song from ' + stationName + '[id:' + str(stationID) + ']' + ' is different from the previous')
                previous_SongInfo[stationID] = songInfo
                
                # display current radio station name and id on the terminal
                print(stationName + ' [id:' + str(stationID) + ']', end = ' ')

                # trim the <td> tag
                songInfo = songInfo.replace('<td>', '')
                songInfo = songInfo.replace('</td>', '')

                 # trim the <b> tag
                if '<b>' in songInfo: songInfo = songInfo.replace('<b>', ' ')
                if '</b>' in songInfo: songInfo = songInfo.replace('</b>', ' -')

                # remove 'Now Playing' or 'Now On Air' bullshit from the song name
                nowPlayingKeno = 'Now Playing: '
                nowPlaying = 'Now Playing:'
                nowOnAirKeno = 'Now On Air: '
                nowOnAir = 'Now On Air:'

                # decide what to do with the link if (it exists)
                if '<a class="ajax"' not in songInfo:
                    # remove the "Now Playing" from the song name if it exists
                    if nowPlayingKeno in songInfo: songInfo = songInfo.replace(nowPlayingKeno, '')
                    if nowPlaying in songInfo: songInfo = songInfo.replace(nowPlaying, '')

                    # remove "Now On Air" if it exists
                    if nowOnAirKeno in songInfo: songInfo = songInfo.replace(nowOnAirKeno, '')
                    if nowOnAir in songInfo: songInfo = songInfo.replace(nowOnAir, '')

                    # write the song info on the txt file
                    songInfo = songInfo.strip()
                    txtfile.write(dateNtime + ' ' + songInfo + '\n')

                    # update the spotify search link file
                    convertToSpotify(stationName, songInfo)

                    # display the info on the terminal if needed
                    print(dateNtime + ' ' + songInfo)
                else:
                    # trim the <a> tag
                    songInfo = songInfo.replace('<a class="ajax" ', '')
                    songInfo = songInfo.replace('</a>', '')

                    # split the string into two
                    songInfo = songInfo.split('>')

                    # remove the "now playing" from the song name if it exists
                    if nowPlayingKeno in songInfo[1]: songInfo[1] = songInfo[1].replace(nowPlayingKeno, '')   # Mad Radio 107
                    if nowPlaying in songInfo[1]: songInfo[1] = songInfo[1].replace(nowPlaying, '')

                    # remove "Now on Air" if it exists
                    if nowOnAirKeno in songInfo[1]: songInfo[1] = songInfo[1].replace(nowOnAirKeno, '') # Chill Radio
                    if nowOnAir in songInfo[1]: songInfo[1] = songInfo[1].replace(nowOnAir, '')   # Fly FM

                    # store the song name and url
                    songName = songInfo[1].strip()
                    songLink = songInfo[0][:-1].replace('href="', 'https://onlineradiobox.com').strip()

                    # write the song info on the txt file
                    txtfile.write(dateNtime + ' ' + songName + ' -> ' + songLink + '\n')

                    # update the spotify search link file
                    convertToSpotify(stationName, songName)

                    # display the info on the terminal if needed
                    print(dateNtime + ' ' + songName + ' -> ' + songLink)
            else:
                print('.')
        else:
            #print('Webpage unreachable...')
            print(stationName + ' [id:' + str(stationID) + '] Webpage unreachable...')

        # save the file after each song stored
        txtfile.close()

        # make the program stall a little
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        #print('Webpage unreachable...')
        print(stationName + ' [id:' + str(stationID) + '] Webpage unreachable...')

def songGrabbing():
    # get current date and time
    now = datetime.now()
    
    # format it into dd/mm/YY H:M:S
    dateNtime = now.strftime('%d/%m/%Y %H:%M:%S')
    
    # display that a new iteration is starting
    print('Starting new iteration [' + dateNtime + ']')
    
    # stationID is the id of the station name we want to keep track of (range is the same as len(urlList))
    stationID = 0
    
    for url in urlList:
        singleSongGrabbing(url, stationID)
        stationID += 1
        
    print()

# start grabbing songs as soon as the program starts
#songGrabbing()

# due to a bug with version 3.6.3 of apScheduler the first run of the scheduled job does not start immediately
# but instead starts after the specified 'interval' time
# the design of the interval trigger has been fixed in the upcoming v4.0 release so that the first run starts immediately
# as of 2020.12.26 the v4.0 is not yet released
# https://stackoverflow.com/questions/43254531/python-apschedule-blockingscheduler-with-interval-trigger-start-immediately

# initialize the scheduler
scheduler = BlockingScheduler()
# queue the songGrabbing every 90 seconds
scheduler.add_job(songGrabbing, 'interval', seconds = 90)
# start the job (the jobs starts)
scheduler.start()
