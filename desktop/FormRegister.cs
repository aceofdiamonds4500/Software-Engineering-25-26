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
using static System.Net.Mime.MediaTypeNames;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace GUI_SoftwareEng
{
    public partial class FormRegister : Form
    {
        private Form1 parentForm;
        public FormRegister(Form1 parent)
        {
            InitializeComponent();
            parentForm = parent;
        }

        private Users GetWriteData()
        {
            string email = emailTex.Text.Trim();
            string password = Security.Encrypt(passwordTex.Text);
            string confirmPassword = Security.Encrypt(confirmPasswordTex.Text);

            return new Users()
            {
                Email = email,
                Password = password,
                ConfirmPassword = confirmPassword
            };
        }

        private bool CheckIfUserAlreadyExists()
        {
            string email = emailTex.Text.Trim();

            var db = FirestoreHelper.Database;
            DocumentReference docRef = db.Collection("UserData").Document(email);
            Users data = docRef.GetSnapshotAsync().Result.ConvertTo<Users>();

            if (data != null)
            {
                return true;
            }
            return false;
        }

        private void Register2_Click(object sender, EventArgs e)
        {
            if (CheckIfUserAlreadyExists())
            {
                MessageBox.Show("User already exists!");
                return;
            }

            var db = FirestoreHelper.Database;
            var data = GetWriteData();
            DocumentReference docRef = db.Collection("UserData").Document(data.Email);
            docRef.SetAsync(data);
            MessageBox.Show("Registration successful!");

            parentForm.ShowLoginPage();
        }
        private void ButTermsOfService(object sender, EventArgs e)
        {
            MessageBox.Show("The application does not provide medical, legal, or professional advice, and all generated " +
                    "content must be independently reviewed by a qualified professional. To the fullest extent" +
                    " permitted by law, the developers shall not be liable for any damages arising from the use " +
                    "or misuse of this application, including but not limited to financial loss, data loss, bodily " +
                    "injury, permanent disability, loss of limbs, or death. Users acknowledge that information ente" +
                    "red into the application may not be secure and could potentially be accessed, intercepted, " +
                    "or disclosed by unauthorized third parties, including hostile actors or foreign entities. " +
                    "The creation of an account in Transcription AI app constitutes to acceptance of these terms.");
        }

        private void butBackToLogin_Click(object sender, EventArgs e)
        {
            parentForm.ShowLoginPage();
        }
    }
}
