using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;
using System;

namespace TranscriptiveLinux.ViewModels;

public partial class TranscribeViewModel : ViewModelBase
{
    //Observable Variables Used For JSON Command Values
    [ObservableProperty] private string? _sampleName;
    [ObservableProperty] private string? _fieldMedicine;
    [ObservableProperty] private string? _descriptionValue;
    [ObservableProperty] private string? _transcriptionValue;
    [ObservableProperty] private string? _keyWords;
    
    //Used For The Server Output -- Usually The AI Transcription
    [ObservableProperty] private string? _outputTranscription;

    //Observable Variables For The ComboBox
    public ObservableCollection<string>? MedicalField { get; } = new() { "Bariatrics", "Cardiology", "Dentistry","General Medicine", "Immunology", "Neurology", "Urology" };
    
    
    //Connection To Server -- Needs Manual IP And Port Assignment -- Permanent Port Has Been Set To 5867
    //Additional Command To Send To Server
    private readonly Connection _connection = new Connection("192.168.1.5", 5867);
    
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
                                   "Keywords": "{{KeyWords}}"
                               }
                           }
                           """;
        
        string response = _connection.ExchangeData(payload);
        
        OutputTranscription = response;
        
    }
}
