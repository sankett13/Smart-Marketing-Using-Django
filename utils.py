import requests
from django.conf import settings
import django, os

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Smart_Marketing.settings")
django.setup()

def get_groq_news(prompt):
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",  
        "Content-Type": "application/json"  
    }

    data = {
        "model": "mixtral-8x7b-32768",  
        "messages": [{"role": "user", "content": prompt}]
    }

    
    response = requests.post(settings.GROQ_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        json_response = response.json()
        message_content = json_response.get("choices", [{}])[0].get("message", {}).get("content", "No content found")
        # print(message_content)
        return message_content
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return f"Error: {response.status_code}, Details: {response.text}"


# prompt = """Find the latest food trends in Gujarat, India, for the current winter season. The response should be structured in news-style bullet points and cover the following aspects:

# - **Trending Seasonal Dishes** – Popular Gujarati winter foods gaining traction.
# - **New Food Industry Trends** – Any new restaurant concepts, fusion foods, or health-focused winter diets emerging in Gujarat.
# - **Street Food Innovations** – Any trending street food or winter-special snacks unique to Gujarat.
# - **Beverage Trends** – Popular winter drinks, including herbal teas or immunity-boosting beverages.
# - **Health & Wellness Trends** – Any superfoods, organic, or plant-based trends popular in Gujarat this winter.
# - **Restaurant & Café Trends** – Any unique offerings, limited-time winter menus, or special dining experiences introduced this season.
# - **Food Industry Updates** – New food startups, restaurant launches, or winter-themed food festivals happening in Gujarat.

# The response should be concise, factual, and up-to-date, ensuring all insights are specific to Gujarat and the winter season."""

# get_groq_news(prompt)
