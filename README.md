[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]

<br />
<div align="center">
  <h1 align="center">Transcriptive AI</h3>

  <p align="center">
    An AI-powered solution to modifying and classifying medical transcriptions for hospitals.
    <br />
    <a href="https://github.com/aceofdiamonds4500/Software-Engineering-25-26/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/aceofdiamonds4500/Software-Engineering-25-26/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

Supported Operating Systems:

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) 
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)

Languages Used:

![C#](https://img.shields.io/badge/c%23-%23239120.svg?style=for-the-badge&logo=csharp&logoColor=white) 
![Kotlin](https://img.shields.io/badge/kotlin-%237F52FF.svg?style=for-the-badge&logo=kotlin&logoColor=white) 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

AI Tools:

![HuggingFace](https://img.shields.io/badge/huggingface-%23FFD21E.svg?style=for-the-badge&logo=huggingface&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=numpy&logoColor=white) 
![Pandas](https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) 
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)

DevOps Tools:

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) 
![Firebase](https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Gradle](https://img.shields.io/badge/Gradle-02303A.svg?style=for-the-badge&logo=Gradle&logoColor=white)
![Android Studio](https://img.shields.io/badge/Android%20Studio-3DDC84.svg?style=for-the-badge&logo=android-studio&logoColor=white) 
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

### Description

Transcriptive is a project for our 2025-26 Software Engineering course, which includes a locally hosted full stack application with a mobile/desktop frontend and a containerized backend. Running the software is simple and lightweight, and offers hospitals a tool for writing transcriptions faster and more effectively using a local AI model and Natural Language Processing for autocorrections.

### Main Components
- Client-Controller-Server Model

- Windows/Linux Desktop Application
- Android Mobile Application w/ Firebase Support
- Custom Python-based Controller w/ Command Design
- MySQL Database
- Hugging Face Pre-trained AI Model w/ NLP

### Installation

_Below is a step-by-step on installing and running the Docker container for the server with the locally hosted AI._

1. Clone the repo:
   ```sh
   git clone https://github.com/aceofdiamonds4500/Software-Engineering-25-26.git
   ```
2. Create the environment variables for MySQL (be sure to change the passwords to your desired password):
   ```sh
   cd Software-Engineering-25-26/backend_container
   echo -e 'MYSQL_PASSWORD=password\nMYSQL_ROOT_PASSWORD=password' > .env
   ```
3. Run the container using Docker Compose:
   ```sh
   docker compose up --build
   ``` 

### Top contributors:

<a href="https://github.com/aceofdiamonds4500/Software-Engineering-25-26/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=aceofdiamonds4500/Software-Engineering-25-26" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/aceofdiamonds4500/Software-Engineering-25-26
[contributors-url]: https://github.com/aceofdiamonds4500/Software-Engineering-25-26/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/aceofdiamonds4500/Software-Engineering-25-26
[forks-url]: https://github.com/aceofdiamonds4500/Software-Engineering-25-26/network/members
[issues-shield]: https://img.shields.io/github/issues/aceofdiamonds4500/Software-Engineering-25-26
[issues-url]: https://github.com/aceofdiamonds4500/Software-Engineering-25-26/issues
