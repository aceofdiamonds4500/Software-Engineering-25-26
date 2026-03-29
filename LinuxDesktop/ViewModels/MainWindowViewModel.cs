using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace LinuxGUI.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{
    [ObservableProperty]
    private ViewModelBase _currentPage;

    // On app start, the GUI will instantly load the main window, which will in turn load the Home view tab
    public MainWindowViewModel()
    {
        _currentPage = new HomeViewModel();
    }
    
    // These commands just create a new view whenever their button is pressed and the method is called.
    // Technically if garbage collection breaks then this will leak memory like hell, but that's a later problem.

    [RelayCommand]
    public void ToHome()
    {
        CurrentPage = new HomeViewModel();
    }
    [RelayCommand]
    public void ToTranscriptive()
    {
        CurrentPage = new TranscriptiveViewModel();
    }
    [RelayCommand]
    public void ToUpload()
    {
        CurrentPage = new UploadViewModel();
    }
    [RelayCommand]
    public void ToSettings()
    {
        CurrentPage = new SettingsViewModel();
    }
}
