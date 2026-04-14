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
            comboBox1 = new ComboBox();
            richTextBox3 = new RichTextBox();
            label3 = new Label();
            label4 = new Label();
            label5 = new Label();
            richTextBox4 = new RichTextBox();
            label6 = new Label();
            richTextBox5 = new RichTextBox();
            pictureBox1 = new PictureBox();
            button2 = new Button();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
            SuspendLayout();
            // 
            // Transcribe
            // 
            Transcribe.AutoSize = true;
            Transcribe.BackColor = Color.Transparent;
            Transcribe.Font = new Font("Segoe UI", 18F, FontStyle.Bold);
            Transcribe.ForeColor = Color.Black;
            Transcribe.Location = new Point(302, 38);
            Transcribe.Name = "Transcribe";
            Transcribe.Size = new Size(132, 32);
            Transcribe.TabIndex = 11;
            Transcribe.Text = "Transcribe";
            Transcribe.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // richTextBox1
            // 
            richTextBox1.Location = new Point(53, 255);
            richTextBox1.Margin = new Padding(3, 2, 3, 2);
            richTextBox1.Name = "richTextBox1";
            richTextBox1.Size = new Size(217, 54);
            richTextBox1.TabIndex = 12;
            richTextBox1.Text = "";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 10F);
            label1.Location = new Point(53, 158);
            label1.Name = "label1";
            label1.Size = new Size(95, 17);
            label1.TabIndex = 14;
            label1.Text = "Transcription:";
            label1.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(210, 232, 247);
            button1.Font = new Font("Microsoft Sans Serif", 10F);
            button1.ImageAlign = ContentAlignment.MiddleLeft;
            button1.Location = new Point(451, 335);
            button1.Margin = new Padding(3, 2, 3, 2);
            button1.Name = "button1";
            button1.Padding = new Padding(9, 0, 0, 0);
            button1.Size = new Size(223, 44);
            button1.TabIndex = 15;
            button1.Text = "Calculate Info";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // richTextBox2
            // 
            richTextBox2.HideSelection = false;
            richTextBox2.Location = new Point(53, 80);
            richTextBox2.Margin = new Padding(3, 2, 3, 2);
            richTextBox2.Name = "richTextBox2";
            richTextBox2.Size = new Size(217, 22);
            richTextBox2.TabIndex = 16;
            richTextBox2.Text = "";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Microsoft Sans Serif", 10F);
            label2.Location = new Point(489, 62);
            label2.Name = "label2";
            label2.Size = new Size(63, 17);
            label2.TabIndex = 17;
            label2.Text = "Results: ";
            label2.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // comboBox1
            // 
            comboBox1.FormattingEnabled = true;
            comboBox1.Items.AddRange(new object[] { "Allergy / Immunology", "Bariatrics", "Cardiovascular / Pulmonary", "Chiropractic", "Consult - History and Phy.", "Cosmetic / Plastic Surgery", "Dentistry", "Dermatology", "Dietetics / Nutrition", "Discharge Summary", "Emergency Room Reports", "Endocrinology", "ENT - Otolaryngology", "Family Medicine", "Gastroenterology", "General Medicine", "Hematology - Oncology", "Infectious Disease", "Internal Medicine", "Lab Medicine - Pathology", "Letters", "Nephrology", "Neurology", "Neurosurgery", "Obstetrics / Gynecology", "Office Notes", "Ophthalmology", "Orthopedic", "Pain Management", "Pediatrics - Neonatal", "Physical Medicine - Rehab", "Podiatry", "Psychiatry / Psychology", "Radiology", "Rheumatology", "Sleep Medicine", "Speech - Language", "Surgery", "Urology" });
            comboBox1.Location = new Point(53, 126);
            comboBox1.Margin = new Padding(3, 2, 3, 2);
            comboBox1.Name = "comboBox1";
            comboBox1.Size = new Size(217, 23);
            comboBox1.TabIndex = 18;
            // 
            // richTextBox3
            // 
            richTextBox3.Location = new Point(53, 176);
            richTextBox3.Margin = new Padding(3, 2, 3, 2);
            richTextBox3.Name = "richTextBox3";
            richTextBox3.Size = new Size(217, 54);
            richTextBox3.TabIndex = 20;
            richTextBox3.Text = "";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Font = new Font("Microsoft Sans Serif", 10F);
            label3.Location = new Point(53, 318);
            label3.Name = "label3";
            label3.Size = new Size(73, 17);
            label3.TabIndex = 21;
            label3.Text = "Keywords:";
            label3.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Font = new Font("Microsoft Sans Serif", 10F);
            label4.Location = new Point(53, 109);
            label4.Name = "label4";
            label4.Size = new Size(69, 17);
            label4.TabIndex = 22;
            label4.Text = "Specialty:";
            label4.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Font = new Font("Microsoft Sans Serif", 10F);
            label5.Location = new Point(53, 62);
            label5.Name = "label5";
            label5.Size = new Size(100, 17);
            label5.TabIndex = 23;
            label5.Text = "Sample Name:";
            label5.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // richTextBox4
            // 
            richTextBox4.Location = new Point(53, 335);
            richTextBox4.Margin = new Padding(3, 2, 3, 2);
            richTextBox4.Name = "richTextBox4";
            richTextBox4.Size = new Size(217, 32);
            richTextBox4.TabIndex = 24;
            richTextBox4.Text = "";
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Font = new Font("Microsoft Sans Serif", 10F);
            label6.Location = new Point(53, 238);
            label6.Name = "label6";
            label6.Size = new Size(83, 17);
            label6.TabIndex = 25;
            label6.Text = "Description:";
            label6.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // richTextBox5
            // 
            richTextBox5.Location = new Point(489, 80);
            richTextBox5.Margin = new Padding(3, 2, 3, 2);
            richTextBox5.Name = "richTextBox5";
            richTextBox5.ReadOnly = true;
            richTextBox5.Size = new Size(185, 239);
            richTextBox5.TabIndex = 26;
            richTextBox5.Text = "";
            // 
            // pictureBox1
            // 
            pictureBox1.Location = new Point(652, 59);
            pictureBox1.Margin = new Padding(3, 2, 3, 2);
            pictureBox1.Name = "pictureBox1";
            pictureBox1.Size = new Size(22, 20);
            pictureBox1.TabIndex = 27;
            pictureBox1.TabStop = false;
            // 
            // button2
            // 
            button2.BackColor = Color.FromArgb(210, 232, 247);
            button2.Font = new Font("Microsoft Sans Serif", 10F);
            button2.ImageAlign = ContentAlignment.MiddleLeft;
            button2.Location = new Point(302, 335);
            button2.Margin = new Padding(3, 2, 3, 2);
            button2.Name = "button2";
            button2.Padding = new Padding(9, 0, 0, 0);
            button2.Size = new Size(134, 44);
            button2.TabIndex = 28;
            button2.Text = "Clear info";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button2_Click;
            // 
            // FormTranscribe
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(700, 392);
            Controls.Add(button2);
            Controls.Add(pictureBox1);
            Controls.Add(richTextBox5);
            Controls.Add(label6);
            Controls.Add(richTextBox4);
            Controls.Add(label5);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(richTextBox3);
            Controls.Add(comboBox1);
            Controls.Add(label2);
            Controls.Add(richTextBox2);
            Controls.Add(button1);
            Controls.Add(label1);
            Controls.Add(richTextBox1);
            Controls.Add(Transcribe);
            Margin = new Padding(3, 2, 3, 2);
            Name = "FormTranscribe";
            Text = "FormTranscribe";
            Load += FormTranscribe_Load;
            ((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
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
        private ComboBox comboBox1;
        private RichTextBox richTextBox3;
        private Label label3;
        private Label label4;
        private Label label5;
        private RichTextBox richTextBox4;
        private Label label6;
        private RichTextBox richTextBox5;
        private PictureBox pictureBox1;
        private Button button2;
    }
}