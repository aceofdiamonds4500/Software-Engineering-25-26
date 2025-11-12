using System;
using System.IO;
using System.Windows.Forms;
using System.Media;
using System.Drawing;
using Microsoft.VisualBasic.FileIO;

namespace GUI_SoftwareEng
{

    public partial class FormDownloadUpload : Form
    {
        private readonly FormTranscribe _transcribe;
        public string uploadedTxtPath = string.Empty;
        private SoundPlayer _soundplayer;

        public FormDownloadUpload(FormTranscribe transcribe)
        {
            InitializeComponent();
            _transcribe = transcribe ?? throw new ArgumentNullException(nameof(transcribe));
            _soundplayer = new SoundPlayer("click.wav");
        }

        // save transcription to a txt file
        private void button1_Click(object sender, EventArgs e)
        {
            _soundplayer.Play();
            if (_transcribe == null)
            {
                label1.Text = "Error: transcribe page not available.";
                return;
            }

            // pull from the new accessor that maps to output
            string textToSave = _transcribe.OutputTranscription ?? string.Empty;

            if (string.IsNullOrWhiteSpace(textToSave))
            {
                label1.Text = "Nothing to save (transcription is empty).";
                return;
            }

            try
            {
                using (var sfd = new SaveFileDialog())
                {
                    sfd.Title = "Save transcription";
                    sfd.Filter = "CSV Files (*.csv)|*.csv";
                    sfd.DefaultExt = "csv";
                    sfd.FileName = "transcription.csv";

                    var result = sfd.ShowDialog(this);
                    if (result != DialogResult.OK)
                    {
                        label1.Text = "Save canceled.";
                        return;
                    }

                    // Save as csv
                    string csvLine = $"\"{textToSave.Replace("\"", "\"\"")}\"";
                    File.WriteAllText(sfd.FileName, csvLine);
                    label1.Text = $"Saved: {Path.GetFileName(sfd.FileName)}";
                }
            }
            catch (Exception ex)
            {
                label1.Text = $"Error saving file: {ex.Message}";
            }
        }

        // Upload the stuff
        private void button2_Click(object sender, EventArgs e)
        {
            _soundplayer.Play();
            {
                using (var ofd = new OpenFileDialog())
                {
                    ofd.Title = "Select an input CSV";
                    ofd.Filter = "CSV Files (*.csv)|*.csv";
                    ofd.FilterIndex = 1;
                    ofd.Multiselect = false;

                    if (ofd.ShowDialog(this) == DialogResult.OK)
                    {
                        try
                        {
                            using (var parser = new TextFieldParser(ofd.FileName))
                            {
                                parser.TextFieldType = FieldType.Delimited;
                                parser.SetDelimiters(",");
                                parser.HasFieldsEnclosedInQuotes = true;
                                parser.TrimWhiteSpace = true;

                                if (parser.EndOfData)
                                {
                                    throw new InvalidDataException("CSV is empty.");
                                }

                                // headers
                                string[] headers = parser.ReadFields();
                                if (headers == null || headers.Length == 0)
                                {
                                    throw new InvalidDataException("CSV missing header row.");
                                }

                                int idxDescription = IndexOf(headers, "Description");
                                int idxSpecialty = Prefer(headers, "Medical_Specialty", "Specialty");
                                int idxSampleName = Prefer(headers, "Sample_Name", "Sample Name");
                                int idxTranscription = IndexOf(headers, "Transcription");
                                int idxKeywords = IndexOf(headers, "Keywords");

                                if (idxDescription < 0 || idxTranscription < 0)
                                {
                                    throw new InvalidDataException("CSV must include at least 'Description' and 'Transcription' headers.");
                                }

                                if (parser.EndOfData)
                                {
                                    throw new InvalidDataException("No data rows found.");
                                }
                                // read first row only
                                string[] row = parser.ReadFields();
                                if (row == null)
                                {
                                    throw new InvalidDataException("Failed to read the first data row.");
                                }

                                string description = SafeGet(row, idxDescription);
                                string specialty = SafeGet(row, idxSpecialty);
                                string sampleName = SafeGet(row, idxSampleName);
                                string transcription = SafeGet(row, idxTranscription);
                                string keywords = SafeGet(row, idxKeywords);

                                // map to FormTranscribe
                                _transcribe.Description = description;
                                _transcribe.Specialty = specialty;
                                _transcribe.SampleName = sampleName;
                                _transcribe.Transcription = transcription;
                                _transcribe.Keywords = keywords;

                                // if Specialty is in the ComboBox items it will select it 
                                TrySelectComboItemCaseInsensitive(_transcribe, specialty);

                                label1.Text = $"Uploaded: {Path.GetFileName(ofd.FileName)}";
                            }
                        }
                        // get errors 
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Failed to load file:\n{ex.Message}",
                                            "Error",
                                            MessageBoxButtons.OK,
                                            MessageBoxIcon.Error);
                        }
                    }
                }
            }
        }

        // =========== toggle functions for dark mode & enlarge text============
        public void ToggleTheme()
        {
            if (DownloadUpload.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                DownloadUpload.ForeColor = Color.White;
                button1.BackColor = Color.FromArgb(32, 42, 72);
                button1.ForeColor = Color.White;
                button2.BackColor = Color.FromArgb(32, 42, 72);
                button2.ForeColor = Color.White;
            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                DownloadUpload.ForeColor = Color.Black;
                button1.BackColor = Color.FromArgb(210, 232, 247);
                button1.ForeColor = Color.Black;
                button2.BackColor = Color.FromArgb(210, 232, 247);
                button2.ForeColor = Color.Black;
            }
        }

        public void ToggleEnlargeText()
        {
            if (DownloadUpload.Font.Size == 18)
            {
                DownloadUpload.Font = new Font(DownloadUpload.Font.FontFamily, 20, FontStyle.Bold);
                button1.Font = new Font(button1.Font.FontFamily, 13);
                button2.Font = new Font(button2.Font.FontFamily, 13);
                DownloadUpload.Location = new Point(275, 50);
                button1.Size = new Size(285, 70);
                button2.Size = new Size(285, 70);
            }
            else
            {
                DownloadUpload.Font = new Font(DownloadUpload.Font.FontFamily, 18, FontStyle.Bold);
                button1.Font = new Font(button1.Font.FontFamily, 10);
                button2.Font = new Font(button2.Font.FontFamily, 10);
                DownloadUpload.Location = new Point(285, 50);
                button1.Size = new Size(261, 64);
                button2.Size = new Size(261, 64);
            }
        }

        // ----------------- helpers -----------------

        // fid header index
        private static int IndexOf(string[] headers, string target)
        {
            if (headers == null) return -1;
            for (int i = 0; i < headers.Length; i++)
            {
                if (string.Equals(headers[i]?.Trim(), target, StringComparison.OrdinalIgnoreCase))
                    return i;
            }
            return -1;
        }

        // chooses best matching header
        private static int Prefer(string[] headers, params string[] candidates)
        {
            foreach (var c in candidates)
            {
                int idx = IndexOf(headers, c);
                if (idx >= 0) return idx;
            }
            return -1;
        }

        // reteieves cell text from csv
        private static string SafeGet(string[] row, int index)
        {
            if (row == null || index < 0 || index >= row.Length) return string.Empty;
            return row[index] ?? string.Empty;
        }

        // sets specialty using setter from other file
        private static void TrySelectComboItemCaseInsensitive(FormTranscribe t, string text)
        {
            if (t == null || string.IsNullOrWhiteSpace(text)) return;
            t.Specialty = text;
        }

    }
}
