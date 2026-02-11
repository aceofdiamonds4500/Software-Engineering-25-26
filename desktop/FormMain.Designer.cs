namespace GUI_SoftwareEng
{
    partial class FormMain
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormMain));
            Welcome = new ReaLTaiizor.Controls.BigLabel();
            label1 = new Label();
            SuspendLayout();
            // 
            // Welcome
            // 
            Welcome.AutoSize = true;
            Welcome.BackColor = Color.Transparent;
            Welcome.Font = new Font("Segoe UI", 18F, FontStyle.Bold, GraphicsUnit.Point, 0);
            Welcome.ForeColor = Color.Black;
            Welcome.Location = new Point(200, 80);
            Welcome.Name = "Welcome";
            Welcome.Size = new Size(417, 41);
            Welcome.TabIndex = 12;
            Welcome.Text = "Welcome To Transcriptive AI";
            Welcome.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 10F);
            label1.Location = new Point(165, 150);
            label1.Name = "label1";
            label1.Size = new Size(475, 140);
            label1.TabIndex = 13;
            label1.Text = resources.GetString("label1.Text");
            label1.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // FormMain
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(800, 450);
            Controls.Add(label1);
            Controls.Add(Welcome);
            Name = "FormMain";
            Text = "FormMain";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private ReaLTaiizor.Controls.BigLabel Welcome;
        private Label label1;
    }
}