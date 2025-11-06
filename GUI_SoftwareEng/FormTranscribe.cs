using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Media;
using System.Linq.Expressions;
using System.IO;
using System.Diagnostics;
using System.Collections;


namespace GUI_SoftwareEng
{
    public partial class FormTranscribe : Form
    {
        private SoundPlayer _soundplayer;

        // Declare tooltip at the class level
        private ToolTip hoverTip;

        public FormTranscribe()
        {
            InitializeComponent();
            _soundplayer = new SoundPlayer("click.wav");

            // Initialize the tooltip 
            hoverTip = new ToolTip();
            hoverTip.AutoPopDelay = 8000;
            hoverTip.InitialDelay = 500;
            hoverTip.ReshowDelay = 200;
            hoverTip.ShowAlways = true;

            // Attach tooltip text to the pictureBox1 img for hover
            hoverTip.SetToolTip(pictureBox1,
            "Description: Brief summary of the recording.  \nExample: 'Cardiology exam for chest pain'\n\n" +
            "Specialty: Medical field related to the note.  \nExample: 'Cardiology'\n\n" +
            "Sample Name: Custom label for this file.  \nExample: 'HeartEcho_01'\n\n" +
            "Transcription: The main medical text.  \nExample: 'Patient presents with irregular heartbeat...'\n\n" +
            "Keywords: Tags for quick search.  \nExample: 'ECG, arrhythmia, chest pain'");
        }

