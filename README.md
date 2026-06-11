# Détection EPI sur chantier — Traitement d'image (YOLOv8)

Projet de détection des équipements de protection individuelle (EPI : casque,
gilet de sécurité, gants...) sur des images et vidéos de chantier, à partir du
dataset [SH17](https://github.com/ahmadmughees/sh17dataset) (17 classes), avec
un modèle YOLOv8m et des règles de conformité basées sur l'IoU.

## Structure du dépôt

```
Projet/
├── documentation/        # Rapport détaillé par étape (01 à 05)
│   ├── 01.Preparation_donnees.md
│   ├── 02.Choix_modele.md
│   ├── 03.Configuration_entrainement.md
│   ├── 04.Evaluation.md
│   └── 05.Inference.md
├── notebooks/             # Notebooks exécutés sur le serveur distant (GPU)
│   ├── 0_pipeline_complet.ipynb        # Pipeline bout-à-bout (toutes les étapes)
│   ├── 1_2_exploration.ipynb
│   ├── 1_3_pretraitement.ipynb
│   ├── 1_4_augmentation.ipynb
│   ├── 2_1_choix_modele.ipynb
│   ├── 2_2_configuration.ipynb
│   ├── 2_3_evaluation.ipynb
│   ├── 2_4_entraitement_1024.ipynb
│   ├── 4_inference.ipynb
│   ├── 4_1_inference_1024.ipynb
│   ├── 5_1_comparaison_modeles.ipynb   # Axe A
│   ├── 5_2_tracking.ipynb              # Axe D
│   └── 5_3_streamlit.ipynb             # Axe E
├── reorganize_dataset.py  # Script de réorganisation du dataset SH17
├── rapport_images/        # Images utilisées dans le rapport
├── *.png / *.jpg          # Captures de résultats (matrice de confusion, démo Streamlit, ...)
└── requirements.txt
```

Le dataset SH17 (`SH17dataset/`, ~14 Go) ainsi que les vidéos d'inférence et
les poids entraînés (`runs/`) ne sont pas versionnés (voir `.gitignore`) : ils
sont régénérés/téléchargés via les notebooks et stockés sur le serveur distant
de calcul.

## Documentation

Le déroulé complet du projet est documenté dans `documentation/` :

1. **01 - Préparation des données** : récupération du dataset SH17, réorganisation
   train/val/test, pré-traitement, augmentation.
2. **02 - Choix du modèle** : justification du choix de YOLOv8m.
3. **03 - Configuration de l'entraînement** : hyperparamètres, résolution d'entrée.
4. **04 - Évaluation** : métriques globales et par classe (mAP50, mAP50-95,
   précision, rappel, F1), comparaison 640×640 vs 1024×1024.
5. **05 - Inférence** : pipeline de détection + règles de conformité EPI,
   inférence image/vidéo, tracking, application Streamlit.

## Modèle retenu

YOLOv8m entraîné en résolution **1024×1024** (`yolov8m_epi_1024-2/weights/best.pt`,
epoch 79) — voir `documentation/04.Evaluation.md` section 2.4 pour le détail des
métriques (mAP50 = 0.697, mAP50-95 = 0.412, Précision = 0.798, Rappel = 0.616,
F1 = 0.695).

## Règles de conformité EPI

La conformité est vérifiée via le recouvrement (IoU) entre la détection d'un
EPI et la partie du corps censée être protégée :

| EPI            | Partie du corps | Message si absent           |
|----------------|------------------|------------------------------|
| `helmet`       | `head`           | casque manquant              |
| `safety-vest`  | `person`         | gilet de securite manquant   |
| `gloves`       | `hands`          | gants manquants              |

## Axes optionnels traités (Partie 2)

- **Axe A** — Comparaison de modèles (YOLOv8m, Faster R-CNN, SSD300, DETR) :
  `notebooks/5_1_comparaison_modeles.ipynb`
- **Axe D** — Tracking vidéo (ByteTrack, suivi de conformité par travailleur) :
  `notebooks/5_2_tracking.ipynb`
- **Axe E** — Application de démonstration Streamlit (upload d'image, réglage
  du seuil de confiance et de l'IoU) : `notebooks/5_3_streamlit.ipynb`

## Reproduction

1. Installer les dépendances : `pip install -r requirements.txt`
2. Renseigner ses identifiants Kaggle (`kaggle.json`, non versionné) pour
   télécharger le dataset SH17 (voir `documentation/01.Preparation_donnees.md`).
3. Exécuter `notebooks/0_pipeline_complet.ipynb` pour parcourir l'intégralité
   du pipeline (préparation des données, configuration du modèle, évaluation,
   inférence + règles de conformité), ou les notebooks détaillés dans l'ordre :
   `1_2` → `1_3` → `1_4` → `2_1` → `2_2` → `2_3` → `2_4` → `4` / `4_1` →
   `5_1` / `5_2` / `5_3`.

Les seeds sont fixées (`seed=42`) dans les notebooks `1_2`, `1_3` et `1_4`
pour garantir la reproductibilité du split train/val/test.
