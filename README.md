# Rick - An AI Voice Assistant for Recording Musicians 

Operating Digital Audio Workstation (DAW) software can be difficult from behind a drumset or with a guitar strapped around your neck. Rick is your virtual assistant behind the computer. He listens for voice commands, and then takes actions in the DAW without you moving from your station. Just say "Hey Rick" and Rick will do his best to run your software for you. 

The project is written and Python and includes two modes: local LLM inference and API-based inference. So if you have a powerful machine and want to run Rick locally, he can work without internet connection. However, if you're running on a laptop, he can send the AI workloads to the cloud no problem. 

Right now Rick only works with Reaper on Windows machines and runs in a terminal, but soon he'll soon have a Graphical User Interface and work with any DAW and with Mac support as well. 

## Features

- **Hotword Detection**: Rick listens for the wake words "Hey Rick" to activate voice commands.
- **Speech-to-Text (STT)**: Converts your spoken words into text that Rick then maps to OSC commands that your DAW understands.
- **Text-to-Speech (TTS)**: Rick provides vocal feedback or responses so you can talk to him just like ChatGPT.
- **LLM Integration**: Uses large language models for natural language understanding, supporting both local inference and API-based inference.
- **UDP Communication**: Connects with DAW software via UDP, enabling seamless integration and control.
- **Modular Architecture**: Designed with flexibility in mind, making it easy to adapt to different DAWs or workflows.

## Requirements

- Python 3.8 or higher
- Windows OS (Mac support in development)
- Reaper DAW software (Further DAW support in development)
- Rick uses UDP port 55444 (a common OSC port). If you have other OSC devices like a MIDI controller, there may be some issues. Ensure that port 55444 is open. 
- For Local mode:
  - A CUDA based GPU able to run Mistral 7B Instruct
- For API mode:
  - Internet access
  - Huggingface account and key

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/adaley222/Rick.git
    cd Rick
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment for LLM inference (local or API-based):
    - For **local inference**, ensure you have the necessary models installed.
    - For **API-based inference**, configure your API keys and endpoints.

## Usage

Right now Rick runs in terminal mode. A UI is in development. For now, open any terminal and use the following bash code:

- For **local LLM inference**:
    ```bash
    python local_inference.py
    ```

- For **API-based inference**:
    ```bash
    python api_inference.py
    ```

Rick will listen for the wake words "Hey Rick" and respond with "Yo" when he's ready. Then, tell him what you'd like him to do. When you're finished, just give him any commands that sounds like "shut down" or "turn off" and he'll understand and close the application. 

## Current Development

- **Front-End Interface**: We are actively working on building a graphical user interface (GUI) for Rick to enhance user experience. Collaboration is welcome!
- **Further Action Support**: Right now Rick can only take a handful of actions. Once we've gotten that working smoothly, we can expand his vocabulary by adding new codes to the OSC code sheet.
- **Further DAW Support**: Right now Rick only works with Reaper. However, all DAWs use the same OSC protocol just with different action codes. By uploading different action code sheets and giving the user the ability to choose their DAW, Rick can easily work with any DAW.
- **Mac Support**: Right now Rick only works in Windows. We'll need to add Mac support. 
  
If you're interested in contributing to this project or have ideas for improvement, feel free to open an issue or submit a pull request.

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

Rick is open-source and available under the [MIT License](LICENSE).

---

Feel free to reach out or contribute!
