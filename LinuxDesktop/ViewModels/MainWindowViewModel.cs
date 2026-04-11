using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace TranscriptiveLinux.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{
    
    private readonly HomeViewModel _homeView = new();
    private readonly SettingsViewModel _settingsView = new();
    private readonly TranscribeViewModel _transcribeView = new();
    
    [ObservableProperty]
    private ViewModelBase _currentView;
    
    public MainWindowViewModel()
    {
        _currentView = _homeView;
    }

    [RelayCommand]
    public void OpenHomeView()
    {
        CurrentView = _homeView;
    }
    
    [RelayCommand]
    public void OpenSettingsView()
    {
        CurrentView = _settingsView;
    }

    [RelayCommand]
    public void OpenTranscribeView()
    {
        CurrentView = _transcribeView;
    }
    
}