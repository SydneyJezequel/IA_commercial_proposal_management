OBJECTIF DE CE PROJET :
Cette fonctionnalité utilise de l'IA pour :
1- Comparer des offres commercial en fonction d'un besoin.
2- Rédiger un argumentaire commercial pour positionner l'une des offres par rapport aux autres.




REMARQUES PREALABLES :
* Ce projet utilise un LLM via une Api. Dans un contexte professionnel, un LLM propre à l'entreprise doit être utilisé pour assurer la confidentialité de vos données.
* Le dataset utilisé est composé de devis tous basés sur le même format. Dans un contexte professionnel, il faut améliorer les traitements pour gérer d'autres formats de devis avec des résolutions parfois plus faible.
* En ajustant ce code, il doit pouvoir être utilisable pour différents types d'offres (ex : offre de produits bancaires).




TUTORIEL :

1- Enregistrer les devis des concurrents à l’emplacement suivant :
CommercialProposals/ressources/quotations_files

2- Renseigner les avantages comparatifs (atouts, référence clients, etc.) de votre entreprise le fichier suivant :
CommercialProposals/ressources/commercial_advantages_list.jsonl.
Le format pour renseigner ses informations est le suivant :
{"instruction": « Question à laquelle répondre, "context": "Le type de question", "response": « Réponse », "category": "closed_qa"}

3- Exécuter la fonctionnalité qui charge le contenu des devis dans la BDD SQL depuis votre navigateur : http://localhost:8011/load-quotations
Une copie de la liste des informations récupérées dans les devis est renvoyé sous forme de JSON. Elle peut donc être intégrable dans un front. 

4- Exécuter la fonctionnalité qui génère un devis et son offre commerciale sur la base des devis et données de votre entreprise. Les données de l’entreprise sont stockées dans la BDD Vectorielle durant cette étape, avant la génération du devis et de l’offre :
http://localhost:8011//generate-commercial-proposal
Le résultat est renvoyé sous forme de JSON. Il peut donc être intégrable dans un front.

N’hésitez pas à suivre les logs d’exécution dans votre IDE.




MODELES UTILISEES :
* Le modèle utilisé pour récupéré pour récupérer les informations textuelles dans les devis est modèle un OCR (Optical Character Recognition).
* Le LLM utilisé est LLAMA3 via MONSTER API : 
https://monsterapi.ai/user/playground?model=meta-llama/Meta-Llama-3-8B-Instruct




REMARQUES ET CONSEILS D'UTILISATION :

* Un diagramme d'activité est stocké à côté de ce README pour illustrer l'exécution des 2 fonctionnalités.

* Ce projet fait appel à un LLM à travers une Api. Dans un contexte professionnel, un LLM propre à l'entreprise doit être utilisé. Cela permet d’assurer la confidentialité de vos données et d’améliorer ses performances par rapport aux cas d’usages. Par exemple, on peut Fine-Tuner ce LLM avec un dataset propre au secteur de l’entreprise pour améliorer les performances. Il faut, néanmoins, avoir en tête que le Fine-Tuning est plus gourmand en ressources que l’utilisation d’une BDD Vectorielle. La mise à jour du modèle sera donc plus coûteuse et complexe via le Fine-Tuning qu’avec l’actualisation d’une BDD Vectorielle.

* Il est possible que l’Api qui permet d’accéder au LLM soit coupé. Si c’est le cas, je vous invite à passer par l’Api d’un autre LLM et à modifier le format du prompt utilisé pour communiquer avec lui (fichier : LLM / Méthode : generate_commercial_proposal()).

* Les devis du dataset utilisent tous le même format. Dans un contexte professionnel, il faut améliorer les traitements pour gérer d'autres formats de devis avec des résolutions parfois plus faibles.

* Le README contient des informations complémentaires pour manipuler les fonctionnalités de ce projet.

* Les noms des classes et méthodes sont en anglais. Les commentaires en français. La classe Quotation qui représente un devis est nommé en anglais pour être en ligne avec les autres fichiers. Ses variables sont en français pour l’affichage des informations du devis.

