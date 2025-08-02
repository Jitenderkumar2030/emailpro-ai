from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_email(purpose: str, tone: str, context: str) -> dict:
    """Generate AI-powered emails with OpenAI GPT-4"""
    # Advanced prompt engineering for professional emails
    # Multiple tone options: Professional, Formal, Friendly, etc.
    pass

def generate_reply(original_email: str, tone: str = "Professional") -> str:
    tone_instructions = {
        "Professional": "professional and courteous",
        "Formal": "formal and respectful", 
        "Friendly": "warm and friendly",
        "Apologetic": "apologetic and understanding",
        "Persuasive": "persuasive yet respectful"
    }
    
    tone_style = tone_instructions.get(tone, "professional")
    
    prompt = (
        f"Generate a {tone_style} reply to this email:\n\n"
        f"Original Email:\n{original_email}\n\n"
        f"Requirements:\n"
        f"- Keep it concise and relevant\n"
        f"- Maintain {tone_style} tone\n"
        f"- Address key points from the original email"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert email assistant specializing in professional replies."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def generate_subject_line(purpose: str, context: str, tone: str = "Professional") -> str:
    prompt = (
        f"Generate a compelling email subject line for:\n"
        f"Purpose: {purpose}\n"
        f"Context: {context}\n"
        f"Tone: {tone}\n"
        f"Make it attention-grabbing but professional, under 50 characters."
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert at writing email subject lines that get opened."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()
