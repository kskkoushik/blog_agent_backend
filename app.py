import requests
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)



load_dotenv()






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

def get_trending_ai_topics():
    url = "https://api.tavily.com/search"
    params = {
        "query": "Trending AI Topics",
        "num_results": 5,  # Adjust the number of results as needed
        "api_key": os.getenv("TAVILTY_API_KEY")
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        topics = [result["title"] for result in data.get("results", [])]
        return topics
    else:
        print("Error:", response.status_code, response.text)
        return []



@app.route('/api/generate-custom', methods=['POST'])
def generate_custom_blog():

        headers = {
          "api-key": os.getenv("DEVCOMMUNITY_API_KEY"),
          "Content-Type": "application/json"
        }
        data = request.json
        topic = data.get('topic')
        tone = data.get('tone', 'professional')
        length = data.get('length', 'medium')

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        user_query = f"I know your are an expert blog wriritng AI agent , {topic} ,  make sure your blog contains high quality content and Its size is {length}"

        data = generate_blog(user_query)

        dev_community_data = {"aricles": {"title": data["blog_name"] , "published": True , "body_markdown": data["body"] , "tags": data["tags"] , "series" : "Automated Blogs" , "canonical_url": "https://www.linkedin.com/in/kskkoushik135/"}}
        
        response = requests.post(os.getenv("API_URL"), headers=headers, json=dev_community_data)

        
        url = response.json().get("url")
        return jsonify({
            "url": url
        })

    



@app.route('/api/generate-trending', methods=['POST'])
def generate_trending_blog():
    try:
        # In a real app, you would generate content based on trends
        # For now, we'll just generate a unique UR
        # Fetch trending AI topics
        trending_topics = get_trending_ai_topics()
        
        user_query = f'''I know your are an expert blog wriritng AI agent , {trending_topics[0]} ,  make sure your blog contains high quality content , if you dont have enough info about the topic make blog post related useful topics related to AI and also provide implementations in python to how to do it , if its possible . Make sure your bloga are professional and should excite users to read the entire blog. '''

        data = generate_blog(user_query)

        dev_community_data = {"aricles": {"title": data["blog_name"] , "published": True , "body_markdown": data["body"] , "tags": data["tags"] , "series" : "Automated Blogs" , "canonical_url": "https://www.linkedin.com/in/kskkoushik135/"}}
        

        headers = {
          "api-key": os.getenv("DEVCOMMUNITY_API_KEY"),
          "Content-Type": "application/json"
        }

        response = requests.post(os.getenv("API_URL"), headers=headers, json=dev_community_data)

        
        url = response.json().get("url")
        return jsonify({
            "url": url
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
