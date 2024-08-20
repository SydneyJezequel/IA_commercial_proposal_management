from openai import OpenAI
import openai
import config





class Model:
    """ Classe du Modèle """



    def __init__(self):
        """ Constructeur """



    def generate_answer(self, question):
        """ Méthode qui interroge le modèle """

        client = OpenAI(
        base_url = config.MONSTER_API_URL,
        api_key = config.MONSTER_API_KEY
        )

        completion = client.chat.completions.create(
        model= "meta-llama/Meta-Llama-3-8B-Instruct" ,
        messages=[{"role": "user", "content": question}],
        temperature=0.9,
        top_p=0.9,
        max_tokens=1000,
        stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")



