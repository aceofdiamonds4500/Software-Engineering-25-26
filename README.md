# Software Engineering – Fall 2025  
## Project 2: Transcriptive – Harnessing AI for Smart Medical Transcription Enhancement  

### Team Members  
- Christopher Khun  
- Alexander Wilson  
- Brian Moore  
- Matthew Carden  
- Brett Lawrence  
- Nicholas Cieplensky  

---

## 🧠 Project Overview  
**Transcriptive** is an AI-powered medical transcription enhancement tool designed to improve accuracy, consistency, and efficiency in clinical documentation. The system leverages **Natural Language Processing (NLP)** and **Machine Learning (ML)** to interpret and refine medical transcriptions by detecting errors, classifying specialties, and extracting key medical entities such as diagnoses, medications, and procedures.

Built for clinicians, educators, and researchers, the tool aims to reduce manual correction time while promoting standardized documentation across medical specialties.

---

## ⚙️ Key Features  
- **Automated Transcription Enhancement:** Refines raw text by identifying common transcription errors using AI models trained on real-world medical data.  
- **Specialty Classification:** Automatically determines the medical specialty context (e.g., cardiology, radiology, neurology) for better organization and reporting.  
- **Entity Extraction:** Detects and highlights critical medical entities diagnoses, medications, and procedures. 
- **Error Detection and Correction:** Flags potential inaccuracies and suggests context-aware replacements.  
- **User-Friendly GUI:**  
  - Built with **VB.NET WinForms**  
  - Includes **Home**, **Transcribe**, **History**, and **Settings** tabs  
  - Features **animated sidebar transitions**, **dark/light mode toggle**, and **sound effects** for interactive elements  
  - Designed for **easy navigation** and **real-time feedback**  
- **Secure Local Storage:** Patient data and transcription logs are stored locally for privacy compliance and offline access.

---

## 🧩 Technologies Used  
| Category | Tools / Frameworks |
|-----------|-------------------|
| Programming Languages | VB.NET, Python |
| AI / NLP Frameworks | PyTorch, spaCy, NLTK |
| Dataset | MTSamples (medical transcription dataset) |
| GUI Framework | WinForms (.NET) |
| Data Handling | JSON, CSV |
| Version Control | GitHub |

---

## 🚀 How It Works  
1. **Load or Record Transcription:** Users can input raw transcripts manually or upload a text/audio file.  
2. **Processing Pipeline:**  
   - The text is analyzed through a PyTorch NLP model.  
   - The model performs specialty classification and entity recognition.  
   - Detected errors or inconsistencies are flagged with suggested corrections.  
3. **Enhanced Output:** A refined version of the transcript is generated, with entity highlights and an optional summary section.  
4. **History Tracking:** All processed transcriptions are stored locally, accessible via the “History” tab.  
5. **Customization:** Users can switch between dark/light themes, adjust preferences in “Settings,” and play sound cues for key interactions.

---

## 🧑‍💻 Project Goals  
- Improve transcription accuracy and readability through AI augmentation.  
- Reduce clinician workload by automating repetitive transcription cleanup.  
- Provide an intuitive, accessible interface suitable for non-technical users.  
- Demonstrate the integration of machine learning with GUI-based software design principles.

---

## 📈 Future Enhancements  
- Integration with live speech-to-text transcription.  
- Cloud-based model deployment for multi-user access.  
- Fine-tuning of models using domain-specific datasets.  
- Addition of analytics dashboard for usage insights.  

---

## 📂 Repository Structure  
