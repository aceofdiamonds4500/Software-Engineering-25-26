namespace GUI_SoftwareEng
{
    partial class FormLogin
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
            button1 = new Button();
            PasswordTex = new TextBox();
            EmailTex = new TextBox();
            label1 = new Label();
            label2 = new Label();
            button2 = new Button();
            SuspendLayout();
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(192, 192, 255);
            button1.Font = new Font("Microsoft Sans Serif", 12F);
            button1.Location = new Point(246, 198);
            button1.Name = "button1";
            button1.Size = new Size(84, 34);
            button1.TabIndex = 0;
            button1.Text = "Login";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // PasswordTex
            // 
            PasswordTex.Location = new Point(321, 157);
            PasswordTex.Name = "PasswordTex";
            PasswordTex.Size = new Size(149, 23);
            PasswordTex.TabIndex = 1;
            PasswordTex.UseSystemPasswordChar = true;
            // 
            // EmailTex
            // 
            EmailTex.Location = new Point(321, 96);
            EmailTex.Name = "EmailTex";
            EmailTex.Size = new Size(149, 23);
            EmailTex.TabIndex = 2;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 12F);
            label1.Location = new Point(254, 96);
            label1.Name = "label1";
            label1.Size = new Size(52, 20);
            label1.TabIndex = 3;
            label1.Text = "Email:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Microsoft Sans Serif", 12F);
            label2.Location = new Point(224, 159);
            label2.Name = "label2";
            label2.Size = new Size(82, 20);
            label2.TabIndex = 4;
            label2.Text = "Password:";
            // 
            // button2
            // 
            button2.BackColor = Color.FromArgb(192, 192, 255);
            button2.Font = new Font("Microsoft Sans Serif", 12F);
            button2.Location = new Point(355, 198);
            button2.Name = "button2";
            button2.Size = new Size(84, 34);
            button2.TabIndex = 5;
            button2.Text = "Register";
            button2.UseVisualStyleBackColor = false;
            // 
            // FormLogin
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(700, 338);
            Controls.Add(button2);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(EmailTex);
            Controls.Add(PasswordTex);
            Controls.Add(button1);
            Name = "FormLogin";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private TextBox PasswordTex;
        private TextBox EmailTex;
        private Label label1;
        private Label label2;
        private Button button2;
    }
}