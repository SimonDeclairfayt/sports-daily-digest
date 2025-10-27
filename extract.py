from datetime import date, timedelta
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from mailjet_rest import Client
import os
load_dotenv()
api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
# On récupère la date pour le prompt
today = date.today()
yesterday = today - timedelta(days=1)
serpAiKey = os.getenv('SERPAI_KEY')
SITES_CIBLES = ["walfoot.be", "lequipe.fr/Football"]
MOTS_CLES = ["jupiler pro league","classement"]
def getFootballInfo():
    """
    Synchronous version - simpler to understand and use
    """
    # Create the client
    all_articles = []
    seen_urls = set() # Trying to avoid doubles
    # We look through the sites to see 
    for site in SITES_CIBLES:
        # Requête SerpAPI avec filtres temporels et site-specific
        params = {
            "q": f'site:{site} {MOTS_CLES}',
            "api_key": serpAiKey,
            "engine": "google",
            "tbm": "nws",  # Onglet "Actualités" de Google
            "tbs":f"qdr:d",  # 24 dernières heures
            "num": 3,  # On en récupère plus pour filtrer après
            "hl": "fr"  # Résultats en français
        }
        search = GoogleSearch(params)
        results = search.get_dict()
    # Send the prompt to Gemini
        if "news_results" in results and results["news_results"]:
                for article in results["news_results"]:
                    url = article.get("link", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_articles.append({
                            "title": article.get("title", ""),
                            "link": url,
                            "source": article.get("source", ""),
                            "date": article.get("date", ""),
                            "snippet": article.get("snippet", ""),
                            "thumbnail":article.get("thumbnail","")
                        })
    if all_articles:
        print(f"Found {len(all_articles)} articles")
        print(all_articles[0])  # Print first article for debugging
        template_id = int(os.getenv('MAILJET_TEMPLATE_ID'))
        
        # Prepare email data for Mailjet
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": os.getenv("SENDER_EMAIL"),
                        "Name": "Ton amoureux"
                    },
                    "To": [
                        {
                            "Email": os.getenv('RECEIVER_EMAIL'),
                            "Name": os.getenv('RECEIVER_NAME')
                        }
                    ],
                    "Subject": f"Nouvelles news de football - {today.strftime('%d/%m/%Y')}",
                    "TemplateID": template_id,
                    "TemplateLanguage": True,
                    "TemplateErrorReporting":{
                        "Email":os.getenv("SENDER_EMAIL"),
                        "Name":"Simon"
                    },
                    "Variables": {
                        "Articles": all_articles,
                        "Date": today.strftime('%d/%m/%Y'),
                        "ArticleCount": len(all_articles)
                    }
                }
            ]
        }
        
        # Send the email
        result = mailjet.send.create(data=data)
            
        if result.status_code == 200:
            print("Email sent successfully!")
            response_json = result.json()
            print(f"Response JSON: {response_json}")
        else:
            print(f"Failed to send email. Status code: {result.status_code}")
        
    else:
        print("Aucun article trouvé pour la période spécifiée.")
    
    # Close the client
    return all_articles

  
# Run the synchronous function
if __name__ == "__main__":
    getFootballInfo()

# Problème la maintenant sur la façon de faire : 
    # Récupère beaucoup trop de lien car fait trop de recherche
    # Et si j'essayais juste de récupèrer 5 liens par site.
    # Quels mots-clés utilisé ?