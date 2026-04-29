namespace GUI_SoftwareEng
{
    partial class FormRegister
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            lable1 = new Label();
            label2 = new Label();
            emailTex = new TextBox();
            passwordTex = new TextBox();
            confirmPasswordTex = new TextBox();
            label3 = new Label();
            label4 = new Label();
            ButTermsOfServic = new Button();
            Register2 = new Button();
            butBackToLogin = new Button();
            SuspendLayout();
            // 
            // lable1
            // 
            lable1.AutoSize = true;
            lable1.BackColor = Color.FromArgb(220, 224, 228);
            lable1.Font = new Font("Microsoft Sans Serif", 11.25F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lable1.Location = new Point(253, 135);
            lable1.Name = "lable1";
            lable1.Size = new Size(49, 18);
            lable1.TabIndex = 1;
            lable1.Text = "Email:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Microsoft Sans Serif", 11.25F);
            label2.Location = new Point(226, 162);
            label2.Name = "label2";
            label2.Size = new Size(79, 18);
            label2.TabIndex = 2;
            label2.Text = "Password:";
            // 
            // emailTex
            // 
            emailTex.Location = new Point(308, 130);
            emailTex.Name = "emailTex";
            emailTex.Size = new Size(149, 23);
            emailTex.TabIndex = 3;
            // 
            // passwordTex
            // 
            passwordTex.Location = new Point(308, 157);
            passwordTex.Name = "passwordTex";
            passwordTex.PasswordChar = '*';
            passwordTex.Size = new Size(149, 23);
            passwordTex.TabIndex = 4;
            passwordTex.UseSystemPasswordChar = true;
            // 
            // confirmPasswordTex
            // 
            confirmPasswordTex.Location = new Point(308, 186);
            confirmPasswordTex.Name = "confirmPasswordTex";
            confirmPasswordTex.PasswordChar = '*';
            confirmPasswordTex.Size = new Size(149, 23);
            confirmPasswordTex.TabIndex = 5;
            confirmPasswordTex.UseSystemPasswordChar = true;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Font = new Font("Microsoft Sans Serif", 11.25F);
            label3.Location = new Point(166, 191);
            label3.Name = "label3";
            label3.Size = new Size(136, 18);
            label3.TabIndex = 6;
            label3.Text = "Confirm Password:";
            // 
            // label4
            // 
            label4.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
            label4.Font = new Font("Microsoft Sans Serif", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label4.Location = new Point(12, 53);
            label4.Name = "label4";
            label4.Size = new Size(676, 57);
            label4.TabIndex = 7;
            label4.Text = "Welcome to Transcriptive AI";
            label4.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // ButTermsOfServic
            // 
            ButTermsOfServic.AutoSize = true;
            ButTermsOfServic.BackColor = Color.Transparent;
            ButTermsOfServic.FlatAppearance.BorderSize = 0;
            ButTermsOfServic.Font = new Font("Microsoft Sans Serif", 9.75F, FontStyle.Italic | FontStyle.Underline, GraphicsUnit.Point, 0);
            ButTermsOfServic.ForeColor = Color.DodgerBlue;
            ButTermsOfServic.Location = new Point(463, 182);
            ButTermsOfServic.Name = "ButTermsOfServic";
            ButTermsOfServic.Size = new Size(128, 28);
            ButTermsOfServic.TabIndex = 9;
            ButTermsOfServic.Text = "Terms of Service";
            ButTermsOfServic.UseVisualStyleBackColor = false;
            ButTermsOfServic.Click += ButTermsOfService;
            // 
            // Register2
            // 
            Register2.BackColor = Color.FromArgb(192, 192, 255);
            Register2.Font = new Font("Microsoft Sans Serif", 12F);
            Register2.Location = new Point(373, 225);
            Register2.Name = "Register2";
            Register2.Size = new Size(84, 34);
            Register2.TabIndex = 10;
            Register2.Text = "Register";
            Register2.UseVisualStyleBackColor = false;
            Register2.Click += Register2_Click;
            // 
            // butBackToLogin
            // 
            butBackToLogin.BackColor = Color.FromArgb(192, 192, 255);
            butBackToLogin.Font = new Font("Microsoft Sans Serif", 12F);
            butBackToLogin.Location = new Point(226, 225);
            butBackToLogin.Name = "butBackToLogin";
            butBackToLogin.Size = new Size(123, 34);
            butBackToLogin.TabIndex = 11;
            butBackToLogin.Text = "Back to Login";
            butBackToLogin.UseVisualStyleBackColor = false;
            butBackToLogin.Click += butBackToLogin_Click;
            // 
            // FormRegister
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(700, 338);
            Controls.Add(butBackToLogin);
            Controls.Add(Register2);
            Controls.Add(ButTermsOfServic);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(confirmPasswordTex);
            Controls.Add(passwordTex);
            Controls.Add(emailTex);
            Controls.Add(label2);
            Controls.Add(lable1);
            Name = "FormRegister";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "FormRegister";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private Label lable1;
        private Label label2;
        private TextBox emailTex;
        private TextBox passwordTex;
        private TextBox confirmPasswordTex;
        private Label label3;
        private Label label4;
        private Button ButTermsOfServic;
        private Button Register2;
        private Button butBackToLogin;
    }
}