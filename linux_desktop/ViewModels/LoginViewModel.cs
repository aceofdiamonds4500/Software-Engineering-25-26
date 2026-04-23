using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using CommunityToolkit.Mvvm.Messaging;
using System;
using System.Threading.Tasks;
using Firebase.Auth;
using Firebase.Auth.Providers;

namespace linux_desktop.ViewModels;

public partial class LoginViewModel : ViewModelBase
{
    [ObservableProperty] private string? _username;
    [ObservableProperty] private string? _password;
    [ObservableProperty] private string? _message;
    
    private readonly string _apiKey = "AIzaSyCdCCeFFwSYFYwD6STaWEGsqdnLkYwtrE0";
    
    [RelayCommand]
    public async Task LoginAsync()
    {
        //If Either Input Field Is Empty, Don't Log in
        if (string.IsNullOrWhiteSpace(Username) || string.IsNullOrWhiteSpace(Password))
        {
            Message = "Error: Missing username or password";
            return;
        }

        //Configures the Authentication With Firebase Itself Using the API Key
        var config = new FirebaseAuthConfig
        {
            ApiKey = _apiKey,
            AuthDomain = "transcriptive-ai.firebaseapp.com",
            Providers = new FirebaseAuthProvider[]
            {
                new EmailProvider()
            }
        };

        //Try To Actually Login
        try
        {
            var client = new FirebaseAuthClient(config);
            var auth = await client.SignInWithEmailAndPasswordAsync(Username, Password);
            
            Message = "";
            WeakReferenceMessenger.Default.Send(new LoginSuccessMessage());
        }
        
        //Login Errors Made Here
        catch (FirebaseAuthException ex)
        {
            Message = $"Login failed: {ex.Reason}";
        }
        
        catch (Exception ex)
        {
            Message = "A connection error occurred.";
        }
    }
}