using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Messaging;

namespace linux_desktop.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{

    [ObservableProperty] private ViewModelBase _currentView;

    private readonly LoginViewModel _loginViewModel = new();
    private readonly RegisterViewModel _registerViewModel = new();
    private readonly NavigationViewModel _navigationViewModel = new();
    
    public MainWindowViewModel()
    {
        //On start, show the login screen, and wait for a success message to trigger the rest of the program
        //Plans are to use firebase for authentication
        _currentView = _loginViewModel;
        WeakReferenceMessenger.Default.Register<LoginSuccessMessage>(this, (r, m) => { CurrentView = _navigationViewModel;});
        WeakReferenceMessenger.Default.Register<RegisterSuccessMessage>(this, (r, m) => { CurrentView = _loginViewModel;});
        WeakReferenceMessenger.Default.Register<RegisterGoTo>(this, (r, m) => { CurrentView = _registerViewModel;});
        WeakReferenceMessenger.Default.Register<LoginGoTo>(this, (r, m) => { CurrentView = _loginViewModel;});
    }
    
}

public record LoginSuccessMessage();
public record RegisterSuccessMessage();
public record RegisterGoTo();
public record LoginGoTo();