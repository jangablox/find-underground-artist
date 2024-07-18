import requests
import json
import base64

GET_ARTIST_URL ='https://api.spotify.com/v1/artists/7Hjbimq43OgxaBRpFXic4x'
#bytes(base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET),'ascii')


CLIENT_ID = '31ddcbfca5754986b1cf2214323552b4'
CLIENT_SECRET = '27b14e5157d34b8abe13518b0a45e8cc'
clientCred = f'{CLIENT_ID}:{CLIENT_SECRET}'
b64ClientCred = base64.b64encode(clientCred.encode())

getToken = requests.post(
    'https://accounts.spotify.com/api/token',
    headers={
        'Authorization': f'Basic {b64ClientCred.decode()}' ,
        'Content-Type': 'application/x-www-form-urlencoded'	
    },
    data={
        'grant_type':'client_credentials'
    }


)



getToken = getToken.json()
TOKEN = getToken['access_token']
responses = requests.get(
    GET_ARTIST_URL,
    headers={
        "Authorization": f"Bearer {TOKEN}"
    }
)

responses = responses.json()

topTracks = requests.get(
    url=f'https://api.spotify.com/v1/artists/{responses["id"]}/top-tracks?market=ES',
    headers={
         "Authorization": f"Bearer {TOKEN}"
    }
)

topTracks = topTracks.json()

trackID = []
for track in topTracks["tracks"]:
    trackID.append(track["id"])


cyaniteSecret = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiSW50ZWdyYXRpb25BY2Nlc3NUb2tlbiIsInZlcnNpb24iOiIxLjAiLCJpbnRlZ3JhdGlvbklkIjo2MTUsInVzZXJJZCI6NDgxNjEsImFjY2Vzc1Rva2VuU2VjcmV0IjoiMzFjNzdjMWVkM2Q5MDRiYmM4MzA1MmEzODEzN2ExODFhNjU2NDhhNmNlNGI0MTFhN2EzZjhkODQwZGUyYWI2YSIsImlhdCI6MTY4ODkxNTMyNX0.NcNanIt8Z5LXOjK2izOfhbaVWH5m1YBJC4stIXIfdTc'
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
test = requests.post(
    url='https://api.cyanite.ai/graphql',
    headers={
        "Content-Type" : "application/json",
        "Authorization": f"Bearer {cyaniteSecret}"
    },
    json={"query": cyaniteBody,
          "variables": '{ "input": { "spotifyTrackId": "2Lmpxi7j95HOvsR6zj1Fl3" } }'
          }
)


test = json.loads(test.content)
arousal = test['data']['spotifyTrackEnqueue']['enqueuedSpotifyTrack']['audioAnalysisV6']['result']['arousal']
print(arousal)

