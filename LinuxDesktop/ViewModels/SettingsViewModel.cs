using CommunityToolkit.Mvvm.ComponentModel;

namespace TranscriptiveLinux.ViewModels;

public partial class SettingsViewModel : ViewModelBase
{
    [ObservableProperty]
    private string? _settingsNote; // This survives even if the window is closed
}