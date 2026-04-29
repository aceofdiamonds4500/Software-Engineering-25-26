using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.Messaging;

namespace linux_desktop.ViewModels;

public partial class HistoryViewModel : ViewModelBase, IRecipient<TranscriptionMessage>
{
    
    //The New History Feature
    public ObservableCollection<string> TranscriptionHistory { get; } = new();
 
    public HistoryViewModel()
    {
        WeakReferenceMessenger.Default.Register(this);
    }
    
    //When The Message From TranscribeViewModel Is Received, Add It To The List
    public void Receive(TranscriptionMessage message)
    {
        if (!string.IsNullOrWhiteSpace(message.Transcription))
        {
            TranscriptionHistory.Add(message.Transcription);
        }
    }
    
}