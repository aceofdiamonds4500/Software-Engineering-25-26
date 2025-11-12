namespace GUI_SoftwareEng
{
    partial class FormDownloadUpload
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
            DownloadUpload = new ReaLTaiizor.Controls.BigLabel();
            button1 = new Button();
            button2 = new Button();
            label1 = new Label();
            SuspendLayout();
            // 
            // DownloadUpload
            // 
            DownloadUpload.AutoSize = true;
            DownloadUpload.BackColor = Color.Transparent;
            DownloadUpload.Font = new Font("Segoe UI", 18F, FontStyle.Bold);
            DownloadUpload.ForeColor = Color.Black;
            DownloadUpload.Location = new Point(285, 50);
            DownloadUpload.Name = "DownloadUpload";
            DownloadUpload.Size = new Size(278, 41);
            DownloadUpload.TabIndex = 12;
            DownloadUpload.Text = "Download/Upload";
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(210, 232, 247);
            button1.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button1.Image = Properties.Resources.Download1;
            button1.ImageAlign = ContentAlignment.MiddleLeft;
            button1.Location = new Point(290, 160);
            button1.Name = "button1";
            button1.Padding = new Padding(10, 0, 0, 0);
            button1.Size = new Size(261, 64);
            button1.TabIndex = 1;
            button1.TabStop = false;
            button1.Text = "Download Current Transcription";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.BackColor = Color.FromArgb(210, 232, 247);
            button2.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button2.Image = Properties.Resources.Upload;
            button2.ImageAlign = ContentAlignment.MiddleLeft;
            button2.Location = new Point(290, 235);
            button2.Name = "button2";
            button2.Padding = new Padding(10, 0, 0, 0);
            button2.Size = new Size(261, 64);
            button2.TabIndex = 1;
            button2.TabStop = false;
            button2.Text = "Upload Patient Details";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button2_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label1.ForeColor = Color.FromArgb(0, 192, 0);
            label1.Location = new Point(275, 312);
            label1.Name = "label1";
            label1.Size = new Size(0, 25);
            label1.TabIndex = 16;
            label1.TextAlign = ContentAlignment.BottomRight;
            // 
            // FormDownloadUpload
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(800, 450);
            Controls.Add(label1);
            Controls.Add(button2);
            Controls.Add(button1);
            Controls.Add(DownloadUpload);
            Name = "FormDownloadUpload";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private ReaLTaiizor.Controls.BigLabel DownloadUpload;
        private Button button1;
        private Button button2;
        private Label label1;
    }
}