using System;
using System.IO;
using System.Security.Cryptography;
using System.Windows.Forms;
using System.Media;

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
            _transcribe = transcribe;
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
            _soundplayer.Play();
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
                button1.Size = new Size(285, 70);
                button2.Size = new Size(285, 70);
            }
            else
            {
                DownloadUpload.Font = new Font(DownloadUpload.Font.FontFamily, 18, FontStyle.Bold);
                button1.Font = new Font(button1.Font.FontFamily, 10);
                button2.Font = new Font(button2.Font.FontFamily, 10);
                button1.Size = new Size(261, 64);
                button2.Size = new Size(261, 64);
            }
        }
    }
}
