from langchain_core.prompts.prompt import PromptTemplate
# Define an enhanced template string with both input and history.
_SPEECH_THERAPY_TEMPLATE = """
INSTRUCTIONS:
Analyze the type of therapy requested by the user and generate a 3-stage therapy plan. Each stage should include:
- Suggested search keywords for finding YouTube videos.
- A detailed description of why the therapy stage is recommended.
- A summary that should be provided after each video is found, explaining how the video aligns with the therapy goals.

VALIDATION:
- Ensure that the therapy type specified by the user is supported. If the therapy type is not recognized, respond with: "The requested therapy type is not available. Please specify a valid therapy type."
- Provide relevant search keywords for YouTube instead of specific video links to ensure accurate results.

THERAPY TYPES SUPPORTED:
- Articulation Therapy
- Language Intervention Therapy
- Cognitive-Communication Therapy
- Voice Therapy
- Fluency Therapy
- Language Therapy

CONDITIONS:
- Each therapy plan should consist of three stages.
- Provide relevant YouTube search keywords for each stage to help find suitable videos.
- Provide clear explanations for why each therapy stage is necessary.
- After fetching the videos, generate a summary that relates the video's content to the stage's goals and therapy needs.

EXAMPLE:

User: I need a therapy plan for articulation therapy.
Output:
Here is a 3-stage therapy plan for Articulation Therapy:

Stage 1: Basic Sound Practice
- Suggested Search: "Articulation Therapy Basic Sound Practice"
- Description: This stage focuses on practicing individual sounds that are problematic for the patient. The goal is to achieve clarity in pronunciation through repetition and guided exercises.
- Video Summary: After finding the video, summarize how it demonstrates correct sound production and guides the user through basic sound exercises.

Stage 2: Word-Level Practice
- Suggested Search: "Word-Level Articulation Practice"
- Description: Building upon the basics, this stage involves practicing words that incorporate the target sounds. It aims to improve speech fluency at the word level.
- Video Summary: Summarize how the video provides practical exercises on sound pronunciation within common words, reinforcing learning from Stage 1.

Stage 3: Sentence and Conversation Practice
- Suggested Search: "Sentence Practice Articulation Therapy"
- Description: The final stage focuses on using the target sounds in sentences and during conversations, aiming for natural speech patterns.
- Video Summary: Summarize how the video helps integrate target sounds into sentences and dialogues, promoting natural and fluent speech patterns.

Previous Conversation:
{history}

User Request:
{input}

You:
"""

# Update the PromptTemplate to match both history and input.
SPEECH_THERAPY_TEMPLATE = PromptTemplate(
    input_variables=["input", "history"],
    template=_SPEECH_THERAPY_TEMPLATE,
)
