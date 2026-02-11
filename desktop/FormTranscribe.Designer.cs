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
            Transcribe.Location = new Point(345, 50);
            Transcribe.Name = "Transcribe";
            Transcribe.Size = new Size(163, 41);
            Transcribe.TabIndex = 11;
            Transcribe.Text = "Transcribe";
            Transcribe.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // richTextBox1
            // 
            richTextBox1.Location = new Point(61, 340);
            richTextBox1.Name = "richTextBox1";
            richTextBox1.Size = new Size(247, 70);
            richTextBox1.TabIndex = 12;
            richTextBox1.Text = "";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 10F);
            label1.Location = new Point(61, 211);
            label1.Name = "label1";
            label1.Size = new Size(112, 20);
            label1.TabIndex = 14;
            label1.Text = "Transcription:";
            label1.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(210, 232, 247);
            button1.Font = new Font("Microsoft Sans Serif", 10F);
            // button1.Image = Properties.Resources.Speech_Bubble;
            button1.ImageAlign = ContentAlignment.MiddleLeft;
            button1.Location = new Point(515, 447);
            button1.Name = "button1";
            button1.Padding = new Padding(10, 0, 0, 0);
            button1.Size = new Size(255, 58);
            button1.TabIndex = 15;
            button1.Text = "Calculate Info";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // richTextBox2
            // 
            richTextBox2.HideSelection = false;
            richTextBox2.Location = new Point(61, 106);
            richTextBox2.Name = "richTextBox2";
            richTextBox2.Size = new Size(247, 28);
            richTextBox2.TabIndex = 16;
            richTextBox2.Text = "";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Microsoft Sans Serif", 10F);
            label2.Location = new Point(559, 83);
            label2.Name = "label2";
            label2.Size = new Size(76, 20);
            label2.TabIndex = 17;
            label2.Text = "Results: ";
            label2.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // comboBox1
            // 
            comboBox1.FormattingEnabled = true;
            comboBox1.Items.AddRange(new object[] { "Allergy / Immunology", "Bariatrics", "Cardiovascular / Pulmonary", "Chiropractic", "Consult - History and Phy.", "Cosmetic / Plastic Surgery", "Dentistry", "Dermatology", "Dietetics / Nutrition", "Discharge Summary", "Emergency Room Reports", "Endocrinology", "ENT - Otolaryngology", "Family Medicine", "Gastroenterology", "General Medicine", "Hematology - Oncology", "Infectious Disease", "Internal Medicine", "Lab Medicine - Pathology", "Letters", "Nephrology", "Neurology", "Neurosurgery", "Obstetrics / Gynecology", "Office Notes", "Ophthalmology", "Orthopedic", "Pain Management", "Pediatrics - Neonatal", "Physical Medicine - Rehab", "Podiatry", "Psychiatry / Psychology", "Radiology", "Rheumatology", "Sleep Medicine", "Speech - Language", "Surgery", "Urology" });
            comboBox1.Location = new Point(61, 168);
            comboBox1.Name = "comboBox1";
            comboBox1.Size = new Size(247, 28);
            comboBox1.TabIndex = 18;
            // 
            // richTextBox3
            // 
            richTextBox3.Location = new Point(61, 234);
            richTextBox3.Name = "richTextBox3";
            richTextBox3.Size = new Size(247, 70);
            richTextBox3.TabIndex = 20;
            richTextBox3.Text = "";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Font = new Font("Microsoft Sans Serif", 10F);
            label3.Location = new Point(61, 424);
            label3.Name = "label3";
            label3.Size = new Size(87, 20);
            label3.TabIndex = 21;
            label3.Text = "Keywords:";
            label3.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Font = new Font("Microsoft Sans Serif", 10F);
            label4.Location = new Point(61, 145);
            label4.Name = "label4";
            label4.Size = new Size(82, 20);
            label4.TabIndex = 22;
            label4.Text = "Specialty:";
            label4.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Font = new Font("Microsoft Sans Serif", 10F);
            label5.Location = new Point(61, 83);
            label5.Name = "label5";
            label5.Size = new Size(119, 20);
            label5.TabIndex = 23;
            label5.Text = "Sample Name:";
            label5.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // richTextBox4
            // 
            richTextBox4.Location = new Point(61, 447);
            richTextBox4.Name = "richTextBox4";
            richTextBox4.Size = new Size(247, 41);
            richTextBox4.TabIndex = 24;
            richTextBox4.Text = "";
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Font = new Font("Microsoft Sans Serif", 10F);
            label6.Location = new Point(61, 317);
            label6.Name = "label6";
            label6.Size = new Size(100, 20);
            label6.TabIndex = 25;
            label6.Text = "Description:";
            label6.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // richTextBox5
            // 
            richTextBox5.Location = new Point(559, 106);
            richTextBox5.Name = "richTextBox5";
            richTextBox5.ReadOnly = true;
            richTextBox5.Size = new Size(211, 317);
            richTextBox5.TabIndex = 26;
            richTextBox5.Text = "";
            // 
            // pictureBox1
            // 
            // pictureBox1.Image = Properties.Resources.Help1;
            pictureBox1.Location = new Point(745, 79);
            pictureBox1.Name = "pictureBox1";
            pictureBox1.Size = new Size(25, 26);
            pictureBox1.TabIndex = 27;
            pictureBox1.TabStop = false;
            // 
            // button2
            // 
            button2.BackColor = Color.FromArgb(210, 232, 247);
            button2.Font = new Font("Microsoft Sans Serif", 10F);
            // button2.Image = Properties.Resources.Broom_25x25;
            button2.ImageAlign = ContentAlignment.MiddleLeft;
            button2.Location = new Point(345, 447);
            button2.Name = "button2";
            button2.Padding = new Padding(10, 0, 0, 0);
            button2.Size = new Size(153, 58);
            button2.TabIndex = 28;
            button2.Text = "Clear info";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button2_Click;
            // 
            // FormTranscribe
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(800, 522);
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
            Name = "FormTranscribe";
            Text = "FormTranscribe";
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