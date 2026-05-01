# **Transcriptive**

Transcriptive is a medical application that uses AI to read patient transcripts, and recommend a specialist.
This is meant to help doctors speed up the process of directing patients to the correct specialist for whatever treatment they need.
Currently, the Transcriptive AI is self-contained in a server package, while the UI can be used standalone on any PC with a registered account.
Please note that Transcriptive **_is not a valid replacement for professional medical advice_**, and is intended to be used by doctors who can verify that the information appears correct.

## **Configuration**

### **Packages**

This project uses .Net 10.0 but supports lower versions such as .Net 9.0


To use a lower .Net version, open the `linux_desktop.csproj` file and edit:
```
<TargetFramework>net10.0</TargetFramework>
```
Into:
```
<TargetFramework>net9.0</TargetFramework>
```


Additionally, the packages should auto install, but if needed, you can download:
```
dotnet new install Avalonia.Templates CommunityToolkit.Mvvm Avalonia.Svg.Skia FirebaseAuthentication.net
```

### **Running The App**
In order to run the app, move into the linux_desktop folder and run: ```dotnet run```

The UI should now launch and present you with a login screen.

## **Usage**
This section goes over the actual usage of the application.

### **Login Menu**
This menu handles basic login functionality. If you don't have an email and password, use the register menu.

### **Register**
This menu handles basic registration. Registration simply requires an email and a matching password in both fields.

### **Transcribe**

The Transcribe menu can be divided into two sections: 

Required - These fields are required to ensure that the illness / condition can be classified.

Optional - These fields are used for an unimplemented feature which would bypass classification and add the information as a sample in the training database.

##### Description - Required
The description field takes a basic description of the user, using details such as
```
sex
age
build
any apparent physical abnormalities
```

##### Transcription - Required

The transcription field takes information about the patient's illness such as
```
basic description
symptoms
medications involved
attempted treatments
```

##### Keywords - Required

The keywords field takes a set of words that are important within the given transcription, and can help emphasize these as more important terms.

##### Sample Name - Optional
The sample name field takes the name of an illness / condition.

##### First Name - Optional
The first name field takes the last name of a patient.

##### Last Name - Optional
The last name field takes the last name of a patient.

##### Field of Medicine - Optional
The field of medicine field takes the field of medicine associated with an illness.

### **History**
The History menu is a basic part of the UI that displays the previous classification that were complete during the current user session.

### **Upload**
The Upload menu is another simple menu with only one button: Upload

to use the upload button, take a file named ```sample.csv``` and add it to the linux_desktop folder. Be sure to use the same formatting as the provided sample.csv.

Now when pressing upload, the first transcription from the csv will be taken and applied to the transcription menu.

## **Notes**

Features surrounding the optional fields in the transcribe menu have not been implemented.