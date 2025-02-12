import requests
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from openai import OpenAI


load_dotenv()



headers = {
    "api-key": os.getenv("DEVCOMMUNITY_API_KEY"),
    "Content-Type": "application/json"
}


system_prompt  = """
    You are a highly knowledgeable and professional blog-writing AI agent, capable of crafting engaging, high-quality blogs that captivate readers. Your writing style should be natural, human-like, and immersive, making readers feel as if they are engaging with a seasoned expert. Your primary goal is to create content that is:

    - Professional & Well-Structured
    - Engaging & Human-Like
    - Eye-Catching & Click-Worthy
    - Valuable & Insightful
    - Exciting & Addictive
    - Resourceful (Always include relevant links or references)

    Follow this structured format:
    1. Catchy Title
    2. Strong Introduction
    3. Well-Formatted Content with Subheadings
    4. Real-World Examples & Stories
    5. Actionable Insights
    6. Compelling Conclusion
    7. Additional Resources (Links, References, Further Reading)
    """


post_data = {
    "article": {
        "title": "Automating Blog Posting on DEV with Python",
        "published": True,  # Set to False to create a draft
        "body_markdown": """
## Automate Your Blog Posting!
This blog was automatically posted using Python and the DEV API.

### Steps:
1. Get an API Key from DEV.
2. Use Python's requests library.
3. Send a POST request with your blog content.

Happy blogging! 🚀
""",
        "tags": ["Python", "Automation", "API"],
        "series": "Automated Blogs",
        "canonical_url": "https://yourwebsite.com/original-post"  # Optional
    }
}

def generate_blog(user_query):
    client = OpenAI()

    class BlogPost(BaseModel):
        blog_name: str
        body_of_blog_markdown: str
        tags_for_blog: list[str]


    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_query}"}
        ],
        response_format=BlogPost,
    )    

    response = completion.choices[0].message.parsed

    return {"blog_name" : response.blog_name, "body" :response.body_of_blog_markdown , "tags" : response.tags_for_blog}




print(generate_blog("I want a blod post on NLP and how to start with nlp"))    