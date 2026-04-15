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
            DownloadUpload.Location = new Point(267, 59);
            DownloadUpload.Name = "DownloadUpload";
            DownloadUpload.Size = new Size(224, 32);
            DownloadUpload.TabIndex = 12;
            DownloadUpload.Text = "Download/Upload";
            // 
            // button1
            // 
            button1.AutoSize = true;
            button1.BackColor = Color.FromArgb(210, 232, 247);
            button1.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button1.ImageAlign = ContentAlignment.MiddleLeft;
            button1.Location = new Point(256, 130);
            button1.Margin = new Padding(3, 2, 3, 2);
            button1.Name = "button1";
            button1.Padding = new Padding(9, 0, 0, 0);
            button1.Size = new Size(251, 52);
            button1.TabIndex = 1;
            button1.TabStop = false;
            button1.Text = "Download Current Transcription";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // button2
            // 
            button2.AutoSize = true;
            button2.BackColor = Color.FromArgb(210, 232, 247);
            button2.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button2.ImageAlign = ContentAlignment.MiddleLeft;
            button2.Location = new Point(256, 206);
            button2.Margin = new Padding(3, 2, 3, 2);
            button2.Name = "button2";
            button2.Padding = new Padding(9, 0, 0, 0);
            button2.Size = new Size(251, 48);
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
            label1.Location = new Point(241, 234);
            label1.Name = "label1";
            label1.Size = new Size(0, 20);
            label1.TabIndex = 16;
            label1.TextAlign = ContentAlignment.BottomRight;
            // 
            // FormDownloadUpload
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(700, 338);
            Controls.Add(label1);
            Controls.Add(button2);
            Controls.Add(button1);
            Controls.Add(DownloadUpload);
            Margin = new Padding(3, 2, 3, 2);
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