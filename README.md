# 🧪 Auto-Evaluation Tool — V1.0.0

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Version](https://img.shields.io/badge/version-v1.0.0-brightgreen.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Education](https://img.shields.io/badge/made%20for-education-blueviolet.svg)
![Roast Mode](https://img.shields.io/badge/roast-mode_enabled-red.svg)
![Sandbox](https://img.shields.io/badge/sandbox-secure-orange.svg)
![Chaotic Good Teacher](https://img.shields.io/badge/teacher-chaotic%20good-ff69b4.svg)
![Mini Kattis](https://img.shields.io/badge/engine-mini--kattis-lightgrey.svg)
![Student Tears](https://img.shields.io/badge/student_tears-++%20collected-9cf.svg)
![Security](https://img.shields.io/badge/security-path_traversal_proof-success.svg)
![Powered by Suffering](https://img.shields.io/badge/powered_by-student_suffering-ff0000.svg)

Un outil d'auto-évaluation automatisé conçu pour mes cours de programmation.  
Ce système corrige automatiquement les exercices, applique un système de points,
déclenche un mode *cooldown* avec feedbacks personnalisés (et parfois des roasts 👀),
et exporte les résultats vers un dépôt Git privé.

Cette **V1 est entièrement opérationnelle** et sert déjà pour des évaluations réelles.

---

## 🚀 Fonctionnalités — Version 1.0.0 (Stable)

### ✅ 1. Évaluation hybride
- QCM + exercices pratiques
- Sélection aléatoire d’exercices (pondérés)
- Comptage automatique des points
- Seuil de réussite configurable

### ✅ 2. Sandbox d’exécution
- Exécution sécurisée des programmes étudiants (Python)
- Timeout automatique
- Isolation et logs d’erreurs
- Support pour inputs multiples par test

### ✅ 3. Comparaison stricte des sorties
- Normalisation des outputs
- Aucun espace ou ligne superflue permis (mode Kattis)
- Tests définis par `tests.json`

### ✅ 4. Cooldown & Feedback
- Pénalité croissante sur les nouvelles tentatives
- Messages personnalisés
- Roasts thématiques selon l'exercice pour le *fun* 🤭

### ✅ 5. Gestion des étudiants
- Dossier par élève
- Historique + `results.json`
- Détection des noms de fichiers attendus
- Interface CLI simple

### ✅ 6. Intégration Git
- Clone automatique du dépôt privé
- Push des résultats d’évaluation
- Structure compatible LMS minimal

---

## 🛠️ Architecture
```bash
.
├── app.py
├── config/
│   ├── eval_config.json
│   ├── qcm.json
│   ├── exercises.json
│   └── roasts.json
├── eval_core/
│   ├── engine.py
│   ├── sandbox_runner.py
│   ├── comparator.py
│   ├── cooldown.py
│   ├── scoring.py
│   ├── utils.py
│   ├── git_manager.py
│   └── file_loader.py
├── exercises/
│   └── exercice_name/
│       ├── tests.json
│       └── description.md
└── results/
└── <student_name>/
└── results.json
```

---

## 🎯 Roadmap — Version 2.0 (à venir)

### 🔜 Corrections & Améliorations
- Support multi-langage (C, Java)
- Comparator flexible (espaces, tolérance optionnelle)
- Interface admin plus complète
- Tracking des tentatives par exercice
- Sécurisation renforcée (hash des fichiers, anti-triche léger)

### 🔜 Nouvelles fonctionnalités
- Interface web (Streamlit ou FastAPI)
- Dashboard progression étudiants
- Export PDF des résultats
- Mode “exercices pratiques” hors évaluation
- Support pour exercices interactifs (input multiples)

### 🔜 Developer Experience
- Tests unitaires (pytest)
- Pipeline CI/CD pour GitHub Actions
- Documentation complète (mkdocs)

V2 sera focalisée sur **plus de sécurité, plus d’automatisation, plus de fun** 🔥

---

## 📌 Installation

```bash
git clone <dépôt_privé>
cd Auto-Evaluation-Tool
python3 app.py
```
## 📜 Licence

Projet à usage pédagogique.
Réutilisation libre pour les enseignants / formateurs.

---

## 🧑‍💻 Auteur

Développé par Léhane Payet aka Wolfinn
Chaotic Good Teacher ✨
