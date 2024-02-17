import sys
import os
import asyncio
from shazamio import Shazam, Serialize

async def identify(song_file):
    title = ""
    subtitle = ""
    song_file_extension = os.path.splitext(song_file)[1]

    shazam = Shazam()
    out = await shazam.recognize_song(song_file)
    serialized = Serialize.full_track(out)

    if serialized.track.title is None:
        print("Song name of ", song_file, " not found")
    else:
        title = serialized.track.title

    if serialized.track.subtitle is None:
        print("Song artist of ", song_file, " not found")
    else:
        subtitle = serialized.track.subtitle
    
    return title + " - " + subtitle + song_file_extension

async def identifier_coroutine(queue, data, start_index, stride):
    for i in range(start_index, len(data), stride):
        item = data[i]
        song_title = await identify(item)
        await queue.put([item, song_title])

async def renamer_coroutine(queue):
    while True:
        result = await queue.get()
        print(f"renaming {result[0]} to {result[1]}")

        # Notify the queue that the item has been processed
        queue.task_done()

async def process(file_list, num_coroutines):
    song_name_queue = asyncio.Queue()

    # Create producer tasks, each with a different start index and the same stride
    identifiers = [
        asyncio.create_task(identifier_coroutine(song_name_queue, file_list, i, num_coroutines))
        for i in range(num_coroutines)
    ]

    renamer = asyncio.create_task(renamer_coroutine(song_name_queue))

    # Wait for all songs to be identified
    await asyncio.gather(*identifiers)

    # Wait until the queue is fully processed
    await song_name_queue.join()

    # Cancel the consumer task as it's intentionally an infinite loop
    renamer.cancel()


if __name__ == "__main__":
    # Get the list of audio files from the command line
    files = sys.argv[1:]

    # TODO: verify supported audio files by shazamio
    audioFileExtensions = [".mp3", ".wav", ".flac", ".m4a", ".ogg", ".opus"]
    # Check that all files are audio files
    for file in files:
        file_extension = os.path.splitext(file)[1]
        if file_extension not in audioFileExtensions:
            print("Error: ", file, " is not an audio file.")

    num_coroutines = 10
    asyncio.run(process(files, num_coroutines))

def rename_file(file, new_name):
    os.rename(file, new_name)
