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
    public partial class FormHistory : Form
    {
        public FormHistory()
        {
            InitializeComponent();
        }








        // =========== toggle functions for dark mode & enlarge text============
        public void ToggleTheme()
        {
            if (History.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                History.ForeColor = Color.White;
            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                History.ForeColor = Color.Black;
            }
            
        }

        public void ToggleEnlargeText()
        {
            if (History.Font.Size == 18)
            {
                History.Font = new Font(History.Font.FontFamily, 25, FontStyle.Bold);
                History.Location = new Point(355, 65);
            }
            else
            {
                History.Font = new Font(History.Font.FontFamily, 18, FontStyle.Bold);
                History.Location = new Point(365, 65);
            }
        }
    }
}
