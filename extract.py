from datetime import date, timedelta
from google import genai
from google.genai import types
from serpapi.google_search import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

# On récupère la date pour le prompt
today = date.today()
yesterday = today - timedelta(days=1)
serpAiKey = os.getenv('SERPAI_KEY')
SITES_CIBLES = ["walfoot.be", "lequipe.fr/Football"]
MOTS_CLES = "match"
def getFootballInfo():
    """
    Synchronous version - simpler to understand and use
    """
    # Create the client
    client = genai.Client(api_key=os.getenv('GEMINI_KEY'))
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
            "num": 5,  # On en récupère plus pour filtrer après
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
                        })
    if all_articles:
        print(all_articles[0])
        # Format articles for the prompt
        articles_text = "\n\n".join([
            f"Title: {a['title']}\nSource: {a['source']}\nDate: {a['date']}\nSnippet: {a['snippet']}\nLink: {a['link']}"
            for a in all_articles[:15]  # Limit to top 15 to avoid token limits
        ])
        
        prompt = f"""Voici les dernières actualités sportives du football entre {yesterday} et {today}:

            {articles_text}

            Peux-tu créer un résumé concis des informations les plus importantes dans ces articles?
            Organise le résumé par catégories:
            1. Résultats de matchs importants
            2. Blessures et suspensions de joueurs
            3. Transferts et rumeurs
            4. Autres actualités notables

            Écris le résumé en français en 400-500 mots maximum.
            """
        
        
        
        print("\n===== RÉSUMÉ DES ACTUALITÉS FOOTBALL =====\n")
        
    else:
        print("Aucun article trouvé pour la période spécifiée.")
    
    # Close the client
    return all_articles
    
    
    # Print the response
    
    # Close the client

  
# Run the synchronous function
if __name__ == "__main__":
    getFootballInfo()

# Problème la maintenant sur la façon de faire : 
    # Récupère beaucoup trop de lien car fait trop de recherche
    # Et si j'essayais juste de récupèrer 5 liens par site.
    # Quels mots-clés utilisé ?