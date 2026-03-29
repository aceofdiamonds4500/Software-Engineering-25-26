# Transcriptive GUI - Linux
Here my aim is to bring the Transcriptive AI's GUI to Linux. The current build is only supported on Windows, which this repo aims to fix.
# Structure
## File Structure
```
LinuxGUI
|   Models - Empty for now
|   |   Empty
|   View -- These are design files for how each tab looks
|   |   HomeView.axaml
|   |   HomeView.axaml.cs
|   |   MainWindow.axaml
|   |   MainWindow.axaml.cs
|   |   SettingsView.axaml
|   |   SettingsView.axaml.cs
|   |   TranscriptiveView.axaml
|   |   TranscriptiveView.axaml.cs
|   |   UploadView.axaml
|   |   UploadView.axaml.cs
|   ViewModels -- Contains extra logic for a tab if needed
|   |   HomeViewModel.cs
|   |   MainWindowsViewModel.cs
|   |   SettingsViewModel.cs
|   |   TranscriptiveViewModel.cs
|   |   UploadViewModel.cs
|   |   ViewModelBase.cs
|
|   Program.cs
|   App.axaml
|   App.axaml.cs
```

## Project Structure
This project is build around Model-View-ViewModel (MVVM) which is a file
structure that has each tab of the program organised as a "view". The program
launches with the MainWindow.axaml which contains all permanently loaded UI elements.

After this the MainWindow.axaml loads any views as defined later in the file such as HomeView.axaml.

Each view comes with it's own logic in the "ViewModels" - such as TrancsriptiveViewModel.cs

# Setup

This project can be setup for basic use with:

```
git clone https://github.com/ZoeTheDragon-Git/TranscriptiveGUI
unzip TranscriptiveGUI.zip
cd TranscriptiveGUI
```

Or you can prepare this project for development with:

```
mkdir LinuxGUI
cd LinuxGUI
git init
git branch -m main
git remote add origin git@github.com:ZoeTheDragon-Git/TranscriptiveGUI
git pull origin main
```

This project makes use of Avalonia UI and the Community Toolkit MVVM libraries.
To import these libraries, simply run these commands:

```
dotnet new install Avalonia.Templates
dotnet add package CommunityToolkit.Mvvm
```

Once the repo has been cloned and you are ready, simply run:

```
dotnet run
```

This project doesn't require an IDE, so assuming you have the .NET SDK, the GUI should now run.

# Usage

This section will detail the UI and basic usage.

## Home

This is a static homescreen. The main function here is just to show what Transcriptive actually is, and greet the user. Maybe we'll add our funny legal policy placeholder, but for now it's pretty basic.

## Transcribe

Here we have the transcription tab, which sends a set of fields to the AI's controller.py file with a command to be executed.

### Sample Name

NOTE !!! This is currently not part of the command, but will be added later on.
This field represents the reason for a patient's visit, or what procedure was done during their stay.\

```
Laparoscopic Gastric Bypass\
Liposuction\
Urology Consult\
2-D Echocardiogram - 1\
etc.
```

### Field of Medicine

NOTE !!! This is currently not part of the command, but will be added later on.
Currently only three options exist, but this will be expanded to classify multiple medical fields.\

```
Cardiology\
Neurology\
Allergy\
Bariatrics\
Urology\
General Medicine\
etc
```

### Transcription



### Description 

### Keywords

This is just general keywords to help summarize what is generally being observed.

## Upload

Not yet implemented...

## Settings

Not yet implemented...
