namespace GUI_SoftwareEng
{
    partial class FormHistory
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
            History = new ReaLTaiizor.Controls.BigLabel();
            richTextBox2 = new RichTextBox();
            SuspendLayout();
            // 
            // History
            // 
            History.AutoSize = true;
            History.BackColor = Color.Transparent;
            History.Font = new Font("Segoe UI", 18F, FontStyle.Bold);
            History.ForeColor = Color.Black;
            History.Location = new Point(365, 65);
            History.Name = "History";
            History.Size = new Size(122, 41);
            History.TabIndex = 11;
            History.Text = "History";
            // 
            // richTextBox2
            // 
            richTextBox2.Enabled = false;
            richTextBox2.Location = new Point(85, 137);
            richTextBox2.Name = "richTextBox2";
            richTextBox2.Size = new Size(670, 301);
            richTextBox2.TabIndex = 17;
            richTextBox2.Text = "";
            // 
            // FormHistory
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(800, 450);
            Controls.Add(richTextBox2);
            Controls.Add(History);
            Name = "FormHistory";
            Text = "FormHistory";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private ReaLTaiizor.Controls.BigLabel History;
        private RichTextBox richTextBox2;
    }
}