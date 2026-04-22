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
            button2 = new Button();
            label1 = new Label();
            label2 = new Label();
            EmailTex = new TextBox();
            PasswordTex = new TextBox();
            button3 = new Button();
            SuspendLayout();
            // 
            // button1
            // 
            button1.AutoSize = true;
            button1.BackColor = Color.LightBlue;
            button1.Font = new Font("Microsoft Sans Serif", 12F);
            button1.Location = new Point(229, 216);
            button1.Name = "button1";
            button1.Size = new Size(75, 30);
            button1.TabIndex = 0;
            button1.Text = "Login";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.AutoSize = true;
            button2.BackColor = Color.LightBlue;
            button2.Font = new Font("Microsoft Sans Serif", 12F);
            button2.Location = new Point(350, 216);
            button2.Name = "button2";
            button2.Size = new Size(79, 30);
            button2.TabIndex = 1;
            button2.Text = "Register";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button2_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 11.25F);
            label1.Location = new Point(220, 105);
            label1.Name = "label1";
            label1.Size = new Size(49, 18);
            label1.TabIndex = 2;
            label1.Text = "Email:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Microsoft Sans Serif", 11.25F);
            label2.Location = new Point(190, 157);
            label2.Name = "label2";
            label2.Size = new Size(79, 18);
            label2.TabIndex = 3;
            label2.Text = "Password:";
            // 
            // EmailTex
            // 
            EmailTex.Location = new Point(275, 105);
            EmailTex.Name = "EmailTex";
            EmailTex.Size = new Size(154, 23);
            EmailTex.TabIndex = 4;
            // 
            // PasswordTex
            // 
            PasswordTex.Location = new Point(275, 157);
            PasswordTex.Name = "PasswordTex";
            PasswordTex.Size = new Size(154, 23);
            PasswordTex.TabIndex = 5;
            PasswordTex.UseSystemPasswordChar = true;
            // 
            // button3
            // 
            button3.BackColor = Color.Transparent;
            button3.BackgroundImageLayout = ImageLayout.None;
            button3.CausesValidation = false;
            button3.FlatAppearance.BorderColor = Color.FromArgb(220, 224, 228);
            button3.Font = new Font("Microsoft Sans Serif", 9F, FontStyle.Italic | FontStyle.Underline, GraphicsUnit.Point, 0);
            button3.ForeColor = SystemColors.Highlight;
            button3.Location = new Point(435, 157);
            button3.Name = "button3";
            button3.Size = new Size(114, 23);
            button3.TabIndex = 6;
            button3.Text = "Forgot Password?";
            button3.UseCompatibleTextRendering = true;
            button3.UseVisualStyleBackColor = false;
            // 
            // FormLogin
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            AutoSize = true;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(700, 355);
            Controls.Add(button3);
            Controls.Add(PasswordTex);
            Controls.Add(EmailTex);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(button2);
            Controls.Add(button1);
            Name = "FormLogin";
            Text = "FormLogin";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private Button button2;
        private Label label1;
        private Label label2;
        private TextBox EmailTex;
        private TextBox PasswordTex;
        private Button button3;
    }
}