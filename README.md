# KRESZ Priority Advisor System

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Framework-Flask-000000?style=flat&logo=flask&logoColor=white)
![Owlready2](https://img.shields.io/badge/Semantic_Web-Owlready2-A42E2B?style=flat&logo=python&logoColor=white)
![Vercel](https://img.shields.io/badge/Deployment-Vercel-000000?style=flat&logo=vercel&logoColor=white)
![SWRL](https://img.shields.io/badge/Logic-SWRL%20%26%20HermiT-4B0082?style=flat)
![HTML5](https://img.shields.io/badge/Frontend-HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/Style-CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/Script-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/Status-Educational_Project-brightgreen?style=flat)
![License](https://img.shields.io/badge/License-All_Rights_Reserved-red?style=flat)

A Semantic Web-based decision support system that models the **Hungarian Highway Code (KRESZ) Section 28** regarding Priority at Intersections. The project was developed as part of the **BME-VIK "Natural Language and Semantic Technologies"** course.

The system determines the right-of-way between two vehicles using a hybrid reasoning approach: it combines an **OWL 2.0 Ontology and SWRL rules** with procedural Python logic to handle complex, non-monotonic traffic exceptions.

---

## 🚀 Live Demo

**Check out the live application here:**
👉 **[https://kresz-priority-advisor-system.vercel.app](https://kresz-priority-advisor-system.vercel.app)**

---

## ✨ Features

- 🚦 **Traffic Situation Modeling** – dynamic creation of ABox individuals (Vehicles, Roads, Signs) based on user input.
- 🧠 **Semantic Reasoning** – uses the **HermiT reasoner** (Owlready2's default `sync_reasoner()`) to infer priority relationships (`yieldsTo`) based on defined SWRL rules.
- 📜 **Complex Rule Handling** – implements the hierarchy of KRESZ § 28:
    - *Emergency Vehicles*
    - *Road Surface (Paved vs. Dirt)*
    - *Traffic Signs (Priority, Stop, Yield)*
    - *Tram Priority (in equal situations)*
    - *Right-hand Rule*
- 🌐 **Web Interface** – clean, responsive UI using Flask and Jinja2 templates.
- 🌗 **Dark/Light Mode** – user preference is saved in local storage.
- 📂 **Ontology Export** - ability to generate and save the static OWL model file.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.10+
- **Web Server:** Flask
- **Semantic Web:**
    - **Owlready2:** For Ontology manipulation and SWRL rule integration.
    - **HermiT:** For consistency checking and inference.
- **Frontend:** HTML5, CSS3, JavaScript

---

## 📂 Project Structure
```
KRESZ-Priority-Advisor_Python/
├── app/
│   ├── app.py
│   ├── business_logic.py
│   └── generate_ontology.py
│
├── model/
│   └── kresz_model.owl
│
├── static/
│   ├── favicon.ico
│   ├── icon-256.png
│   ├── scripts.js
│   └── style.css
│
├── template/
│   ├── 404.html
│   ├── _macros.html
│   ├── base.html
│   └── index.html
│
├── requirements.txt
└── vercel.json
```

---

## 🧠 Ontology & Logic

The system creates a new in-memory ontology with a unique IRI (`http://test.org/kresz_<uuid>.owl`) for every request to ensure a stateless calculation.

1. **TBox (Terminology)**
    - **Classes:** `Vehicle` (Subclasses: `Tram`, `EmergencyVehicle`), `Road` (Subclasses: `PavedRoad`, `DirtRoad`), `TrafficSign` (`StopSign`, `PrioritySign`, etc.).
    - **Properties:** `locatedOn` (Vehicle $\to$ Road), `hasSign` (Road $\to$ Sign), `isRightOf` (Spatial relation).
2. **Reasoning (SWRL & Python)**
The logic follows a strict hierarchy:
    1. **Emergency Vehicles:** Always take precedence (unless meeting another emergency vehicle).
    2. **Road Surface:** Dirt roads yield to paved roads.
    3. **Traffic Signs:** SWRL rules infer `yieldsTo` relations based on sign hierarchy (e.g., STOP vs. Priority).
    4. **Equal Situations:** If signs/roads are equal rank:
        - **Tram Rule:** Trams take priority.
        - **Right-hand Rule:** The vehicle coming from the right has priority.

---

## 📝 Implementation of Course Requirements

**Dynamic Ontology Construction (Requirement 3)**
Instead of using a static file from Protege, the ontology is built **programmatically using Owlready2** in `business_logic.py`. This approach allows for dynamic instantiation of ABox individuals based on user input, making the system more flexible and robust than a static `.owl` file.

**Defined Query Scenarios (Requirement 4)**
The system dynamically evaluates any user-defined scenario. Below are specific test cases (queries) that demonstrate the rule engine's capabilities:

1. **Emergency Vehicle Priority:**
    - *Input:* User (Car) vs. Other (Emergency Vehicle).
    - *Rule:* `Vehicle(?v1), EmergencyVehicle(?v2) -> yieldsTo(?v1, ?v2)`
    - *Result:* **User yields.**
2. **Sign Hierarchy:**
    - *Input:* User (STOP Sign) vs. Other (Priority Road).
    - *Rule:* `StopSign(?s1) ^ PrioritySign(?s2) -> yieldsTo(?v1, ?v2)`
    - *Result:* **User yields.**
3. **Tram Rule (Equal Situation):**
    - *Input:* Equal intersection (both Paved, no Signs), Other is a Tram coming from Left.
    - *Rule:* `Tram(?v2) ^ ... -> yieldsTo(?v1, ?v2)`
    - *Result:* **User yields.**
4. **Right-hand Rule (Equal Situation):**
    - *Input:* Equal intersection, Other vehicle coming from Right.
    - *Rule:* `isRightOf(?v2, ?v1) -> yieldsTo(?v1, ?v2)`
    - *Result:* **User yields.**

---

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/hajdu-patrik/KRESZ-Priority-Advisor_Python.git
cd KRESZ-Priority-Advisor_Python
```

### 2. Create and Activate Virtual Environment

**Windows (Git Bash):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Static Ontology Model

Before running the app, you can generate the static `.owl` file (saved to `model/`):
```bash
python app/generate_ontology.py
```

### 5. Run the Application

To launch the server (the script automatically handles the split folder structure):
```bash
python app/app.py
```
The server will be available here:
- http://127.0.0.1:5000
- http://localhost:5000

Open it in your browser to use it.

---

## 🎮 Usage Example

1. **Open the Web Interface.**
2. **Configure Vehicle 'A' (You):**
    - Type: *Car*
    - Road: *Paved*
    - Sign: *STOP Sign*
3. **Configure Vehicle 'B' (Other):**
    - Type: *Car*
    - Road: *Paved*
    - Sign: *Priority Road*
    - Direction: *Coming from Left*
4. **Click Analyze.**

**Result:**
    ⚠️ **ELSŐBBSÉGET KELL ADNOD!** (Tábla szabályozás) (*Since Vehicle B is on a priority road and you have a STOP sign, the SWRL rule infers that you must yield*)

---

## 📦 Deployment

This project is configured for automated deployment via **Vercel**.
Any push to the `main` branch automatically triggers a new build and deployment.

| Environment | Status |
| :--- | :--- |
| **Production** | [![Vercel App](https://img.shields.io/badge/Visit-Live_App-success?style=for-the-badge&logo=vercel)](https://kresz-priority-advisor-system.vercel.app) |

---

## 📄 License

Copyright (c) Hajdú Patrik Zsolt. All rights reserved.

Published for demonstration and portfolio purposes only. Using any part of this code as a solution for an academic assignment is strictly prohibited. See [LICENSE.md](LICENSE.md) for the full terms.
