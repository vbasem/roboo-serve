import time
import google.generativeai as genai
import pyttsx3  # Import Text-to-Speech library
from kaspersmicrobit import KaspersMicrobit

tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)  # Speed of speech (words per minute)
tts_engine.setProperty('volume', 1.0) # Volume level 0.0 to 1.0
finished = False
question = None

system_message = (
    "You are a robot in a museum that is answering kids questions. "
    "You are communicating with a human through a tiny micro:bit controller. "
    "Keep all answers very short, maximum one line. "
    "You only know that the museum has following 3 art pieces and you only know the following them: " \
    """
1. The Cloud-Slinging Cannon
This massive, bright-orange sculpture looks like a friendly robot’s toy. Instead of launching heavy things, it has a giant funnel at the back that "scoops up" invisible daydreams and shoots them out of a silver nozzle as fluffy, purple-tinted clouds. If you look closely at the "clouds" made of soft cotton, you might see the shapes of ice cream cones or dragons hidden inside.
2. The Whispering Forest Tapestry
This isn't a normal flat painting; it’s a huge wall hanging made of velvet, silk, and actual twigs. It shows a forest where the leaves are shaped like tiny ears. If you stand very still and put your ear near the fabric, the museum's hidden speakers play tiny whispers—the sounds of the trees sharing secrets about where they’ve hidden the forest’s magical golden acorns.
3. The Gravity-Free Breakfast Table
In this gravity-defying installation, a breakfast table is bolted to the ceiling! You can see a bowl of cereal where the milk and colorful loops are frozen in mid-air, floating upward like tiny balloons. The artist, a famous "trickster" named Sir Waffles-a-Lot, wanted to show what happens when the Earth forgets to pull things down for just five minutes.
"""
)

genai.configure(api_key='')
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    system_instruction=system_message # This sets the persona!
)
# Replace 'COM3' with your actual port (e.g., '/dev/tty.usbmodem...' on Mac/Linux)
# The baud rate for micro:bit is usually 115200
#ser = serial.Serial('COM6', 115200)

print("Listening for micro:bit input...")

def on_received_data(line):
    global question
    print(f"Received via Bluetooth: {line}")
   
    

        #if ser.in_waiting > 0:
            # Read a line from the micro:bit and decode it
            #line = ser.readline().decode('utf-8').strip()
            #print(f"Received from micro:bit: {line}")
            
            # You can now trigger PC actions based on the input
    question = ""
    if "butA" in line:
        question = "What color is The Cloud-Slinging Canon?"
        print("Detected butA")
    if "butB" in line:
        question ="The Gravity-Free Breakfast Table"
        print("Detected butB")                
    if "butA+B" in line:
        print("Detected butA+B")
    if "Crash!!!" in line:
        print("Detected Crashy")

    if line == "Button A":
        print("Action triggered for A!")


print("Searching for micro:bit via Bluetooth...")
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)  # Speed of speech (words per minute)
tts_engine.setProperty('volume', 1.0) # Volume level 0.0 to 1.0

voices = tts_engine.getProperty('voices')

# Print available voices
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name}")
    print(f"  - ID: {voice.id}")
    print(f"  - Languages: {voice.languages}")
    print()

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
            response = 'Du bist dumm'
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
# Keep the script alive until a button is pressed
    
        time.sleep(0.1)


#except KeyboardInterrupt:
    #ser.close()
    #print("Stopped.")
