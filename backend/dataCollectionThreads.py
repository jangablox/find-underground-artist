import threading
import requests
from dataColectionFunctions import getAccessTokenCC, fields
import concurrent.futures
import json
from time import sleep
from queue import Queue
from Secrets import CYANITE_SECRET
import csv
from datetime import datetime, timedelta


finishedSet = set({})
toVisit = Queue(maxsize= -1)

def getSimilar(id:str, token, level, dict):
    if level > 2:
        return 
    response = requests.get(
        url=f'https://api.spotify.com/v1/artists/{id}/related-artists',
        headers={
            'Authorization': f'Bearer {token}'
        }   
    )

    if not response.status_code == 200:
        return 

    
    response = response.json()
    for artist in response['artists']:
        dict.append((artist['id'], level))


def getSongInfo(id:str, rep, avgTrack, n):
    
    cyaniteBody = """
    mutation SpotifyTrackEnqueueMutation($input: SpotifyTrackEnqueueInput!) {
        spotifyTrackEnqueue(input: $input) {
            __typename
            ... on SpotifyTrackEnqueueSuccess {
                enqueuedSpotifyTrack {
                    id
                    audioAnalysisV6{
                        __typename
                        ...on AudioAnalysisV6Finished{
                            result{
                                moodTags
                                advancedInstrumentTags
                                bpmRangeAdjusted
                                valence
                                arousal
                                energyLevel
                                emotionalProfile
                                voicePresenceProfile
                                movementTags
                                characterTags
                                advancedSubgenreTags
                                energyDynamics
                                emotionalDynamics
                            }
                        }
                    }
                }
            }
            ... on Error {
                message
            }
        }
    }
    """


    data = requests.post(
        url='https://api.cyanite.ai/graphql',
        headers={
            'Content-Type' : 'application/json',
            'Authorization': f'Bearer {CYANITE_SECRET}'
        },
        json={
            'query': cyaniteBody,
            'variables': '{ "input": { "spotifyTrackId": "' + id + '" } }'
        }
    )

    if not data.status_code == 200:
        return 

    data = json.loads(data.content)
    if data['data'] == None:
        return 
    if data['data']['spotifyTrackEnqueue']['__typename'] == 'SpotifyTrackEnqueueError':
        return 
    audioAnalysis = data['data']['spotifyTrackEnqueue']['enqueuedSpotifyTrack']['audioAnalysisV6']
    if audioAnalysis['__typename'] == 'AudioAnalysisV6Finished':
        for tag in audioAnalysis['result']:
            if audioAnalysis['result'][tag] == None:
                return 
            if tag == 'bpmRangeAdjusted':
                    if 60 <= audioAnalysis['result'][tag] < 80:
                        avgTrack[0]['Adagio'] += 1.0
                    elif 80 <= audioAnalysis['result'][tag] < 100:
                        avgTrack[0]['Andante'] += 1.0
                    elif 100 <= audioAnalysis['result'][tag] < 120:
                        avgTrack[0]['Moderato'] += 1.0
                    elif 120 <= audioAnalysis['result'][tag] < 150:
                        avgTrack[0]['Allegro'] += 1.0
                    else:
                        avgTrack[0]['Vivace'] += 1.0
                
            elif tag == 'valence' or tag == 'arousal':
                if -1 <= audioAnalysis['result'][tag] < -0.666:
                    avgTrack[0][tag + '1']+=1.0
                elif -.666 <= audioAnalysis['result'][tag] < -0.333:
                    avgTrack[0][tag + '2']+=1.0
                elif -.333 <= audioAnalysis['result'][tag] < 0:
                    avgTrack[0][tag + '3']+=1.0
                elif 0 <= audioAnalysis['result'][tag] < 0.333:
                    avgTrack[0][tag + '4']+=1.0
                elif 0.333 <= audioAnalysis['result'][tag] < .666:
                    avgTrack[0][tag + '5']+=1.0
                else:
                    avgTrack[0][tag + '6']+=1.0
                
            elif tag == 'energyLevel' or tag == 'emotionalProfile' or tag == 'voicePresenceProfile' or tag == 'energyDynamics' or tag =='emotionalDynamics':
                avgTrack[0][tag + '-' + audioAnalysis['result'][tag]] += 1.0

            else:
                for tag in audioAnalysis['result'][tag]:
                    avgTrack[0][tag] += 1.0
        n[0] += 1
        
    elif audioAnalysis['__typename'] == 'AudioAnalysisV6Failed':
        return 
    else:
        sleep(3)
        if rep < 2:
            return getSongInfo(id, rep + 1, avgTrack, n)
        return 

    


