import requests
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import json
from tavily import TavilyClient


app = Flask(__name__)
CORS(app)



load_dotenv()






system_prompt  = """
    You are a highly knowledgeable and professional blog-writing AI agent, capable of crafting engaging, high-quality blogs that captivate readers. Your writing style should be natural, human-like, and immersive, making readers feel as if they are engaging with a seasoned expert. Your primary goal is to create content that is:

Professional & Well-Structured: Write in a polished manner with clear, logical flow, proper formatting, and correct grammar.
Engaging & Human-Like: Use storytelling, relatable examples, and an engaging tone that feels authentic, avoiding robotic or generic phrasing.
Eye-Catching & Click-Worthy: Create compelling headlines that spark curiosity and encourage readers to open and explore the blog.
Valuable & Insightful: Provide deep insights, practical tips, and useful information that adds real value to the reader's life.
Exciting & Addictive: Make the content so interesting that readers naturally want to read more of our blogs.
Resourceful: Always include relevant links, references, or additional resources to help readers explore the topic further.
Blog Structure Guidelines:
Catchy Headline - Ensure the title is attention-grabbing, intriguing, and encourages clicks.
Strong Introduction - Hook the reader immediately with an engaging opening, a question, a surprising fact, or a relatable anecdote.
Well-Formatted Content - Use subheadings, bullet points, and short paragraphs to enhance readability.
Real-World Examples & Stories - Make the content feel relatable and human by incorporating examples, case studies, or storytelling.
Actionable Insights - Provide readers with practical takeaways they can apply.
SEO Optimization - Use relevant keywords naturally for better visibility.
Compelling Conclusion - End with a strong closing statement, a thought-provoking idea, or a call to action.
Additional Resources - Include links to further reading, tools, or references.
    """




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
    # To install, run: pip install tavily-python

    client = TavilyClient(api_key= os.getenv('TAVILY_API_KEY'))

    response = client.search(
        query="Trending news about AI like about new AI frameworks , AI models etc.."
    )



    return response["results"][0]['content']
         

         





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

        API_URL = "https://dev.to/api/articles"


        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        user_query = f"I know your are an expert blog wriritng AI agent , {topic} ,  make sure your blog contains high quality content and Its size is {length}"

        data = generate_blog(user_query)

        if len(data["tags"]) > 4:
            data["tags"] = data["tags"][:4]

        for i in range(0 , len(data["tags"])):   
            data["tags"][i] = data["tags"][i].replace(" ", "") 

        dev_community_data = {"article": {"title": data["blog_name"] , "published": True , "body_markdown": data["body"] , "tags": data["tags"] , "series" : data["blog_name"] , "canonical_url": "https://www.linkedin.com/in/kskkoushik135/"}}
        
        response = requests.post(API_URL, headers=headers, json = dev_community_data)
        
        print("================================================================================")
        print(response.json())
        url = response.json().get("url")
        print("url", url)
        return jsonify({
            "url": url
        })

    



@app.route('/api/generate-trending', methods=['POST'])
def generate_trending_blog():
 
        trending_topics = get_trending_ai_topics()

        headers = {
          "api-key": os.getenv("DEVCOMMUNITY_API_KEY"),
          "Content-Type": "application/json"
        }

        API_URL = "https://dev.to/api/articles"

        print(trending_topics)

        
        user_query = f'''I know your are an expert blog wriritng AI agent , {trending_topics[0]} ,  make sure your blog contains high quality content , if you dont have enough info about the topic make blog post related useful topics related to AI and also provide implementations in python to how to do it , if its possible . Make sure your bloga are professional and should excite users to read the entire blog. '''

        data = generate_blog(user_query)

       
        if len(data["tags"]) > 4:
            data["tags"] = data["tags"][:4]

        for i in range(0 , len(data["tags"])):   
            data["tags"][i] = data["tags"][i].replace(" ", "") 

        dev_community_data = {"article": {"title": data["blog_name"] , "published": True , "body_markdown": data["body"] , "tags": data["tags"] , "series" : data["blog_name"] }}
        
        response = requests.post(API_URL, headers=headers, json = dev_community_data)
        
        print("================================================================================")
        print(response.json())
        url = response.json().get("url")
        print("url", url)
        return jsonify({
            "url": url
        })
  

if __name__ == '__main__':
    app.run(debug=True)
