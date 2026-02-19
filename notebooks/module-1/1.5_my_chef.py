from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langchain_core.tools import tool
from tavily import TavilyClient
from typing import Dict, Any
####### image imports
from ipywidgets import FileUpload
from IPython.display import display
import base64
####### Audio input
import sounddevice as sd
from scipy.io.wavfile import write
import base64
import io
import time
from tqdm import tqdm

load_dotenv()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""

    return tavily_client.search(query)


MODEL_NAME = "gemini-2.5-flash-lite"

tavily_client = TavilyClient()

model = init_chat_model(model=MODEL_NAME, model_provider="google_genai")

config = {"configurable": {"thread_id": "1"}}

agent = create_agent(model=model,
                     checkpointer=InMemorySaver(),
                     tools=[web_search])

### ask user to upload his fridge image
uploader = FileUpload(accept='.png', multiple=False)
display(uploader)

# Get the first (and only) uploaded file dict
uploaded_file = uploader.value[0]

# This is a memoryview
content_mv = uploaded_file["content"]

# Convert memoryview -> bytes
img_bytes = bytes(content_mv)  # or content_mv.tobytes()

# Now base64 encode
img_b64 = base64.b64encode(img_bytes).decode("utf-8")

multimodal_question = HumanMessage(content=[
    {"type": "text", "text": "Tell me about the image"},
    {"type": "image", "base64": img_b64, "mime_type": "image/png"}
])

### record the user's audio
# Recording settings
duration = 5  # seconds
sample_rate = 44100

print("Recording...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
# Progress bar for the duration
for _ in tqdm(range(duration * 10)):   # update 10× per second
    time.sleep(0.1)
sd.wait()
print("Done.")

# Write WAV to an in-memory buffer
buf = io.BytesIO()
write(buf, sample_rate, audio)
wav_bytes = buf.getvalue()

aud_b64 = base64.b64encode(wav_bytes).decode("utf-8")

multimodal_question = HumanMessage(content=[
    {"type": "text", "text": "Write the transcript of the user's voice"},
    {"type": "audio", "base64": aud_b64, "mime_type": "audio/wav"}
])

response = agent.invoke(
    {"messages": [multimodal_question][-1].content}
)