namespace GUI_SoftwareEng
{
    partial class FormTranscribe
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
            Transcribe = new ReaLTaiizor.Controls.BigLabel();
            richTextBox1 = new RichTextBox();
            label1 = new Label();
            button1 = new Button();
            richTextBox2 = new RichTextBox();
            label2 = new Label();
            SuspendLayout();
            // 
            // Transcribe
            // 
            Transcribe.AutoSize = true;
            Transcribe.BackColor = Color.Transparent;
            Transcribe.Font = new Font("Segoe UI", 25.2F, FontStyle.Bold, GraphicsUnit.Point, 0);
            Transcribe.ForeColor = Color.Black;
            Transcribe.Location = new Point(305, 80);
            Transcribe.Name = "Transcribe";
            Transcribe.Size = new Size(228, 57);
            Transcribe.TabIndex = 11;
            Transcribe.Text = "Transcribe";
            Transcribe.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // richTextBox1
            // 
            richTextBox1.Location = new Point(65, 150);
            richTextBox1.Name = "richTextBox1";
            richTextBox1.Size = new Size(213, 227);
            richTextBox1.TabIndex = 12;
            richTextBox1.Text = "";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 10F);
            label1.Location = new Point(65, 110);
            label1.Name = "label1";
            label1.Size = new Size(174, 20);
            label1.TabIndex = 14;
            label1.Text = "Enter Patient Details: ";
            label1.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(210, 232, 247);
            button1.Font = new Font("Microsoft Sans Serif", 10F);
            button1.Image = Properties.Resources.Speech_Bubble;
            button1.ImageAlign = ContentAlignment.MiddleLeft;
            button1.Location = new Point(305, 200);
            button1.Name = "button1";
            button1.Padding = new Padding(10, 0, 0, 0);
            button1.Size = new Size(228, 58);
            button1.TabIndex = 15;
            button1.Text = "Calculate Information";
            button1.UseVisualStyleBackColor = false;
            // 
            // richTextBox2
            // 
            richTextBox2.Location = new Point(565, 150);
            richTextBox2.Name = "richTextBox2";
            richTextBox2.ReadOnly = true;
            richTextBox2.Size = new Size(213, 227);
            richTextBox2.TabIndex = 16;
            richTextBox2.Text = "";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Microsoft Sans Serif", 10F);
            label2.Location = new Point(565, 110);
            label2.Name = "label2";
            label2.Size = new Size(76, 20);
            label2.TabIndex = 17;
            label2.Text = "Results: ";
            label2.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // FormTranscribe
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(800, 450);
            Controls.Add(label2);
            Controls.Add(richTextBox2);
            Controls.Add(button1);
            Controls.Add(label1);
            Controls.Add(richTextBox1);
            Controls.Add(Transcribe);
            Name = "FormTranscribe";
            Text = "FormTranscribe";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private ReaLTaiizor.Controls.BigLabel Transcribe;
        private RichTextBox richTextBox1;
        private Label label1;
        private Button button1;
        private RichTextBox richTextBox2;
        private Label label2;
    }
}