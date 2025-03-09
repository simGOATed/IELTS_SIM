import sounddevice as sd
import numpy as np
import queue
from faster_whisper import WhisperModel, BatchedInferencePipeline
import pyttsx3
import soundfile as sf
import time
from textgen import TextGen


class InterviewHandler:
    def __init__(self):
        self.whisper_model = WhisperModel("small", device="cuda", compute_type="float32")
        self.batched_model = BatchedInferencePipeline(model=self.whisper_model)
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 170)
        self.audio_queue = queue.Queue()
        self.recognized_text = ""
        self.sections = ["Introduction", "Long Turn", "Two-Way Discussion"]
        self.current_section = ""
        self.questions = []
        self.question_index = 0
        self.answers = []
        self.stopped = False
        self.start = 0
        self.end = 0
        self.delta = 0
        self.time_limit = 120
        self.limit_reached = False
        self.chat_model = None
        self.eval_model = TextGen(mode='eval')
        self.next_ready = False

    def set_section(self, section):
        self.current_section = section
        if section == "Introduction":
            self.chat_model = TextGen(mode='chat_intro', time_limit = self.time_limit)
        elif section == "Long Turn":
            self.chat_model = TextGen(mode='chat_long_turn', time_limit = self.time_limit)
        elif section == "Two-Way Discussion":
            self.chat_model = TextGen(mode='chat_discussion', time_limit = self.time_limit)
        elif section == "Test":
            self.time_limit = 360
            self.chat_model = TextGen(mode = 'chat_test', time_limit = self.time_limit)

        self.question = self.chat_model.conversation('Hello')
        self.questions.append(self.question)

    def start_recording(self):
        self.stopped = False
        self.next_ready = False
        self.answers.append("")
        self.start_audio_stream()

    def start_audio_stream(self):
        def on_data(indata, frames, time, status):
            self.process_audio_data(indata)

        self.stream = sd.InputStream(callback=on_data, dtype=np.float32, samplerate=16000, blocksize=80000)
        self.stream.start()

    def process_audio_data(self, indata):
        self.save_audio_to_file(indata, filename="audio.wav")
        # print('transcribing...')

        try:
            # print(indata.shape)
            segments, _ = self.batched_model.transcribe("audio.wav", beam_size=5, language="en", batch_size=8, word_timestamps=True)
            for segment in segments:
                text = segment.text
                self.answers[self.question_index] += text
                # print(segment)
        except Exception as e:
            print(f"Error during transcription: {e}")
        # print('...stopped transcribing')
        self.handle_post_transcription()

    def handle_post_transcription(self):
        if self.stopped:
            self.stream.stop()
            self.question = self.chat_model.conversation(f'{self.answers[self.question_index]} '
                                                         f'[{round(self.delta, 2)} seconds have elapsed]')
            self.questions.append(self.question)
            self.next_ready = True

    def stop_recording(self):
        self.stopped = True
        self.end = time.time()
        self.delta += self.end - self.start
        if self.delta > self.time_limit:
            self.limit_reached = True

    def next_question(self):
        self.start = time.time()
        self.question_index += 1
        question = self.questions[self.question_index]
        self.tts_engine.say(question)
        self.tts_engine.runAndWait()

    def start_interview(self):
        self.start = time.time()
        self.tts_engine.say(self.question)
        self.tts_engine.runAndWait()

    def save_audio_to_file(self, audio_data, filename="output.wav"):
        sf.write(filename, audio_data, 16000)
        # print(f"Audio saved to file: {filename}")

    def format_questions_answers(self):
        result = ""
        for q, a in zip(self.questions, self.answers):
            result += f"q: {q} a: {a} "
        return result.strip()
