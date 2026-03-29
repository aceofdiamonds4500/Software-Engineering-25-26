using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;
using System;

namespace LinuxGUI.ViewModels;

public partial class TranscriptiveViewModel : ViewModelBase
{
    [ObservableProperty] private string? _sampleName;
    [ObservableProperty] private string? _mediField;
    [ObservableProperty] private string? _transcription;
    [ObservableProperty] private string? _description;
    [ObservableProperty] private string? _tags;
    [ObservableProperty] private string? _outputTranscription;

    public ObservableCollection<string> Options { get; } = new() { "Cardiology", "Neurology", "General Medicine" };
    
    // Here defines the actual connection to the server
    private Connection _connection = new Connection("10.12.113.113", 5867);

    [RelayCommand]
    private void Send()
    {
        
        string payload = $$"""
                           {
                               "command": "CLASSIFY",
                               "timestamp": "{{DateTime.UtcNow:yyyy-MM-ddTHH:mm:ssZ}}",
                               "fields": {
                                   "Description": "{{Description}}",
                                   "Transcription": "{{Transcription}}",
                                   "Keywords": "{{Tags}}"
                               }
                           }
                           """;
        
        string response = _connection.ExchangeData(payload);
        
        OutputTranscription = response;
        
    }
}