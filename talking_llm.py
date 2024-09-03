import os
from dotenv import load_dotenv, find_dotenv
import numpy as np
import openai
from pynput import keyboard
import sounddevice as sd
import wave

load_dotenv(find_dotenv())

client = openai.Client()


class TalkingLLM:
    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.samplerate = 44100
        self.channels = 1
        self.dtype = "int16"

    def start_or_stop_rec(self):
        if self.is_recording:
            self.is_recording = False
            self.save_and_transcribe()
            self.audio_data = []
        else:
            print("Starting record")
            self.audio_data = []
            self.is_recording = True

    def create_agent(self):
        pass

    def save_and_transcribe(self):
        print("Saving the recording...")
        if "temp.wav" in os.listdir():
            os.remove("temp.wav")
        wav_file = wave.open("test.wav", "wb")
        wav_file.setnchannels(self.channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(self.samplerate)
        wav_file.writeframes(np.array(self.audio_data, dtype=self.dtype))
        wav_file.close()

    def covert_and_play(self):
        pass

    def run(self):

        def callback(indata, frame_count, time_info, status):
            if self.is_recording:
                self.audio_data.extend(indata.copy())

        with sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            callback=callback,
        ):
            pass

        def on_activate():
            self.start_or_stop_rec()

        def for_canonical(f):
            return lambda k: f(l.canonical(k))

        hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+<alt>+h"), on_activate)
        with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release),
        ) as l:
            l.join()


if __name__ == "__main__":
    talking_llm = TalkingLLM()
    talking_llm.run()