        // transcription button
        private void button1_Click(object sender, EventArgs e)
        {
            _soundplayer.Play(); // ding ding ding ding ding ding ding

            try
            {
                // get data from ALL OF THE TEXGTBOXES
                string description = Description?.Trim() ?? "";
                string sampleName = SampleName?.Trim() ?? "";
                string transcription = Transcription?.Trim() ?? "";
                string keywords = Keywords?.Trim() ?? "";
                string specialty = Specialty?.Trim() ?? "";

                // Manually build to json file
                string json = "{\n" +
                    $"  \"version\": \"1.0\",\n" +
                    $"  \"source\": \"FormTranscribe\",\n" +
                    $"  \"timestamp\": \"{DateTime.UtcNow:yyyy-MM-ddTHH:mm:ssZ}\",\n" +
                    "  \"fields\": {\n" +
                    $"    \"Description\": \"{EscapeJson(description)}\",\n" +
                    $"    \"SampleName\": \"{EscapeJson(sampleName)}\",\n" +
                    $"    \"Transcription\": \"{EscapeJson(transcription)}\",\n" +
                    $"    \"Keywords\": \"{EscapeJson(keywords)}\",\n" +
                    $"    \"Specialty\": \"{EscapeJson(specialty)}\"\n" +
                    "  }\n" +
                    "}";

                // Save to file
                string folder = AppDomain.CurrentDomain.BaseDirectory;
                string fileName = $"payload-{DateTime.Now:yyyyMMdd_HHmmss}.json";
                string filePath = Path.Combine(folder, fileName);

                File.WriteAllText(filePath, json, Encoding.UTF8);

                MessageBox.Show($"JSON exported successfully:\n{filePath}",
                    "Export Complete", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to export JSON:\n" + ex.Message,
                    "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // setters & getters for textboxes 
        public string Description { get => richTextBox1.Text; set => richTextBox1.Text = value; }
        public string SampleName { get => richTextBox2.Text; set => richTextBox2.Text = value; }
        public string Transcription { get => richTextBox3.Text; set => richTextBox3.Text = value; }
        public string Keywords { get => richTextBox4.Text; set => richTextBox4.Text = value; }
        public string OutputTranscription { get => richTextBox5.Text; set => richTextBox5.Text = value; }
        public string Specialty
        {
            get => comboBox1.Text;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                {
                    comboBox1.SelectedIndex = -1;
                    comboBox1.Text = string.Empty;
                    return;
                }

                int matchIndex = -1;
                for (int i = 0; i < comboBox1.Items.Count; i++)
                {
                    var itemText = comboBox1.Items[i]?.ToString();
                    if (string.Equals(itemText, value, StringComparison.OrdinalIgnoreCase))
                    {
                        matchIndex = i;
                        break;
                    }
                }
                if (matchIndex >= 0)
                {
                    comboBox1.SelectedIndex = matchIndex;
                }
                else
                    comboBox1.Text = value;
            }
        }

        // =========== toggle functions for dark mode & enlarge text ============
        public void ToggleTheme()
        {
            if (Transcribe.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                label1.ForeColor = Color.White;
                label2.ForeColor = Color.White;
                label3.ForeColor = Color.White;
                label4.ForeColor = Color.White;
                label5.ForeColor = Color.White;
                label6.ForeColor = Color.White;
                Transcribe.ForeColor = Color.White;
                button1.BackColor = Color.FromArgb(32, 42, 72);
                button1.ForeColor = Color.White;
                button2.BackColor = Color.FromArgb(32, 42, 72);
                button2.ForeColor = Color.White;
            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                label1.ForeColor = Color.Black;
                label2.ForeColor = Color.Black;
                label3.ForeColor = Color.Black;
                label4.ForeColor = Color.Black;
                label5.ForeColor = Color.Black;
                label6.ForeColor = Color.Black;
                Transcribe.ForeColor = Color.Black;
                richTextBox1.BackColor = Color.White;
                button1.BackColor = Color.FromArgb(210, 232, 247);
                button1.ForeColor = Color.Black;
                button2.BackColor = Color.FromArgb(210, 232, 247);
                button2.ForeColor = Color.Black;
            }
        }
        public void ToggleEnlargeText()
        {
            if (Transcribe.Font.Size == 18)
            {
                Transcribe.Font = new Font(Transcribe.Font.FontFamily, 20, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 13);
                label2.Font = new Font(label2.Font.FontFamily, 13);
                label3.Font = new Font(label3.Font.FontFamily, 13);
                label4.Font = new Font(label4.Font.FontFamily, 13);
                label5.Font = new Font(label5.Font.FontFamily, 13);
                label6.Font = new Font(label6.Font.FontFamily, 13);
                button1.Font = new Font(button1.Font.FontFamily, 12);
                button2.Font = new Font(button1.Font.FontFamily, 12);
                label5.Location = new Point(label5.Location.X, 75);
                label4.Location = new Point(label4.Location.X, 139);
                label1.Location = new Point(label1.Location.X, 206);
                label6.Location = new Point(label6.Location.X, 312);
                label3.Location = new Point(label3.Location.X, 419);
                label2.Location = new Point(label2.Location.X, 75);
            }
            else
            {
                Transcribe.Font = new Font(Transcribe.Font.FontFamily, 18, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 10);
                label2.Font = new Font(label2.Font.FontFamily, 10);
                label3.Font = new Font(label3.Font.FontFamily, 10);
                label4.Font = new Font(label4.Font.FontFamily, 10);
                label5.Font = new Font(label5.Font.FontFamily, 10);
                label6.Font = new Font(label6.Font.FontFamily, 10);
                button1.Font = new Font(button1.Font.FontFamily, 10);
                button2.Font = new Font(button1.Font.FontFamily, 10);
                label5.Location = new Point(label5.Location.X, 83);
                label4.Location = new Point(label4.Location.X, 145);
                label1.Location = new Point(label1.Location.X, 211);
                label6.Location = new Point(label6.Location.X, 317);
                label3.Location = new Point(label3.Location.X, 424);
                label2.Location = new Point(label2.Location.X, 83);
            }
        }

        // =========== helper func for json ============
        private static string EscapeJson(string s)
        {
            if (string.IsNullOrEmpty(s)) return "";
            StringBuilder sb = new StringBuilder();
            foreach (char c in s)
            {
                switch (c)
                {
                    case '\\': sb.Append(@"\\"); break;
                    case '\"': sb.Append("\\\""); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default:
                        if (c < 32)
                            sb.Append("\\u" + ((int)c).ToString("x4"));
                        else
                            sb.Append(c);
                        break;
                }
            }
            return sb.ToString();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            richTextBox1.Text = "";
            richTextBox2.Text = "";
            richTextBox3.Text = "";
            richTextBox4.Text = "";
            richTextBox5.Text = "";
            comboBox1.SelectedIndex = -1;
        }
    }
}
