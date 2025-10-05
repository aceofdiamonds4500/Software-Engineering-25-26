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
        public string InputText
        {
            get => richTextBox1.Text;
            set => richTextBox1.Text = value;
        }
        public string OutputText
        {
            get => richTextBox2.Text;
            set => richTextBox2.Text = value;
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
