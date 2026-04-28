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
    
    public ObservableCollection<string>? MedicalField { get; } = new() { "Bariatrics", "Cardiology", "Dentistry","General Medicine", "Immunology", "Neurology", "Urology" };
    
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
                                   "Keywords": "{{KeyWords}}",
                                   "p_firstname": "{{FirstName}}",
                                   "p_lastname": "{{LastName}}"
                               }
                           }
                           """;
        
        //Now Additionally Sends The Output To The History Tab
        OutputTranscription = _connection.ExchangeData(payload);
        WeakReferenceMessenger.Default.Send(new TranscriptionMessage(TranscriptionValue + "\n" + OutputTranscription));

        if (IsAnyFieldEmpty() == false)
        {
            payload = $$"""
                        {
                            "command": "INSERTPATIENT",
                            "timestamp": "{{DateTime.UtcNow:yyyy-MM-ddTHH:mm:ss}}",
                            "fields": {
                                "p_firstname": "{{FirstName}}",
                                "p_lastname": "{{LastName}}",
                                "desc": "{{DescriptionValue}}",
                                "med_specialty": "{{FieldMedicine}}",
                                "sample_name": "{{SampleName}}",
                                "transcription": "{{TranscriptionValue}}"
                              }
                        }
                        """;
            
            _connection.ExchangeData(payload);
        }
        
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