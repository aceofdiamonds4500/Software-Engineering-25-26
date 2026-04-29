using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace linux_desktop.ViewModels;

public partial class NavigationViewModel : ViewModelBase
{
    
    private readonly HomeViewModel _homeView = new();
    private readonly TranscribeViewModel _transcribeView = new();
    private readonly HistoryViewModel _historyView = new();
    private readonly UploadViewModel _uploadView = new();
    
    [ObservableProperty] private ViewModelBase _currentView;
    
    public NavigationViewModel()
    {
        _currentView = _homeView;
    }

    [RelayCommand]
    public void OpenHomeView()
    {
        CurrentView = _homeView;
    }
    
    [RelayCommand]
    public void OpenTranscribeView()
    {
        CurrentView = _transcribeView;
    }
    
    [RelayCommand]
    public void OpenHistoryView()
    {
        CurrentView = _historyView;
    }
    
    [RelayCommand]
    public void OpenUploadView()
    {
        CurrentView = _uploadView;
    }

}