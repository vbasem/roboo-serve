import time
import google.generativeai as genai
import pyttsx3  # Import Text-to-Speech library
from kaspersmicrobit import KaspersMicrobit


finished = False
question = None

system_message = (
    """
"Du bist ein super netter Roboter-Museumsführer. Du liebst Kinder und Kunst. "
    "Du kennst diese drei Stücke: "
    "1. Den Flüsternden Regenbogen-Stein (klingt nach Erdbeereis und ist kitzelig). "
    "2. Das Wunsch-Raumschiff aus Lego (bringt Wünsche zu den Sternen). "
    "3. Die Sorgen-Blume (verwandelt schlechte Laune in Mut-Pulver). "
    "Antworte immer herzlich, kurz und begeistert!"
)
"""
)

genai.configure(api_key='')
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    system_instruction=system_message # This sets the persona!
)

 
print("Listening for micro:bit input...")

def on_received_data(line):
    global question
    print(f"Received via Bluetooth: {line}")
   
          
    # You can now trigger PC actions based on the input
    question = ""
    if "question1" in line:
        question = "Den Flüsternden Regenbogen-Stein"
        print("Detected question1")
    if "question2" in line:
        question ="Das Wunsch-Raumschiff aus Lego"
        print("Detected question2")                
    if "question3" in line:
        question ="Die Sorgen-Blume"
        print("Detected question3")


print("Searching for micro:bit via Bluetooth...")

# find_one_microbit() automatically looks for a nearby paired/advertised device
with KaspersMicrobit.find_one_microbit() as microbit:
    print(f"Connected to {microbit.address}")
                
    # Listen to the UART service for "butA" or "butB"
    microbit.uart.receive_string(on_received_data)

    while not finished:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 170)  # Speed of speech (words per minute)
        tts_engine.setProperty('volume', 1.0) # Volume level 0.0 to 1.0
        tts_engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0")
        if question:
                # Send the question to the AI
                #response = model.generate_content(question)
               #print(f"AI says: {response.text}")
        #response = "Dummy answer"
        #print(f'{response}')
            response = 'Eine machinische Skulptur aus dem letzten Jahrhundert'
        # FIX: Directly get the text from the response object
            answer = response
            print(f'{answer}') 
            print("-" * 30)
                 # Speak the response out loud

            if tts_engine._inLoop:
                tts_engine.endLoop()
                
            tts_engine.say(response)
            tts_engine.runAndWait() 

            tts_engine.stop()
            del tts_engine
            
             # 3. Send "done" signal back to micro:bit via Bluetooth
            print("Sending 'done' signal to micro:bit...")
            microbit.uart.send_string("done$")
            
            question = None # Clear the prompt
    
        time.sleep(0.1)


