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
    public partial class FormLogin : Form
    {
        public FormLogin()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            String Email = EmailTex.Text;
            String Password = PasswordTex.Text;
            if (Email == "admin" && Password == "admin")
            {
                MessageBox.Show("Login successful!");
            }
            else
            {
                MessageBox.Show("Login failed!");
            }
        }
    }
}
