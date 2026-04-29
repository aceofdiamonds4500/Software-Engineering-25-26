using Google.Cloud.Firestore;
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
            string email = emailTex.Text.Trim();
            string password = passwordTex.Text;

            var db = FirestoreHelper.Database;
            DocumentReference docRef = db.Collection("UserData").Document(email);
            Users data = docRef.GetSnapshotAsync().Result.ConvertTo<Users>();

            if (data != null)
            {
                if (password == Security.Decrypt( data.Password ))
                {
                    //MessageBox.Show("Login successful!");
                    parentForm.LoginSuccessful();
                } 
                else
                {
                    MessageBox.Show("Login Faild!");
                }
            }
            else
            {
                MessageBox.Show("Login Faild!");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            parentForm.ShowRegisterPage();
        }
    }
}
