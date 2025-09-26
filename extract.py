from datetime import date, timedelta
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# On récupère la date pour le prompt
today = date.today()
yesterday = today - timedelta(days=1)
def getFootballInfo():
    """
    Synchronous version - simpler to understand and use
    """
    # Create the client
    client = genai.Client(api_key=os.getenv('GEMINI_KEY'))
    
    # Send the prompt to Gemini
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="""Effectue une recherche approfondie sur Internet des actualités les plus récentes concernant le football. Concentre-toi spécifiquement sur les sources d'informations suivantes :
    *   https://www.walfoot.be/
    *   https://www.lequipe.fr/Football/

    Analyse le contenu de ces sites pour identifier les articles d'actualité publiés au cours des dernières 24 heures. Privilégie les articles traitant des sujets suivants (liste non exhaustive, mais indicative) :

    *   Résultats de matchs récents
    *   Blessures de joueurs
    *   Analyses de matchs
    *   Informations sur les compétitions (Ligue 1, Ligue des Champions, etc.)

    Pour chaque article d'actualité pertinent trouvé, fournis les informations suivantes :

    1.  **Titre de l'article :** (Le titre exact de l'article)
    2.  **Lien URL :** (L'adresse web complète de l'article)
    3.  **Date et heure de publication :** (Indiquer la date et l'heure de publication de l'article, si disponibles)
    4.  **Source :** (Le nom du site web d'où provient l'article)
    5.  **Résumé :** (Un court résumé de 2-3 phrases de l'article, mettant en évidence les points clés)

    Présente les résultats sous forme de liste structurée.

    **Important :**

    *   Ne recherche pas d'informations en dehors des sites web spécifiés.
    *   Ne choisis que des articles publiés entre {} et {}.
    *   Assure-toi que les liens URL fournis sont valides et fonctionnels.
    *   Ignore les articles non pertinents (par exemple, les articles d'opinion sans contenu informatif direct).
    *   Retourne un maximum de 10 articles.""".format(yesterday,today)
    )
    
    # Print the response
    print(response)
    
    # Close the client

    
# Fetch links using gemini api
# Scrape the articles
# Use gemini to summarize the articles
# Send emails (using mailjet ?)
# Mettre sur un serveur ?

# Run the synchronous function
if __name__ == "__main__":
    getFootballInfo()

