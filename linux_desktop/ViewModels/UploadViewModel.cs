using CommunityToolkit.Mvvm.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using CommunityToolkit.Mvvm.Input;
using CommunityToolkit.Mvvm.Messaging;
using CsvHelper;
using CsvHelper.Configuration.Attributes;

namespace linux_desktop.ViewModels;

public partial class UploadViewModel : ViewModelBase
{
    
    //This Just Sets Our Variables To Send To The Transcribe View
    [ObservableProperty] private string? _sampleUpload;
    [ObservableProperty] private string? _fieldUpload;
    [ObservableProperty] private string? _descriptionUpload;
    [ObservableProperty] private string? _transcriptionUpload;
    [ObservableProperty] private string? _keyUpload;

    [RelayCommand]
    public void Upload(string filePath)
    {
        using (var reader = new StreamReader(filePath))
        using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
        {
            //This Sets Up So That Only The First Case Is Read
            var records = csv.GetRecords<PatientRecord>();
            var firstPatient = records.FirstOrDefault();

            //If The Values Exist, Set Them
            if (firstPatient != null)
            {
                SampleUpload = firstPatient.SampleName;
                FieldUpload = firstPatient.MedicalSpecialty;
                DescriptionUpload = firstPatient.Description;
                TranscriptionUpload = firstPatient.Transcription;
                KeyUpload = firstPatient.Keywords;
            }
        }
        
        //Now We Broadcast The Message Which Will Be Received By Transcribe View
        WeakReferenceMessenger.Default.Send(new UploadMessage(SampleUpload, FieldUpload, DescriptionUpload, TranscriptionUpload, KeyUpload));
        
    }
    
    //Originally This Would Have Been Replaced With Dynamic, But This Is A Placeholder Until Errors Are Resolved
    public class PatientRecord
    {
        [Index(0)] public int? Id { get; set; }
        [Name("description")] public string? Description { get; set; }
        [Name("medical_specialty")] public string? MedicalSpecialty { get; set; }
        [Name("sample_name")] public string? SampleName { get; set; }
        [Name("transcription")] public string? Transcription { get; set; }
        [Name("keywords")] public string? Keywords { get; set; }
    }

}

public record UploadMessage(string SampleUpload, string FieldUpload, string DescriptionUpload, string TranscriptionUpload, string KeyUpload);