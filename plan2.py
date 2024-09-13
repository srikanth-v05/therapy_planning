import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os
from trail1 import SPEECH_THERAPY_TEMPLATE
from googleapiclient.discovery import build  # YouTube API client
from langchain_google_genai import ChatGoogleGenerativeAI

# Set environment variable for API key
API_KEY1=st.secrets['API_KEY']

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY1)

# Initialize LLM with Google Generative AI
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, top_p=0.85)

# Function to search YouTube for videos
def search_youtube(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,  # Fetch only one video to match format
        q=query,
        type="video"
    )
    response = request.execute()
    # Extract video details
    videos = [{"title": item["snippet"]["title"], "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"} for item in response.get("items", [])]
    return videos

# Function to reset session states for a new chat
def new_chat():
    st.session_state.generated_plan = ""
    st.session_state.entity_memory = ConversationBufferMemory()

# Streamlit page configuration
st.set_page_config(page_title="Speech Therapy Plan Generator", layout="wide")

# Initialize session state for entity memory if not present
if 'entity_memory' not in st.session_state:
    st.session_state.entity_memory = ConversationBufferMemory()

if 'generated_plan' not in st.session_state:
    st.session_state.generated_plan = ""

# Sidebar for initiating a new chat
with st.sidebar:
    st.button("New Chat", on_click=new_chat)

# Main page title
st.title('Speech Therapy Plan Generator')

# Dropdown menu for selecting therapy type
therapy_options = [
    "Articulation Therapy",
    "Fluency Therapy",
    "Voice Therapy",
    "Language Therapy",
    "Cognitive Communication Therapy"
]
therapy_type = st.selectbox('Select the type of speech therapy needed:', therapy_options)

# Button to generate the therapy plan
if st.button('Generate Plan'):
    if therapy_type:
        # Create a ConversationChain with the prompt template and memory
        conversation_chain = ConversationChain(
            llm=llm,
            prompt=SPEECH_THERAPY_TEMPLATE,
            verbose=True,
            memory=st.session_state.entity_memory
        )
        
        # Run the conversation chain to generate a therapy plan
        response = conversation_chain.run(input=therapy_type)
        st.session_state.generated_plan = response
        
        # Display the generated speech therapy plan
        st.markdown("### Generated Speech Therapy Plan")
        st.markdown(f"Here is a 3-stage therapy plan for {therapy_type}:")

        # Extract and format stages, descriptions, and video details
        levels = response.split("Stage")  # Split response by stages
        for i, level in enumerate(levels[1:], 1):  # Skip the first empty split
            lines = level.splitlines()
            topic = f"Stage: {lines[0].strip()}"  # Extract stage topic

            # Extract details
            description = next((line for line in lines if "Description" in line), "Description: Not available").split(":", 1)[1].strip()
            search_query = next((line.split(":")[1].strip() for line in lines if "Suggested Search" in line), "")
            video_summary = next((line.split(":", 1)[1].strip() for line in lines if "Video Summary" in line), "")
            
            # Display stage information
            st.markdown(f"**{topic}**")
            st.write(f"- **Description**: {description}")

            # Search for and display the video link and summary only if available
            videos = search_youtube(search_query) if search_query else []
            if videos:
                video = videos[0]
                st.write(f"- **Video Link**: [{video['title']}]({video['url']})")
                if video_summary:
                    st.write(f"- **Summary of Video**: {video_summary}")
            st.markdown("---")  # Separator between levels

    else:
        st.error('Please select a type of speech therapy.')

# Display the generated plan if available
#if st.session_state.generated_plan:
#    st.markdown("### Generated Speech Therapy Plan")
#    st.write(st.session_state.generated_plan)
