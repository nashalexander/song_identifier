import sys
import os
import asyncio
from shazamio import Shazam, Serialize

song = sys.argv[1]

async def identify(song):
    shazam = Shazam()
    out = await shazam.recognize_song(song)
    return out

    serialized = Serialize.full_track(out)
    print(serialized)
    print(serialized.track.title, serialized.track.subtitle)

def rename_file(file, new_name):
    os.rename(file, new_name)

asyncio.run(identify(song))

# loop = asyncio.get_event_loop_policy().get_event_loop()
# loop.run_until_complete(identify(song))

shazam = Shazam()
coroutine = shazam.recognize_song(song)
out = asyncio.run(coroutine)

serialized = Serialize.full_track(out)
print(serialized)
# if title and subtitle do not exist, print song with error message
if serialized.track.title is None:
    print("Song ", song, " not found")
else:
    print("title: ", serialized.track.title, "subtitle: ", serialized.track.subtitle)
