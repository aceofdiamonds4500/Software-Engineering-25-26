using System;
using System.Linq;
using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using CommunityToolkit.Mvvm.Messaging;

namespace linux_desktop.ViewModels;

public partial class TranscribeViewModel : ViewModelBase, IRecipient<UploadMessage>
{

    [ObservableProperty] private string? _sampleName;
    [ObservableProperty] private string? _fieldMedicine;
    [ObservableProperty] private string? _transcriptionValue;
    [ObservableProperty] private string? _descriptionValue;
    [ObservableProperty] private string? _keyWords;
    [ObservableProperty] private string? _firstName;
    [ObservableProperty] private string? _lastName;
    [ObservableProperty] private string? _outputTranscription;
    
    public ObservableCollection<string>? MedicalField { get; } = new() { " Allergy / Immunology",
        " Bariatrics",
        " Cardiovascular / Pulmonary",
        " Neurology",
        " Dentistry",
        " Urology",
        " General Medicine",
        " Surgery",
        " Speech - Language",
        " SOAP / Chart / Progress Notes",
        " Sleep Medicine",
        " Rheumatology",
        " Radiology",
        " Psychiatry / Psychology",
        " Podiatry",
        " Physical Medicine - Rehab",
        " Pediatrics - Neonatal",
        " Pain Management",
        " Orthopedic",
        " Ophthalmology",
        " Office Notes",
        " Obstetrics / Gynecology",
        " Neurosurgery",
        " Nephrology",
        " Letters",
        " Lab Medicine - Pathology",
        " IME-QME-Work Comp etc.",
        " Hospice - Palliative Care",
        " Hematology - Oncology",
        " Gastroenterology",
        " ENT - Otolaryngology",
        " Endocrinology",
        " Emergency Room Reports",
        " Discharge Summary",
        " Diets and Nutritions",
        " Dermatology",
        " Cosmetic / Plastic Surgery",
        " Consult - History and Phy.",
        " Chiropractic",
        " Autopsy" };
    
    //Connection To Server -- Needs Manual IP And Port Assignment -- Permanent Port Has Been Set To 5867
    //Additional Command To Send To Server
    private readonly Connection _connection = new Connection("127.0.0.1", 5867);
    
    public bool IsAnyFieldEmpty()
    {
        var fieldsDatabase = new[] {SampleName, FieldMedicine, TranscriptionValue, DescriptionValue, KeyWords, FirstName, LastName};
        return fieldsDatabase.Any(string.IsNullOrWhiteSpace);
    }
    
    [RelayCommand]
    public void Send()
    {
        
        string payload = $$"""
                           {
                               "command": "CLASSIFY",
                               "timestamp": "{{DateTime.UtcNow:yyyy-MM-ddTHH:mm:ss}}",
                               "fields": {
                                   "Description": "{{DescriptionValue}}",
                                   "Transcription": "{{TranscriptionValue}}",
                                   "MedicalSpecialty": "{{FieldMedicine}}",
                                   "SampleName": "{{SampleName}}",
                                   "Keywords": "{{KeyWords}}",
                                   "p_firstname": "{{FirstName}}",
                                   "p_lastname": "{{LastName}}",
                                   "confidence": "0"
                               }
                           }
                           """;
        
        //Now Additionally Sends The Output To The History Tab
        OutputTranscription = _connection.ExchangeData(payload);
        WeakReferenceMessenger.Default.Send(new TranscriptionMessage(TranscriptionValue + "\n" + OutputTranscription));
        
    }
    
    //Register To Receive The Upload Message
    public TranscribeViewModel()
    {
        WeakReferenceMessenger.Default.Register(this);
    }
    
    //Receive The Upload Values And Apply Them
    public void Receive(UploadMessage message)
    {
        SampleName = message.SampleUpload;
        FieldMedicine = message.FieldUpload;
        DescriptionValue = message.DescriptionUpload;
        TranscriptionValue = message.TranscriptionUpload;
        KeyWords = message.KeyUpload;
    }
    
}

public record TranscriptionMessage(string Transcription);