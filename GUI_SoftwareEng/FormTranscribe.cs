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

namespace GUI_SoftwareEng
{
    public partial class FormTranscribe : Form
    {
        private SoundPlayer _soundplayer;
        public FormTranscribe()
        {
            InitializeComponent();
            _soundplayer = new SoundPlayer("click.wav");
        }

        // transcription button
        private void button1_Click(object sender, EventArgs e)
        {
            _soundplayer.Play();
        }

        // setters & getters for textboxes 
        public string Description {get => richTextBox1.Text; set => richTextBox1.Text = value;}
        public string SampleName {get => richTextBox2.Text; set => richTextBox2.Text = value;}
        public string Transcription {get => richTextBox3.Text; set => richTextBox3.Text = value;}
        public string Keywords {get => richTextBox4.Text; set => richTextBox4.Text = value;}
        public string OutputTranscription {get => richTextBox5.Text; set => richTextBox5.Text = value;}
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

        // =========== toggle functions for dark mode & enlarge text============
        public void ToggleTheme()
        {
            if (Transcribe.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                label1.ForeColor = Color.White;
                label2.ForeColor = Color.White;
                Transcribe.ForeColor = Color.White;
                button1.BackColor = Color.FromArgb(32, 42, 72);
                button1.ForeColor = Color.White;
            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                label1.ForeColor = Color.Black;
                label2.ForeColor = Color.Black;
                Transcribe.ForeColor = Color.Black;
                richTextBox1.BackColor = Color.White;
                button1.BackColor = Color.FromArgb(210, 232, 247);
                button1.ForeColor = Color.Black;
            }
        }
        public void ToggleEnlargeText()
        {
            if (Transcribe.Font.Size == 18)
            {
                Transcribe.Font = new Font(Transcribe.Font.FontFamily, 20, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 13);
                label2.Font = new Font(label2.Font.FontFamily, 13);
                button1.Font = new Font(button1.Font.FontFamily, 12);
                button1.Size = new Size(265, 70);
                button1.Location = new Point(290, 200);
            }
            else
            {
                Transcribe.Font = new Font(Transcribe.Font.FontFamily, 18, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 10);
                label2.Font = new Font(label2.Font.FontFamily, 10);
                button1.Font = new Font(button1.Font.FontFamily, 10);
            }
        }
    }
}