* Les prompt utilisés sont ceux du modèle d’IA de Méta Llama 3. Je les ai récupéré dans la documentation officiel et ai ajusté les paramètres suivants pour obtenir les résultats souhaités :
-temperature=0.1,  # Réduire pour une réponse plus déterministe
-top_p=0.8,        # Limiter les choix pour une réponse plus prévisible
Vous pouvez jouer avec ses paramètres pour obtenir des résultats différents.


* L’utilisation d’une BDD SQL pour stocker les devis est plus adaptée qu’une BDD vectorielle. Une BDD SQL est conçue pour fournir des réponses précises et structurées. C’est adapté à notre besoin quand il s’agit de fournir des informations précises au LLM. Une BDD vectorielle génère des comparaisons ou des réponses enrichies ce qui correspond à notre besoin pour enrichir le devis d’informations sur notre société.

* Il est nécessaire d’être précis quant au rabais souhaité dans le prompt envoyé au LLM. Sinon, il peut générer un devis dont le montant est 0. * La qualité des images fournies à un modèle de type OCR doit être élevée pour récupérer des données fiables. Il faut donc disposer d’images de qualité et/ou mettre en place des traitements en amont du LLM pour lui fournir des données qualitatives.




DEPENDANCES UTILISEES :
Package                                  Version
---------------------------------------- ---------
absl-py                                  2.1.0
accelerate                               0.31.0
aiohttp                                  3.9.5
aiosignal                                1.3.1
albucore                                 0.0.13
albumentations                           1.4.14
annotated-types                          0.6.0
anyio                                    4.3.0
asgiref                                  3.8.1
astunparse                               1.6.3
attrs                                    23.2.0
backoff                                  2.2.1
bcrypt                                   4.2.0
blis                                     0.7.11
build                                    1.2.1
cachetools                               5.5.0
catalogue                                2.0.10
certifi                                  2023.5.7
charset-normalizer                       3.3.2
chroma-hnswlib                           0.7.6
chromadb                                 0.5.5
click                                    8.1.7
cloudpathlib                             0.18.1
coloredlogs                              15.0.1
confection                               0.1.5
contourpy                                1.2.0
cycler                                   0.12.1
cymem                                    2.0.8
datasets                                 2.20.0
Deprecated                               1.2.14
dill                                     0.3.8
distro                                   1.9.0
dlib                                     19.24.2
eval_type_backport                       0.2.0
evaluate                                 0.4.2
face-recognition                         1.3.0
face-recognition-models                  0.3.0
fastapi                                  0.110.0
filelock                                 3.13.1
flatbuffers                              24.3.25
fonttools                                4.49.0
fr-core-news-md                          3.7.0
frozenlist                               1.4.1
fsspec                                   2024.2.0
gast                                     0.6.0
google-auth                              2.34.0
google-pasta                             0.2.0
googleapis-common-protos                 1.63.2
greenlet                                 3.0.3
grpcio                                   1.65.5
h11                                      0.14.0
h5py                                     3.11.0
httpcore                                 1.0.5
httptools                                0.6.1
httpx                                    0.27.0
huggingface-hub                          0.23.3
humanfriendly                            10.0
idna                                     3.6
imageio                                  2.35.0
importlib_metadata                       8.0.0
importlib_resources                      6.4.3
inexactsearch                            1.0.2
install                                  1.3.5
Jinja2                                   3.1.3
jiter                                    0.5.0
joblib                                   1.2.0
keras                                    3.5.0
kiwisolver                               1.4.5
kubernetes                               30.1.0
langcodes                                3.4.0
language_data                            1.2.0
lazy_loader                              0.4
libclang                                 18.1.1
marisa-trie                              1.2.0
Markdown                                 3.7
markdown-it-py                           3.0.0
MarkupSafe                               2.1.5
matplotlib                               3.8.3
mdurl                                    0.1.2
ml-dtypes                                0.3.2
mmh3                                     4.1.0
monotonic                                1.6
monsterapi                               1.0.9.2
mpmath                                   1.3.0
multidict                                6.0.5
multiprocess                             0.70.16
murmurhash                               1.0.10
namex                                    0.0.8
networkx                                 3.2.1
numpy                                    1.26.4
oauthlib                                 3.2.2
onnxruntime                              1.19.0
openai                                   1.41.0
opencv-python-headless                   4.10.0.84
opentelemetry-api                        1.26.0
opentelemetry-exporter-otlp-proto-common 1.26.0
opentelemetry-exporter-otlp-proto-grpc   1.26.0
opentelemetry-instrumentation            0.47b0
opentelemetry-instrumentation-asgi       0.47b0
opentelemetry-instrumentation-fastapi    0.47b0
opentelemetry-proto                      1.26.0
opentelemetry-sdk                        1.26.0
opentelemetry-semantic-conventions       0.47b0
opentelemetry-util-http                  0.47b0
opt-einsum                               3.3.0
optree                                   0.12.1
orjson                                   3.10.7
overrides                                7.7.0
packaging                                23.2
pandas                                   2.2.2
Pillow                                   10.1.0
pip                                      24.2
posthog                                  3.5.2
preshed                                  3.0.9
protobuf                                 4.25.4
psutil                                   5.9.8
pyarrow                                  16.1.0
pyarrow-hotfix                           0.6
pyasn1                                   0.6.0
pyasn1_modules                           0.4.0
pydantic                                 2.8.2
pydantic_core                            2.20.1
Pygments                                 2.18.0
pyparsing                                3.1.1
PyPika                                   0.48.9
pyproject_hooks                          1.1.0
pyspellchecker                           0.8.1
pytesseract                              0.3.10
python-dateutil                          2.8.2
python-dotenv                            1.0.1
pytz                                     2024.1
PyYAML                                   6.0.1
regex                                    2024.5.15
requests                                 2.32.3
requests-oauthlib                        2.0.0
requests-toolbelt                        1.0.0
rich                                     13.7.1
rsa                                      4.9
safetensors                              0.4.3
scikit-image                             0.24.0
scikit-learn                             1.2.2
scipy                                    1.10.1
sentence-transformers                    3.0.1
setuptools                               65.5.0
shellingham                              1.5.4
silpa-common                             0.3
six                                      1.16.0
smart-open                               7.0.4
sniffio                                  1.3.1
soundex                                  1.1.3
spacy                                    3.7.5
spacy-legacy                             3.0.12
spacy-loggers                            1.0.5
spellchecker                             0.4
SQLAlchemy                               2.0.32
srsly                                    2.4.8
starlette                                0.36.3
sympy                                    1.12
tenacity                                 9.0.0
tensorboard                              2.16.2
tensorboard-data-server                  0.7.2
tensorflow                               2.16.2
tensorflow-io-gcs-filesystem             0.37.1
termcolor                                2.4.0
thinc                                    8.2.5
threadpoolctl                            3.1.0
tifffile                                 2024.8.10
tokenizers                               0.19.1
tomli                                    2.0.1
torch                                    2.2.1
torchvision                              0.17.1
tqdm                                     4.66.4
transformers                             4.41.2
typer                                    0.12.4
typing_extensions                        4.12.2
tzdata                                   2024.1
urllib3                                  2.2.1
uvicorn                                  0.27.1
uvloop                                   0.20.0
wasabi                                   1.1.3
watchfiles                               0.23.0
weasel                                   0.4.1
websocket-client                         1.8.0
websockets                               13.0
Werkzeug                                 3.0.3
wheel                                    0.44.0
wrapt                                    1.16.0
xxhash                                   3.4.1
yarl                                     1.9.4
zipp                                     3.20.0




COMMANDES PERSO :
export PYTHONPATH=/Users/sjezequel/PycharmProjects/CommercialProposals:$PYTHONPATH
echo $PYTHONPATH

