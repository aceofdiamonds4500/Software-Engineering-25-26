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

