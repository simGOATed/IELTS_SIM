# IELTS Speaking Test Simulator App

## Overview

Welcome to the IELTS Speaking Test Simulator App! This application is designed to help users practice and prepare for the IELTS speaking test by simulating real test scenarios. The app includes three sections of the IELTS speaking test: Introduction, Long Turn, and Two-Way Discussion. Additionally, users can receive feedback on their performance for each section and a comprehensive summary at the end.

## Features

- **Practice Mode**: Allows users to practice each section individually.
- **Test Mode**: Simulates the entire IELTS speaking test with feedback provided for each section and a final summary.
- **Real-time Transcription**: Uses AI transcription models to convert spoken responses into text.
- **Feedback Generation**: Provides detailed AI-Generated feedback on performance based on IELTS criteria.

## Known Bugs

- Variables do not reset, meaning the app needs to be closed after each session.
- Sometimes the AI will ask questions even after the session has ended.
- The pdf file produced does not have text wrapping.

## Challenges

- I'd never really worked with CUDA so it took 4 hours to get it working with faster-whisper.
- My CPU took too long to transcribe
- Many bugs only showed up during the demo

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ielts-speaking-test-simulator.git
    cd ielts-speaking-test-simulator
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```
  Or, run the executable:
    ```sh
    dist/main
    ```
2. **Start Screen**: Click "Start" to enter the main menu.

3. **Main Menu**:
    - **Practice Mode**: Select "Practice Mode" to practice individual sections (Introduction, Long Turn, Two-Way Discussion).
    - **Test Mode**: Select "Test Mode" to simulate the entire test. Follow the prompts to navigate through each section.

4. **During the Test**:
    - Use the "Start" button to begin recording your response.
    - Use the "Stop" button to stop recording and wait for the transcription to complete.
    - Use the "Next" button to proceed to the next question or section.

5. **Feedback**:
    - After each section, you will receive detailed feedback based on your responses.
    - At the end of the test, you will receive a comprehensive summary of your performance across all sections.

## Requirements

- Python 3.7+ or higher
- Tkinter
- Sounddevice
- Numpy
- Faster Whisper
- Pyttsx3
- Soundfile
- Google Generative AI

