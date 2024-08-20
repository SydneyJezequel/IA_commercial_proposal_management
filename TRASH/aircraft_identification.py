MODEL_NAME = "microsoft/conditional-detr-resnet-50"  # or "facebook/detr-resnet-50"
IMAGE_SIZE = 480



from datasets import load_dataset





"""  *************** Chargement du dataset  *************** """
military_aicrafts =  load_dataset("Illia56/Military-Aircraft-Detection")
print(military_aicrafts)




"""  *************** Séparation en dataset de tests et d'entrainement  *************** """
if "validation" not in military_aicrafts:
    split = military_aicrafts["train"].train_test_split(0.15, seed=1337)
    military_aicrafts["train"] = split["train"]
    military_aicrafts["validation"] = split["test"]

# AFFICHER les datasets :
print(military_aicrafts)
print(military_aicrafts['train'][0])
print(military_aicrafts['test'][0])








"""  *************** Préparation des images  *************** """
from transformers import AutoImageProcessor

MAX_SIZE = IMAGE_SIZE

image_processor = AutoImageProcessor.from_pretrained(
    MODEL_NAME,
    do_resize=True,
    size={"max_height": MAX_SIZE, "max_width": MAX_SIZE},
    do_pad=True,
    pad_size={"height": MAX_SIZE, "width": MAX_SIZE},
)



import albumentations as A

train_augment_and_transform = A.Compose(
    [
        A.Perspective(p=0.1),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.HueSaturationValue(p=0.1),
    ],
    bbox_params=A.BboxParams(format="coco", label_fields=["category"], clip=True, min_area=25),
)

validation_transform = A.Compose(
    [A.NoOp()],
    bbox_params=A.BboxParams(format="coco", label_fields=["category"], clip=True),
)