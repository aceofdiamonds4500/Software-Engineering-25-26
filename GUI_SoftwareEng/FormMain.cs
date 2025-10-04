using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GUI_SoftwareEng
{
    public partial class FormMain : Form
    {
        public FormMain()
        {
            InitializeComponent();
        }

        public void ToggleTheme()
        {
            if (Welcome.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                Welcome.ForeColor = Color.White;
                label1.ForeColor = Color.White;
            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                Welcome.ForeColor = Color.Black;
                label1.ForeColor = Color.Black;
            }
        }
    }
}
