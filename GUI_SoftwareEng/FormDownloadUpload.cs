using System;
using System.IO;
using System.Security.Cryptography;
using System.Windows.Forms;

namespace GUI_SoftwareEng
{

    public partial class FormDownloadUpload : Form
    {
        private readonly FormTranscribe _transcribe;
        public string uploadedTxtPath = string.Empty;

        public FormDownloadUpload(FormTranscribe transcribe)
        {
            InitializeComponent();
            _transcribe = transcribe;
        }

        // save transcription to a txt file
        private void button1_Click(object sender, EventArgs e)
        {
            // Safety: make sure we can read text
            if (_transcribe == null)
            {
                label1.Text = "Error: transcribe page not available.";
                return;
            }

            string textToSave = _transcribe.OutputText ?? string.Empty;

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
                    sfd.Filter = "Text Files (*.txt)|*.txt";
                    sfd.DefaultExt = "txt";
                    sfd.FileName = "transcription.txt";

                    var result = sfd.ShowDialog(this);
                    if (result != DialogResult.OK)
                    {
                        label1.Text = "Save canceled.";
                        return;
                    }

                    File.WriteAllText(sfd.FileName, textToSave);
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
            {
                using (var ofd = new OpenFileDialog())
                {
                    ofd.Title = "Select a transcription (.txt)";
                    ofd.Filter = "Text Files (*.txt)|*.txt";
                    ofd.FilterIndex = 1;
                    ofd.Multiselect = false;

                    if (ofd.ShowDialog(this) == DialogResult.OK)
                    {
                        try
                        {
                            string text = File.ReadAllText(ofd.FileName);
                            _transcribe.InputText = text;
                            label1.Text = $"Uploaded: {Path.GetFileName(ofd.FileName)}";
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
    }
}