def getTopTracks(id:str, token, tracks):

    topTracks = requests.get(
        url=f'https://api.spotify.com/v1/artists/{id}/top-tracks?market=US',
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    if topTracks.status_code == 429:
        print('stop')
        return
    topTracks = topTracks.json()
    topTracks = topTracks['tracks']
    for track in topTracks:
        tracks.append(track['id'])
    

def getPopularity(id:str, token, popularity):
    data = requests.get(
        url=f'https://api.spotify.com/v1/artists/{id}',
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    data = data.json()
    popularity.append(data['popularity'])


def getArtistInfo(id, token):
    tracks = []
    tracksThread = threading.Thread(target=getTopTracks(id[0], token, tracks), name='tracksThread')
    similar = []
    similarThread = threading.Thread(target=getSimilar(id[0], token, id[1] + 1, similar), name='similarThread')
    popularity = []
    popularityThread = threading.Thread(target=getPopularity(id[0], token, popularity), name='popularityThread')

    tracksThread.start()
    similarThread.start()
    popularityThread.start()

    tracksThread.join()
    similarThread.join()
    popularityThread.join()


    avgTrack = [{}]
    for field in fields:
        avgTrack[0][field] = 0

    n = [0]

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    for track in tracks:
        pool.submit(getSongInfo(track, 0, avgTrack, n))
    
    pool.shutdown(wait=True)

    for key in avgTrack[0].keys():
        if n[0] == 0:
            avgTrack[0][key] = None
        else:
            avgTrack[0][key] /= n[0]
    
    avgTrack[0]['id'] = id[0]
    avgTrack[0]['popularity'] = popularity[0]

    if not id[0] in finishedSet:
        writer.writerows(avgTrack)

    else:
        return

    finishedSet.add(id[0])
    for artist in similar:
         toVisit.put(artist)



tokens = getAccessTokenCC()

def write0():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[0])

def write1():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[1])

def write2():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[2])

def write3():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[3])

def write4():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[4])

def write5():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[5])

def write6():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[6])

def write7():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[7])

def write8():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[8])

def write9():
    if toVisit.empty() == True:
        return
    curr = toVisit.get()
    if curr[0] in finishedSet:
        return
    getArtistInfo(curr, tokens[9])
        


name = 'origArtists.csv'
f = open(name,'r')
dt = csv.reader(f)
dt = list(dt)
f.close()

MIN = timedelta(minutes=30)
last_update = datetime.now()

dt = dt[0]
for id in dt:
    toVisit.put((id[1:-1], 0))


csvfile = open('ArtistDB.csv', 'w')
writer = csv.DictWriter(csvfile, fieldnames=fields)
writer.writeheader()

while(toVisit.empty() == False):
    now = datetime.now()
    if now - last_update > MIN:
        tokens = getAccessTokenCC()
        last_update = now

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    for i in range(2):
        pool.submit(write0)
        pool.submit(write1)
        pool.submit(write2)
        pool.submit(write3)
        pool.submit(write4)
        pool.submit(write5)
        pool.submit(write6)
        pool.submit(write7)
        pool.submit(write8)
        pool.submit(write9)
    pool.shutdown(wait=True)


csvfile.close()

print('done')    