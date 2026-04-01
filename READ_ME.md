# PreSkool - Systeme de Gestion Scolaire

Projet academique (2025/2026). Application web Django pour centraliser la gestion d'une ecole: etudiants, enseignants, departements, matieres, emplois du temps, examens, jours feries, avec acces par roles.

## Fonctionnalites

- CRUD des entites principales
- Dashboards selon le role (Admin, Teacher, Student)
- Notes sur 20 avec mention automatique
- Interface Bootstrap responsive

## Tech stack

- Python 3.13
- Django 5.x
- SQLite
- Bootstrap 4

## Architecture du projet

- Pattern Django MVT (Model / View / Template)
- Apps principales: home_auth, faculty, student, teacher, departement, subject, timetable, exam, holiday

Structure (resume):

```
pfm-school-management/
├── monenv/                      ← Environnement virtuel Python (isolé)
└── school/                      ← Répertoire principal du projet Django
    ├── manage.py                ← Point d'entrée Django (commandes)
    ├── requirements.txt         ← Dépendances du projet
    ├── db.sqlite3               ← Base de données SQLite
    │
    ├── school/                  ← Configuration centrale
    │   ├── settings.py          ← INSTALLED_APPS, AUTH_USER_MODEL, STATIC...
    │   ├── urls.py              ← Routage principal (inclut les apps)
    │   └── wsgi.py
    │
    ├── faculty/                 ← Dashboards (admin / teacher / student)
    ├── home_auth/               ← Auth + CustomUser + Décorateurs RBAC
    ├── student/                 ← CRUD Étudiants + Parents
    ├── teacher/                 ← CRUD Enseignants
    ├── department/              ← CRUD Départements
    ├── subject/                 ← CRUD Matières
    ├── holiday/                 ← CRUD Jours Fériés
    ├── timetable/               ← CRUD Emploi du Temps + Bonus iframe
    ├── exam/                    ← CRUD Examens + Résultats avec note
    ├── Rapport/
    ├── Video-demonstratif/
    ├── static/assets/           ← CSS, JS, images Bootstrap (PreSkool theme)
    ├── media/                   ← Photos uploadées (students/, teachers/)
    └── templates/
        ├── Home/                ← base.html + dashboards
        ├── authentication/      ← login, register, logout, reset password
        ├── students/            ← templates CRUD étudiants
        ├── teachers/            ← templates CRUD enseignants
        ├── departments/
        ├── subjects/
        ├── holidays/
        ├── timetable/
        └── exams/

```

## Rapport et video demonstratif

- Rapport technique: [pfm-school-management/Rapport](pfm-school-management/Rapport)
- Video demonstrative: [Video-demonstratif](Video-demonstratif)

## Installation rapide

```bash
cd pfm-school-management\school
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/.

## Comptes de test

| Role    | Email                | Mot de passe |
| ------- | -------------------- | ------------ |
| Admin   | admin@admin.com      | admin123     |
| Teacher | teacher@preskool.com | teacher123   |
| Student | student@preskool.com | student123   |

## Donnees de demo (optionnel)

```bash
python seed.py
```

## Limite connue

- L'iframe Visual Timetabling peut etre bloquee par X-Frame-Options du site tiers , c'est pout ca il est recommandé de installer l'extention "
  Ignore X-Frame headers" .
