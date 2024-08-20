from openai import OpenAI
import config




client = OpenAI(
  base_url = config.MONSTER_API_URL,
  api_key = config.MONSTER_API_KEY
)



completion = client.chat.completions.create(
 model= "meta-llama/Meta-Llama-3-8B-Instruct" ,
 messages=[{"role":"user","content":"Whats the meaning of life"}],
 temperature=0.9,
 top_p=0.9,
 max_tokens=1000,
 stream=True
 )



for chunk in completion:
 if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")



