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
            label1 = new Label();
            label2 = new Label();
            textBox1 = new TextBox();
            textBox2 = new TextBox();
            textBox3 = new TextBox();
            label3 = new Label();
            label4 = new Label();
            button2 = new Button();
            SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.BackColor = Color.FromArgb(220, 224, 228);
            label1.Font = new Font("Microsoft Sans Serif", 11.25F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label1.Location = new Point(253, 135);
            label1.Name = "label1";
            label1.Size = new Size(49, 18);
            label1.TabIndex = 1;
            label1.Text = "Email:";
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
            // textBox1
            // 
            textBox1.Location = new Point(308, 130);
            textBox1.Name = "textBox1";
            textBox1.Size = new Size(149, 23);
            textBox1.TabIndex = 3;
            // 
            // textBox2
            // 
            textBox2.Location = new Point(308, 157);
            textBox2.Name = "textBox2";
            textBox2.Size = new Size(149, 23);
            textBox2.TabIndex = 4;
            textBox2.UseSystemPasswordChar = true;
            // 
            // textBox3
            // 
            textBox3.Location = new Point(308, 186);
            textBox3.Name = "textBox3";
            textBox3.Size = new Size(149, 23);
            textBox3.TabIndex = 5;
            textBox3.UseSystemPasswordChar = true;
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
            // button2
            // 
            button2.BackColor = Color.FromArgb(192, 192, 255);
            button2.Font = new Font("Microsoft Sans Serif", 12F);
            button2.Location = new Point(373, 225);
            button2.Name = "button2";
            button2.Size = new Size(84, 34);
            button2.TabIndex = 8;
            button2.Text = "Register";
            button2.UseVisualStyleBackColor = false;
            // 
            // FormRegister
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(700, 338);
            Controls.Add(button2);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(textBox3);
            Controls.Add(textBox2);
            Controls.Add(textBox1);
            Controls.Add(label2);
            Controls.Add(label1);
            Name = "FormRegister";
            Text = "FormRegister";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private Label label1;
        private Label label2;
        private TextBox textBox1;
        private TextBox textBox2;
        private TextBox textBox3;
        private Label label3;
        private Label label4;
        private Button button2;
    }
}