import pyaudio
import wave
import numpy as np
import time

class VoiceRecorder:
    """
    A class to record voice and stop when silence is detected for a specified duration.
    The class is auto-iterable to create sequential filenames like 'voice1.wav', 'voice2.wav', etc.
    """

    def __init__(self, silence_threshold=1000, silence_duration=2, 
                 format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        """
        Initializes the VoiceRecorder object with the specified parameters.

        Args:
            silence_threshold (int): Threshold for detecting silence.
            silence_duration (int): Duration in seconds for silence before stopping.
            format (int): Audio format for recording (default is pyaudio.paInt16).
            channels (int): Number of audio channels (default is 1 for mono).
            rate (int): Sample rate (default is 44100 samples per second).
            chunk (int): Size of each audio chunk (default is 1024).
        """
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.silence_start_time = None
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recording_count = 1  # To auto-generate filenames

    def start_recording(self):
        """
        Starts the recording process and saves it to a file with an auto-incremented name.
        """
        # Set the filename based on the current recording count
        output_filename = f"voice{self.recording_count}.wav"
        
        # Start the recording process
        self.frames = []  # Clear previous frames
        self.silence_start_time = None  # Reset silence timer

        print(f"Recording to {output_filename}...")

        # Start the audio stream
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        while True:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

            if self._is_silent(data):
                if self.silence_start_time is None:
                    self.silence_start_time = time.time()  # Start the silence timer
                elif time.time() - self.silence_start_time > self.silence_duration:
                    print("Silence detected. Stopping...")
                    break
            else:
                self.silence_start_time = None  # Reset the silence timer if sound is detected

        # Stop the stream and close it
        self.stream.stop_stream()
        self.stream.close()

        # Save the recorded audio to a .wav file
        self._save_audio(output_filename)

        # Increment the recording count for the next file
        self.recording_count += 1

        # Return the filename for the current recording
        return output_filename

    def _is_silent(self, data):
        """
        Checks if the audio data is silent based on the set threshold.

        Args:
            data (bytes): Raw audio data.

        Returns:
            bool: True if the audio is silent, False otherwise.
        """
        audio_data = np.frombuffer(data, dtype=np.int16)
        return np.max(np.abs(audio_data)) < self.silence_threshold

    def _save_audio(self, output_filename):
        """
        Saves the recorded audio frames to a .wav file.

        Args:
            output_filename (str): The name of the output audio file.
        """
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f"Audio saved as {output_filename}")


# Initialize the recorder instance
recorder = VoiceRecorder(silence_threshold=1000, silence_duration=2)
