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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormRegister));
            lable1 = new Label();
            lable2 = new Label();
            EmailRTex = new TextBox();
            PassRTex = new TextBox();
            button1 = new Button();
            label3 = new Label();
            lable3 = new Label();
            CPassRTex = new TextBox();
            label1 = new Label();
            SuspendLayout();
            // 
            // lable1
            // 
            lable1.AutoSize = true;
            lable1.Font = new Font("Microsoft Sans Serif", 11.25F);
            lable1.Location = new Point(138, 119);
            lable1.Name = "lable1";
            lable1.Size = new Size(49, 18);
            lable1.TabIndex = 0;
            lable1.Text = "Email:";
            // 
            // lable2
            // 
            lable2.AutoSize = true;
            lable2.Font = new Font("Microsoft Sans Serif", 11.25F);
            lable2.Location = new Point(108, 158);
            lable2.Name = "lable2";
            lable2.Size = new Size(79, 18);
            lable2.TabIndex = 1;
            lable2.Text = "Password:";
            // 
            // EmailRTex
            // 
            EmailRTex.Location = new Point(193, 119);
            EmailRTex.Name = "EmailRTex";
            EmailRTex.Size = new Size(140, 23);
            EmailRTex.TabIndex = 2;
            // 
            // PassRTex
            // 
            PassRTex.Location = new Point(193, 158);
            PassRTex.Name = "PassRTex";
            PassRTex.Size = new Size(140, 23);
            PassRTex.TabIndex = 3;
            PassRTex.UseSystemPasswordChar = true;
            // 
            // button1
            // 
            button1.AutoSize = true;
            button1.BackColor = Color.LightBlue;
            button1.Font = new Font("Microsoft Sans Serif", 12F);
            button1.Location = new Point(254, 235);
            button1.Name = "button1";
            button1.Size = new Size(79, 30);
            button1.TabIndex = 4;
            button1.Text = "Register";
            button1.UseVisualStyleBackColor = false;
            // 
            // label3
            // 
            label3.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
            label3.Font = new Font("Microsoft Sans Serif", 20.25F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label3.Location = new Point(12, 26);
            label3.Name = "label3";
            label3.Size = new Size(676, 52);
            label3.TabIndex = 5;
            label3.Text = "Welcome to Transcriptive AI";
            label3.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lable3
            // 
            lable3.AutoSize = true;
            lable3.Font = new Font("Microsoft Sans Serif", 11.25F);
            lable3.Location = new Point(51, 195);
            lable3.Name = "lable3";
            lable3.Size = new Size(136, 18);
            lable3.TabIndex = 8;
            lable3.Text = "Confirm Password:";
            // 
            // CPassRTex
            // 
            CPassRTex.Location = new Point(193, 195);
            CPassRTex.Name = "CPassRTex";
            CPassRTex.Size = new Size(140, 23);
            CPassRTex.TabIndex = 9;
            CPassRTex.UseSystemPasswordChar = true;
            // 
            // label1
            // 
            label1.Location = new Point(350, 90);
            label1.Name = "label1";
            label1.Size = new Size(324, 256);
            label1.TabIndex = 10;
            label1.Text = resources.GetString("label1.Text");
            // 
            // FormRegister
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(700, 355);
            Controls.Add(label1);
            Controls.Add(CPassRTex);
            Controls.Add(lable3);
            Controls.Add(label3);
            Controls.Add(button1);
            Controls.Add(PassRTex);
            Controls.Add(EmailRTex);
            Controls.Add(lable2);
            Controls.Add(lable1);
            Name = "FormRegister";
            Text = "FormRegister";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label lable1;
        private Label lable2;
        private TextBox EmailRTex;
        private TextBox PassRTex;
        private Button button1;
        private Label label3;
        private Label lable3;
        private TextBox CPassRTex;
        private Label label1;
    }
}