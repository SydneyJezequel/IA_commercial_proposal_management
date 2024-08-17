



# LIEN :
# https://huggingface.co/docs/transformers/tasks/visual_question_answering






""" ******************************************************* """
""" *************** Classic Fine-Tuning VQA *************** """
""" ******************************************************* """





""" ************* Chargement du dataset ************* """
from datasets import load_dataset
from PIL import Image
import itertools



# Chargement du dataset :
dataset = load_dataset("Graphcore/vqa", split="validation[:200]")
print(dataset)
print(dataset[0])

dataset = dataset.remove_columns(['question_type', 'question_id', 'answer_type'])
print(dataset)
print(dataset[0])

image = Image.open(dataset[0]['image_id'])
print(image)



# Récupération des labels et de leurs identifiants :
labels = [item['ids'] for item in dataset['label']]
flattened_labels = list(itertools.chain(*labels))
unique_labels = list(set(flattened_labels))

label2id = {label: idx for idx, label in enumerate(unique_labels)}
id2label = {idx: label for label, idx in label2id.items()} 



# Remplace les labels et ids d'inputs par ceux d'une autre liste :
def replace_ids(inputs):
  inputs["label"]["ids"] = [label2id[x] for x in inputs["label"]["ids"]]
  return inputs

# Chaque élément du dataset est passé à la fonction replace_ids, qui remplace les identifiants de labels par leurs équivalents numériques :
dataset = dataset.map(replace_ids)
flat_dataset = dataset.flatten()
flat_dataset.features








""" ************* Preprocessing Data ************* """

from transformers import ViltProcessor
import torch


processor = ViltProcessor.from_pretrained(model_checkpoint)


def preprocess_data(examples):
    # Récupération du texte et des images :
    image_paths = examples['image_id']
    images = [Image.open(image_path) for image_path in image_paths]
    texts = examples['question']    
    # Encodage du texte et des images :
    encoding = processor(images, texts, padding="max_length", truncation=True, return_tensors="pt")
    for k, v in encoding.items():
          encoding[k] = v.squeeze()
    targets = []
    # Prend des labels et des scores associés pour chaque exemple dans un dataset et les convertit en tensors de cibles (targets) utilisables par un modèle. :
    for labels, scores in zip(examples['label.ids'], examples['label.weights']):
        target = torch.zeros(len(id2label))
        #  :
        for label, score in zip(labels, scores):
            target[label] = score
        targets.append(target)
    encoding["labels"] = targets
    return encoding




# Preprocessing des données :
processed_dataset = flat_dataset.map(preprocess_data, batched=True, remove_columns=['question','question_type',  'question_id', 'image_id', 'answer_type', 'label.ids', 'label.weights'])
print(processed_dataset)









""" *************** Création d'un Batch d'exemples *************** """

from transformers import DefaultDataCollator

data_collator = DefaultDataCollator()









""" *************** Entrainement du modèle *************** """

from transformers import ViltForQuestionAnswering
from transformers import TrainingArguments
from transformers import Trainer


# Initialisation du modèle :
model = ViltForQuestionAnswering.from_pretrained(model_checkpoint, num_labels=len(id2label), id2label=id2label, label2id=label2id)


# Initialisation des Hyperparamètres :
repo_id = "MariaK/vilt_finetuned_200"
training_args = TrainingArguments(
    output_dir=repo_id,
    per_device_train_batch_size=4,
    num_train_epochs=20,
    save_steps=200,
    logging_steps=50,
    learning_rate=5e-5,
    save_total_limit=2,
    remove_unused_columns=False,
    push_to_hub=True,
)


# Initialisation du Trainer :
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=processed_dataset,
    tokenizer=processor,
)


# Exécution de l'entrainement :
trainer.train() 










""" *************** Inférence *************** """
from transformers import pipeline


# Initialisation du pipeline Hugging Face :
pipe = pipeline("visual-question-answering", model="MariaK/vilt_finetuned_200")


# Test du modèle :
example = dataset[0]
image = Image.open(example['image_id'])
question = example['question']
print(question)
pipe(image, question, top_k=1)












""" ********************************************* """
""" *************** Zero-Shot VQA *************** """
""" ********************************************* """

from transformers import AutoProcessor, Blip2ForConditionalGeneration
import torch



# Initialisation des modèles et devices :
processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)



# Initialisation du Test :
example = dataset[0]
image = Image.open(example['image_id'])
question = example['question']
prompt = f"Question: {question} Answer:" 



# Exécution du Test :
inputs = processor(image, text=prompt, return_tensors="pt").to(device, torch.float16)
generated_ids = model.generate(**inputs, max_new_tokens=10)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
print(generated_text)








