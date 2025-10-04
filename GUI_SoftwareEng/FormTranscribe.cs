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
    public partial class FormTranscribe : Form
    {
        public FormTranscribe()
        {
            InitializeComponent();
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

        public void ToggleTheme()
        {
            BackColor = Color.FromArgb(24, 30, 54);
        }
    }
}
