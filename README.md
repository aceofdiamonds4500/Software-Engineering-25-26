# 🧠 Software Engineering GUI Project - Transcriptive Application

## 📘 Overview
This project is a **Windows Forms–based GUI** developed in **C# (.NET 6+)** for the **Software Engineering (2025–2026)** course.  
It demonstrates multi-form navigation, data handling, and UX design through a simulated **medical transcription management system**.

---

## 🖥️ Core Features

### 🧭 Multi-Form Navigation System
- Central controller form (`Form1`) manages navigation between:
  - **Home (FormMain)**
  - **Transcribe (FormTranscribe)**
  - **History (FormHistory)**
  - **Settings (FormSettings)**
  - **Download/Upload (FormDownloadUpload)**
- Each form is dynamically loaded into a shared content panel.
- Sidebar includes:
  - **Animated expand/collapse** transition.
  - **Slide sound effect (`slide.wav`)** during expansion/collapse.
- Every navigation button and interactive element includes **sound feedback (`click.wav`)** for a polished user experience.

---

## 🏠 Home Page (FormMain)
- Serves as the **landing screen** when the application starts.  
- Displays a welcome message and short overview of the project.
- Automatically updates appearance with **dark mode** and **enlarged text toggles**.
- Simple, minimal, and consistent with the rest of the application’s design.

---

## ✍️ Transcribe Page (FormTranscribe)
- Central workspace for creating and managing transcription data.
- Input fields:
  - **Description**
  - **Sample Name**
  - **Transcription Text**
  - **Keywords**
  - **Medical Specialty (ComboBox)**
- **Tooltip system** provides detailed instructions and examples for each field.
- **Export to JSON**:
  - Saves all field data in structured JSON format.
  - Auto-generates filename: `payload-YYYYMMDD_HHMMSS.json`.
  - Includes version, timestamp, and all field entries.
- **Clear Form** button resets all text and dropdown inputs instantly.
- **Dark mode** and **font scaling** applied dynamically.
- **Sound feedback** plays on all buttons and interactions.

---

## 🕓 History Page (FormHistory)
- Placeholder section for viewing **past transcriptions or export logs**.
- Supports **theme toggling** (light/dark) and **enlarge text** functions for accessibility.
- Designed for future implementation of a **history tracking system** (e.g., JSON or database log).

---

## ⚙️ Settings Page (FormSettings)
- Provides user control over application appearance and accessibility:
  - **Dark Mode Toggle**
  - **Enlarge Text Toggle**
- Toggles update all forms simultaneously via a broadcast system.
- **Sound feedback** plays when toggles are activated.
- Visual **on/off indicators** using icons (✅ / ❌).
- Works globally across every page for a consistent experience.

---

## 📂 Download / Upload Page (FormDownloadUpload)
- **Upload CSV files** to quickly load transcription data:
  - Detects headers like `Description`, `Transcription`, `Specialty`, and `Keywords`.
  - Automatically maps and transfers data into the Transcribe form.
- **Export transcription** data as `.csv` files for storage or sharing.
- Built-in validation checks for missing headers or invalid CSVs.
- Clear feedback messages (success, cancel, or error).
- Fully compatible with **dark mode**, **font enlargement**, and **sound feedback**.

---

## 🔊 Sound Effects & Interactivity
All **interactive elements** have responsive sound effects:
- Sidebar buttons → `click.wav`
- Sidebar toggle → `slide.wav`
- Form buttons (Export, Upload, Clear, Toggle) → `click.wav`
- Labels and icons → `click.wav`

This gives every action a clear, tactile sense of feedback and enhances overall user engagement.

---

## 🎨 User Interface & Experience
- **Borderless window** with draggable title panel.
- **Animated sidebar** with smooth transitions.
- **Sound effects** on all interactive buttons.
- **Tooltips** for user guidance on Transcribe page.
- **Dark Mode & Enlarge Text** toggle across all forms.
- **Adaptive color scheme:**
  - Light mode → pastel blue & white
  - Dark mode → deep navy & midnight blue

---

## 🧩 Technical Details
- **Language:** C#
- **Framework:** Windows Forms (.NET 6+)
- **Entry Point:** `Program.cs` → launches `Form1`
- **Namespaces Used:**
  - `System.Media` — sound playback
  - `System.IO` — file operations
  - `Microsoft.VisualBasic.FileIO` — CSV parsing
- **Core UI Components:**
  - Panels, Buttons, PictureBoxes
  - ComboBoxes, RichTextBoxes
  - ToolTips for field assistance
