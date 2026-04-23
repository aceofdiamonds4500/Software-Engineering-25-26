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
        private Form1 parentForm;
        public FormLogin(Form1 parent)
        {
            InitializeComponent();
            parentForm = parent;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string email = EmailTex.Text;
            string password = PasswordTex.Text;

            if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(password))
            {
                MessageBox.Show("Please enter email and password.");
                return;
            }

            if (email == "admin" && password == "admin")
            {
                //MessageBox.Show("Login successful!");
                parentForm.LoginSuccessful();
            }
            else
            {
                MessageBox.Show("Invalid email or password.");
                return;
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            parentForm.ShowRegisterPage();
        }
    }
}
