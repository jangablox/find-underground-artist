from Secrets import CYANITE_SECRET, CLIENT_ID, CLIENT_SECRET
import requests
import json
import base64
from time import sleep

fields =['id',
    'popularity',
    'aggressive',
    'calm',
    'chilled',
    'dark',
    'energetic',
    'epic',
    'happy',
    'romantic',
    'sad',
    'scary',
    'sexy',
    'ethereal',
    'uplifting',
    'ambiguous',
    'percussion',
    'synth',
    'piano',
    'acousticGuitar',
    'electricGuitar',
    'strings',
    'bass',
    'bassGuitar',
    'brass',
    'woodwinds',
    'bouncy', 
    'driving',
    'flowing',
    'groovy',
    'nonrhythmic',
    'pulsing',
    'robotic',
    'running',
    'steady',
    'stomping' ,
    'bold',
    'cool',
    'epic',
    'ethereal',
    'heroic',
    'luxurious',
    'magical',
    'mysterious',
    'playful',
    'powerful',
    'retro',
    'sophisticated',
    'sparkling',
    'sparse',
    'unpolished',
    'warm',
    'bluesRock' ,
    'folkRock' ,
    'hardRock' ,
    'indieAlternative' ,
    'psychedelicProgressiveRock' ,
    'punk' ,
    'rockAndRoll' ,
    'popSoftRock' ,
    'abstractIDMLeftfield' ,
    'breakbeatDnB' ,
    'deepHouse' ,
    'electro' ,
    'house' ,
    'minimal' ,
    'synthPop' ,
    'techHouse' ,
    'techno' ,
    'trance' ,
    'contemporaryRnB' ,
    'gangsta' ,
    'jazzyHipHop' ,
    'popRap' ,
    'trap' ,
    'blackMetal' ,
    'deathMetal' ,
    'doomMetal' ,
    'heavyMetal' ,
    'metalcore' ,
    'nuMetal' ,
    'disco' ,
    'funk' ,
    'gospel' ,
    'neoSoul' ,
    'soul' ,
    'bigBandSwing' ,
    'bebop' ,
    'contemporaryJazz' ,
    'easyListening' ,
    'fusion' ,
    'latinJazz' ,
    'smoothJazz' ,
    'country' ,
    'folk' ,
    'energyLevel-variable' ,
    'energyLevel-medium' ,
    'energyLevel-high' ,
    'energyLevel-low' ,
    'energyDynamics-low' ,
    'energyDynamics-medium' ,
    'energyDynamics-high' ,
    'emotionalProfile-variable' ,
    'emotionalProfile-negative' ,
    'emotionalProfile-balanced' ,
    'emotionalProfile-positive' ,
    'emotionalDynamics-low' ,
    'emotionalDynamics-medium' ,
    'emotionalDynamics-high' ,
    'voicePresenceProfile-none' ,
    'voicePresenceProfile-low' ,
    'voicePresenceProfile-medium' ,
    'voicePresenceProfile-high' ,
    'Adagio' ,
    'Andante' ,
    'Moderato' , 
    'Allegro' ,
    'Vivace' ,
    'valence1',
    'valence2',
    'valence3',
    'valence4',
    'valence5',
    'valence6',
    'arousal1',
    'arousal2',
    'arousal3',
    'arousal4',
    'arousal5',
    'arousal6'
    ]



def getAccessTokenCC():
    tokens = []
    for i in range(len(CLIENT_ID)):

        clientCred = f'{CLIENT_ID[i]}:{CLIENT_SECRET[i]}'
        b64ClientCred = base64.b64encode(clientCred.encode())
        df = b64ClientCred.decode()
        token = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': f'Basic {b64ClientCred.decode()}' ,
                'Content-Type': 'application/x-www-form-urlencoded'	
            },
            data={
                'grant_type':'client_credentials'
            }
        )

        tokens.append(token.json()['access_token'])
    return tokens


def getArtistData(id:str, token:str):
    data = requests.get(
        url=f'https://api.spotify.com/v1/artists/{id}',
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    data = data.json()

    topTracks = requests.get(
        url=f'https://api.spotify.com/v1/artists/{id}/top-tracks?market=US',
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    topTracks = topTracks.json()

    avgTrack = [{}]
    for field in fields:
        avgTrack[0][field] = 0
    
    n = 0
    for track in topTracks["tracks"]:
        temp = getSongInfo(track["id"],0)
        if not temp == None:
            for metric in temp:
                if metric == 'bpmRangeAdjusted':
                    if 60 <= temp[metric] < 80:
                        avgTrack[0]['Adagio'] += 1.0
                    elif 80 <= temp[metric] < 100:
                        avgTrack[0]['Andante'] += 1.0
                    elif 100 <= temp[metric] < 120:
                        avgTrack[0]['Moderato'] += 1.0
                    elif 120 <= temp[metric] < 150:
                        avgTrack[0]['Allegro'] += 1.0
                    else:
                        avgTrack[0]['Vivace'] += 1.0
                
                elif metric == 'valence' or metric == 'arousal':
                    if -1 <= temp[metric] < -0.666:
                        avgTrack[0][metric + '1']+=1.0
                    elif -.666 <= temp[metric] < -0.333:
                        avgTrack[0][metric + '2']+=1.0
                    elif -.333 <= temp[metric] < 0:
                        avgTrack[0][metric + '3']+=1.0
                    elif 0 <= temp[metric] < 0.333:
                        avgTrack[0][metric + '4']+=1.0
                    elif 0.333 <= temp[metric] < .666:
                        avgTrack[0][metric + '5']+=1.0
                    else:
                        avgTrack[0][metric + '6']+=1.0
                
                elif metric == 'energyLevel' or metric == 'emotionalProfile' or metric == 'voicePresenceProfile' or metric == 'energyDynamics' or metric =='emotionalDynamics':
                    avgTrack[0][metric + '-' + temp[metric]] += 1.0

                else:
                    for tag in temp[metric]:
                        avgTrack[0][tag] += 1.0
            n += 1.0

    for key in avgTrack[0].keys():
        if n == 0:
            avgTrack[0][key] = None
        else:
            avgTrack[0][key] /= n

    avgTrack[0]['id'] = id
    avgTrack[0]['popularity'] = data['popularity']
    
    return avgTrack
                                


    


def getSongInfo(id:str, rep):
    
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
        return None

    data = json.loads(data.content)
    if data['data'] == None:
        return None
    if data['data']['spotifyTrackEnqueue']['__typename'] == 'SpotifyTrackEnqueueError':
        return None
    audioAnalysis = data['data']['spotifyTrackEnqueue']['enqueuedSpotifyTrack']['audioAnalysisV6']
    if audioAnalysis['__typename'] == 'AudioAnalysisV6Finished':
        for tag in audioAnalysis['result']:
            if audioAnalysis['result'][tag] == None:
                return None
        return audioAnalysis['result']
    elif audioAnalysis['__typename'] == 'AudioAnalysisV6Failed':
        return None
    else:
        sleep(2)
        if rep < 15:
            return getSongInfo(id, rep + 1)
        return None



print(getAccessTokenCC())