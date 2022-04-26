#ffmpeg
Converting Audio into Different Formats / Sample Rates:

Convert any MP3 file to WAV 16khz mono 16bit:
ffmpeg -i 111.mp3 -acodec pcm_s16le -ac 1 -ar 16000 out.wav

Extract audio:-
ffmpeg -i video.mp4 -f mp3 -ab 192000 -vn music.mp3

The -i option in the above command is simple: it is the path to the input file. The second option -f mp3 tells ffmpeg that the ouput is in mp3 format. The third option i.e -ab 192000 tells ffmpeg that we want the output to be encoded at 192Kbps and -vn tells ffmpeg that we dont want video. The last param is the name of the output file.

You say you want to "extract audio from them (mp3 or ogg)". But what if the audio in the mp4 file is not one of those? you'd have to transcode anyway. So why not leave the audio format detection up to ffmpeg?

To convert one file:

ffmpeg -i videofile.mp4 -vn -acodec libvorbis audiofile.ogg

Pulse-code modulation (PCM) is a method used to digitally represent sampled analog signals. It is the standard form of digital audio in computers, compact discs, digital telephony and other digital audio applications.

Generate audio frames from PCM audio files:-
An audio frame, or sample, contains amplitude (loudness) information at that particular point in time. To produce sound, tens of thousands of frames are played in sequence to produce frequencies.

In the case of CD quality audio or uncompressed wave audio, there are around 44,100 frames/samples per second. Each of those frames contains 16-bits of resolution, allowing for fairly precise representations of the sound levels. Also, because CD audio is stereo, there is actually twice as much information, 16-bits for the left channel, 16-bits for the right.

When you use the sound module in python to get a frame, it will be returned as a series of hexadecimal characters:

One character for an 8-bit mono signal.
Two characters for 8-bit stereo.
Two characters for 16-bit mono.
Four characters for 16-bit stereo.
In order to convert and compare these values you'll have to first use the python wave module's functions to check the bit depth and number of channels. Otherwise, you'll be comparing mismatched quality settings.

Understanding how digital audio works:
there are two numbers that are associated with a wav file one of which is called bit depth and the other thing is called the sample frequency.
So these are the two paramters used to convert an analog signal to digital signal.

Sample frequency :-
the number of slices per second is the sample frequency ,the more slices you stab the better the audio quality.

The yield statement suspends function’s execution and sends a value back to the caller, but retains enough state to enable function to resume where it is left off. When resumed, the function continues execution immediately after the last yield run. This allows its code to produce a series of values over time, rather than computing them at once and sending them back like a list.

VAD file :-https://git.speed.pub.ro/diploma/multimodal-person-identification/-/blob/d9430dc0dc35bb3b8040142e74913226758994c7/audio_processing/example.py

Voiced sounds are ones where you can feel a vibration.

On the other hand, unvoiced sounds do not make a vibration in your vocal chords.

SRT file manipulation :-
https://pypi.org/project/srt/
