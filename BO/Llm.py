from openai import OpenAI
import config





class Llm:
    """ Classe du Modèle """



    def __init__(self):
        """ Constructeur """



    def generate_answer(self, prompt):
        """ Méthode qui interroge le modèle """

        client = OpenAI(
        base_url = config.MONSTER_API_URL,
        api_key = config.MONSTER_API_KEY
        )



        """ PREMIERE VERSION """
        """
        completion = client.chat.completions.create(
            model= "meta-llama/Meta-Llama-3-8B-Instruct" ,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            top_p=0.9,
            max_tokens=1000,
            stream=True
        )
        """

        """ VERSION DE TEST """
        completion = client.chat.completions.create(
            model= "meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Réduire pour une réponse plus déterministe
            top_p=0.8,        # Limiter les choix pour une réponse plus prévisible
            max_tokens=500,
            stream=True
        )



        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        return full_response

