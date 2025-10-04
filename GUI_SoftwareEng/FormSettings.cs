using System;
using System.Windows.Forms;

namespace GUI_SoftwareEng
{
    public partial class FormSettings : Form
    {
        private readonly Form1 _form1;
        private readonly FormDownloadUpload _formDownloadUpload;
        public FormSettings(Form1 form1)
        {
            InitializeComponent();
            InitToggleButton(button1);
            InitToggleButton(button2);
            _form1 = form1;
        }

        private void InitToggleButton(Button btn)
        {
            btn.Image = Properties.Resources.x;
            btn.Tag = "off"; 
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ToggleEnlargeText(button1);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            ToggleDarkMode(button2);

        }

        private void ToggleEnlargeText(Button btn)
        {
            // This method can be expanded to actually toggle dark mode settings
            
            ToggleButtonImage(btn);
        }

        private void ToggleDarkMode(Button btn)
        {
            // This method can be expanded to actually toggle dark mode settings
            _form1.BroadcastToggleTheme();
            ToggleButtonImage(btn);
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
    }
}
