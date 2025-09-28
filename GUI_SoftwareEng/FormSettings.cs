using System;
using System.Windows.Forms;

namespace GUI_SoftwareEng
{
    public partial class FormSettings : Form
    {
        public FormSettings()
        {
            InitializeComponent();
            InitToggleButton(button1);
            InitToggleButton(button2);
        }

        private void InitToggleButton(Button btn)
        {
            btn.Image = Properties.Resources.x;
            btn.Tag = "off"; 
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ToggleButtonImage(button1);
        }

        private void button2_Click(object sender, EventArgs e)
        {
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
    }
}
