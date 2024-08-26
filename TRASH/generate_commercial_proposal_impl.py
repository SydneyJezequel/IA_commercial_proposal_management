




""" ********************** Exemple de dataset ******************* """

[
  {
    "input": {
      "Entreprise": "PeinturePro",
      "Quantité": "200 m²",
      "Prix unitaire": "15€/m²",
      "Délai": "7 jours",
      "Conditions de paiement": "50% à la commande, 50% à la livraison"
    },
    "output": "Devis: Pour la peinture de 200 m² à un prix unitaire de 15€/m², le total s'élève à 3000€. Le chantier sera terminé dans un délai de 7 jours. Les conditions de paiement sont de 50% à la commande et 50% à la livraison."
  },
  {
    "input": {
      "Entreprise": "BatiColor",
      "Quantité": "150 m²",
      "Prix unitaire": "18€/m²",
      "Délai": "5 jours",
      "Conditions de paiement": "30 jours après livraison"
    },
    "output": "Devis: Pour la peinture de 150 m² à un prix unitaire de 18€/m², le total s'élève à 2700€. Le chantier sera terminé dans un délai de 5 jours. Les conditions de paiement sont de 30 jours après livraison."
  },
  {
    "input": {
      "Entreprise": "DecoPeinture",
      "Quantité": "300 m²",
      "Prix unitaire": "12€/m²",
      "Délai": "10 jours",
      "Conditions de paiement": "40% à la commande, 60% à la réception des travaux"
    },
    "output": "Devis: Pour la peinture de 300 m² à un prix unitaire de 12€/m², le total s'élève à 3600€. Le chantier sera terminé dans un délai de 10 jours. Les conditions de paiement sont de 40% à la commande et 60% à la réception des travaux."
  },
  {
    "input": {
      "Entreprise": "ProBat",
      "Quantité": "250 m²",
      "Prix unitaire": "14€/m²",
      "Délai": "8 jours",
      "Conditions de paiement": "100% à la fin des travaux"
    },
    "output": "Devis: Pour la peinture de 250 m² à un prix unitaire de 14€/m², le total s'élève à 3500€. Le chantier sera terminé dans un délai de 8 jours. Les conditions de paiement sont de 100% à la fin des travaux."
  },
  {
    "input": {
      "Entreprise": "ArtPeint",
      "Quantité": "100 m²",
      "Prix unitaire": "20€/m²",
      "Délai": "4 jours",
      "Conditions de paiement": "30% à la commande, 70% à la livraison"
    },
    "output": "Devis: Pour la peinture de 100 m² à un prix unitaire de 20€/m², le total s'élève à 2000€. Le chantier sera terminé dans un délai de 4 jours. Les conditions de paiement sont de 30% à la commande et 70% à la livraison."
  },
  {
    "input": {
      "Entreprise": "Alpha Peinture",
      "Quantité": "250 m²",
      "Prix unitaire": "15€/m²",
      "Délai": "7 jours",
      "Conditions de paiement": "50% à la commande, 50% à la livraison"
    },
    "output": "Devis: Pour un chantier de 250 m² à un prix unitaire de 15€/m², le total s'élève à 3 750€. Le délai d'exécution est de 7 jours. Les conditions de paiement sont de 50% à la commande et 50% à la livraison."
  },
  {
    "input": {
      "Entreprise": "ProBat Peinture",
      "Quantité": "400 m²",
      "Prix unitaire": "12€/m²",
      "Délai": "10 jours",
      "Conditions de paiement": "30 jours après livraison"
    },
    "output": "Devis: Pour un chantier de 400 m² à un prix unitaire de 12€/m², le total s'élève à 4 800€. Le délai d'exécution est de 10 jours. Les conditions de paiement sont de 30 jours après livraison."
  },
  {
    "input": {
      "Entreprise": "Color'Expert",
      "Quantité": "150 m²",
      "Prix unitaire": "18€/m²",
      "Délai": "5 jours",
      "Conditions de paiement": "100% à la livraison"
    },
    "output": "Devis: Pour un chantier de 150 m² à un prix unitaire de 18€/m², le total s'élève à 2 700€. Le délai d'exécution est de 5 jours. Les conditions de paiement sont de 100% à la livraison."
  },
  {
    "input": {
      "Entreprise": "Rénov Peinture",
      "Quantité": "500 m²",
      "Prix unitaire": "10€/m²",
      "Délai": "14 jours",
      "Conditions de paiement": "60 jours après livraison"
    },
    "output": "Devis: Pour un chantier de 500 m² à un prix unitaire de 10€/m², le total s'élève à 5 000€. Le délai d'exécution est de 14 jours. Les conditions de paiement sont de 60 jours après livraison."
  },
  {
    "input": {
      "Entreprise": "Bâtiments & Couleurs",
      "Quantité": "300 m²",
      "Prix unitaire": "14€/m²",
      "Délai": "8 jours",
      "Conditions de paiement": "40% à la commande, 60% à la livraison"
    },
    "output": "Devis: Pour un chantier de 300 m² à un prix unitaire de 14€/m², le total s'élève à 4 200€. Le délai d'exécution est de 8 jours. Les conditions de paiement sont de 40% à la commande et 60% à la livraison."
  }
]






""" ********************** Pré-traitement des données ******************* """

def preprocess_data(examples):
    inputs = examples['input']
    outputs = examples['output']
    # Encodage des inputs et outputs
    encoding = processor(inputs, text_pair=outputs, padding="max_length", truncation=True, return_tensors="pt")
    encoding["labels"] = encoding["input_ids"].clone()  # Les labels sont les outputs textuels
    return encoding






""" ********************** Entrainement du modèle ******************* """

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Trainer, TrainingArguments

model_checkpoint = "gpt-2"  # Vous pouvez choisir un autre modèle selon votre besoin
model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

# Définir les arguments d'entraînement
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_steps=500,
    save_total_limit=2,
    remove_unused_columns=False,
)

# Entraînement avec Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=processed_dataset,  # le dataset pré-traité
    tokenizer=tokenizer,
)

trainer.train()






""" ********************** Inférence / Génération du Devis ******************* """

def generate_quote(model, tokenizer, input_data):
    inputs = tokenizer(input_data, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

input_data = "Quantité: 20, Prix unitaire: 30€, Délai: 7 jours, Conditions de paiement: 15 jours"
quote = generate_quote(model, tokenizer, input_data)
print(quote)





