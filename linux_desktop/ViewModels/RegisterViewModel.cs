using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using CommunityToolkit.Mvvm.Messaging;
using System;
using System.Threading.Tasks;
using Firebase.Auth;
using Firebase.Auth.Providers;

namespace linux_desktop.ViewModels;

public partial class RegisterViewModel : ViewModelBase
{
 
    [ObservableProperty] private string? _email;
    [ObservableProperty] private string? _password;
    [ObservableProperty] private string? _passwordConfirm;
    [ObservableProperty] private string? _message;
    
    private readonly string _apiKey = "AIzaSyCdCCeFFwSYFYwD6STaWEGsqdnLkYwtrE0";

    [RelayCommand]
    public async Task RegisterAsync()
    {
        //Confirms All Fields Are Being Used, And The Passwords Match
        if (string.IsNullOrWhiteSpace(Email) || string.IsNullOrWhiteSpace(Password))
        {
            Message = "Error: Email and Password are required.";
            return;
        }
        
        if (Password != PasswordConfirm)
        {
            Message = "Error: Passwords do not match.";
            return;
        }
        
        var config = new FirebaseAuthConfig
        {
            ApiKey = _apiKey,
            AuthDomain = "transcriptive-ai.firebaseapp.com",
            Providers = [ new EmailProvider() ]
        };
        
        try
        {
            var client = new FirebaseAuthClient(config);
            
            //Creates The User In Firebase
            var auth = await client.CreateUserWithEmailAndPasswordAsync(Email, Password);
            
            Message = "Registration successful!";
            
            //Go Back To Login
            WeakReferenceMessenger.Default.Send(new RegisterSuccessMessage());
        }
        
        //Catch Errors When Configured
        catch (FirebaseAuthException ex)
        {
            Message = $"Registration failed: {ex.Reason}";
        }
        catch (Exception)
        {
            Message = "A connection error occurred.";
        }
        
    }

    [RelayCommand]
    public void Login()
    {
        WeakReferenceMessenger.Default.Send(new LoginGoTo());
    }
    
}