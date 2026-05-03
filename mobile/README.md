# Transcriptive AI — Android App Client

> Kotlin / Jetpack Compose frontend for the Transcriptive AI medical NLP platform.

---

## Features

- Medical transcription input with specialty options [optional].
- NLP classification via backend - returns diagnosis, keywords, and structured description.
- Transcription history with expandable detail cards.
- Group / organization management - create a group with a shareable code or join an existing one.
- Admin panel - view all group members and their transcription records.
- Biometric login [fingerprint] via Biometric, toggleable per user.
- Firebase password reset.
- Profile picture upload [Firebase Storage].
- Dark mode and enlarged text settings, persisted to Firestore.
- Account settings - profile info, security, privacy, group, billing, payments, support.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Kotlin |
| UI | Jetpack Compose, Material3 |
| Networking | Ktor (TCP socket to backend) |
| Auth | Firebase Authentication |
| Database | Cloud Firestore |
| File Storage | Firebase Storage |
| Image Loading | Coil |
| Serialization | Gson |
| Biometrics | AndroidX Biometric |

---

## Project Structure

```
app/src/main/java/com/example/myapplication/
│
├── MainActivity.kt                  # App entry point, screen state machine, drawer nav
│
├── screens/
│   ├── AccountSettingsScreen.kt     # Account settings menu
│   ├── AdminScreen.kt               # Admin panel - view all group member transcriptions
│   └── HistoryScreen.kt             # Personal transcription history for each user
│
├── network/
│   └── Connection.kt                # Ktor TCP socket connection to NLP backend
│
├── WelcomeScreen.kt                 # Login / Register entry screen
├── LoginScreen.kt                   # Email + password login, biometric gate
├── RegisterScreen.kt                # New account registration
├── ForgotPasswordScreen.kt          # Firebase password reset
├── TermsOfService.kt                # Terms of service screen
│
├── TranscribeScreen.kt              # Main transcription input and classification
│
├── CreateJoinGroupScreen.kt         # Choose to create or join a group
├── CreateGroupScreen.kt             # Create a new organization group
├── JoinGroupScreen.kt               # Join an existing group via code
├── GroupSettingsScreen.kt           # View group info, members, copy code, leave group
│
├── HomeScreen.kt                    # Dashboard - recent transcriptions, weekly bar chart
├── SettingsScreen.kt                # Dark mode, enlarge text, link to account settings
├── ProfileInformationScreen.kt      # Edit name, password, profile picture
├── SecurityScreen.kt                # Biometrics and 2FA toggles
├── PrivacyDataScreen.kt             # Privacy toggles, download transcriptions (NOT WORKING)
├── BillingSubscriptionScreen.kt     # Subscription plan and billing cycle (NOT WORKING)
├── PaymentsScreen.kt                # Payment method entry (NOT WORKING)
└── SupportLegalScreen.kt            # Legal disclaimer
```

---

## Firestore Data Model

```
users/
  {uid}/
    FirstnameLastname   : String
    email               : String
    admin               : Number   (0 = user, 1 = admin)
    biometrics          : String   ("0" or "1")  f / t
    darkmode            : String   ("0" or "1")  f / t
    enlargeText         : String   ("0" or "1")  f / t
    groupID             : String
    organizationName    : String
    profilePicUrl       : String?

    transcriptions/
      {docId}/
        data            : String   (JSON-serialized TranscriptionItem)

groups/
  {groupID}/
    groupID             : String
    organizationName    : String
    createdBy           : String        (uid)
    members             : List<String>  (uid)
```

> **Note:** Transcription records are stored as a JSON string in the `data` field, serialized via Gson into a `TranscriptionItem` object. Fields: `id`, `title`, `date`, `preview`, `specialty`, `transcription`, `description`, `keywords`, `diagnosis`.

---

## Getting Started

### Prerequisites

- Latest version of Android Studio.
- JDK 17+.
- A Firebase project with Auth, Firestore, and Storage enabled.
- The Transcriptive AI backend running (see backend README).

### Setup

1. Clone the repository.
2. Open the `app/` folder in Android Studio.
3. Add your `google-services.json` to `app/`.
4. Enable the following in your Firebase console:
   - Authentication - Email/Password provider
   - Firestore - create a database
   - Storage - create a storage bucket
5. Start the backend (see backend README) and confirm it is reachable.
6. Make sure the connection is set to the right ip address read below.
7. Run the app on an emulator or physical device.

### Backend Networking

The app connects to the backend via TCP. The host is currently hardcoded in `TranscribeScreen.kt`:

```kotlin
val connection = Connection("10.0.2.2", 5867)
```

`10.0.2.2` is the Android emulator's alias for `localhost` on the host machine. If running on a physical device or in a different environment (like a seperate serrver) update this value accordingly.

---

## Known Issues / Roadmap

| Item | Status |
|---|---|
| Backend host/port hardcoded in `TranscribeScreen.kt` | Should be moved to a config file |
| Billing & Payments screens | UI only, no logic wired up |
| Privacy & Data - download/delete | Stub buttons, not yet implemented |
| 2FA toggle in Security screen | UI only, not functional |
