using System;
using System.Windows.Forms;
using System.Media;

namespace GUI_SoftwareEng
{
    public partial class FormSettings : Form
    {
        private readonly Form1 _form1;
        private readonly FormDownloadUpload _formDownloadUpload;
        private SoundPlayer _soundplayer;
        public FormSettings(Form1 form1)
        {
            InitializeComponent();
            InitToggleButton(button1);
            InitToggleButton(button2);
            _form1 = form1;
            _soundplayer = new SoundPlayer("click.wav");
        }

        private void InitToggleButton(Button btn)
        {
            btn.Image = Properties.Resources.x;
            btn.Tag = "off"; 
        }

        private void button1_Click(object sender, EventArgs e)
        {
            _soundplayer.Play();
            _form1.BroadcastToggleEnlargeText();
            ToggleButtonImage(button1);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            _soundplayer.Play();
            _form1.BroadcastToggleTheme();
            ToggleButtonImage(button2);

        }

        private void ToggleButtonImage(Button btn)
        {
            if (btn.Tag?.ToString() == "off")
            {
                btn.Image = Properties.Resources.yes;
                btn.Tag = "on";
            }
            else
            {
                btn.Image = Properties.Resources.x;
                btn.Tag = "off";
            }
        }

        // =========== toggle functions for dark mode & enlarge text============
        public void ToggleTheme()
        {
            if (Settings.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                Settings.ForeColor = Color.White;
                button1.ForeColor = Color.White;
                button1.BackColor = Color.FromArgb(32, 42, 72);
                button2.ForeColor = Color.White;
                button2.BackColor = Color.FromArgb(32, 42, 72);

            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                Settings.ForeColor = Color.Black;
                button1.BackColor = Color.FromArgb(210, 232, 247);
                button1.ForeColor = Color.Black;
                button2.BackColor = Color.FromArgb(210, 232, 247);
                button2.ForeColor = Color.Black;
            }
        }

        public void ToggleEnlargeText()
        {
            if (Settings.Font.Size == 18)
            {
                Settings.Font = new Font(Settings.Font.FontFamily, 20, FontStyle.Bold);
                button1.Font = new Font(button1.Font.FontFamily, 12);
                button2.Font = new Font(button2.Font.FontFamily, 12);
                button1.Size = new Size(228, 58);
                button2.Size = new Size(228, 58);
            }
            else
            {
                Settings.Font = new Font(Settings.Font.FontFamily, 18, FontStyle.Bold);
                button1.Font = new Font(button1.Font.FontFamily, 10);
                button2.Font = new Font(button2.Font.FontFamily, 10);
                button1.Size = new Size(210, 50);
                button2.Size = new Size(210, 50);
            }
        }
    }
}
