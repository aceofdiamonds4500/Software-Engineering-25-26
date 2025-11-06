namespace GUI_SoftwareEng
{
    partial class FormSettings
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
            button2 = new Button();
            button1 = new Button();
            Settings = new ReaLTaiizor.Controls.BigLabel();
            SuspendLayout();
            // 
            // button2
            // 
            button2.BackColor = Color.FromArgb(210, 232, 247);
            button2.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button2.Image = Properties.Resources.x;
            button2.ImageAlign = ContentAlignment.MiddleLeft;
            button2.Location = new Point(315, 225);
            button2.Name = "button2";
            button2.Padding = new Padding(10, 0, 0, 0);
            button2.Size = new Size(210, 50);
            button2.TabIndex = 7;
            button2.Text = "Dark Mode";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button2_Click;
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(210, 232, 247);
            button1.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button1.Image = Properties.Resources.x;
            button1.ImageAlign = ContentAlignment.MiddleLeft;
            button1.Location = new Point(315, 160);
            button1.Name = "button1";
            button1.Padding = new Padding(10, 0, 0, 0);
            button1.Size = new Size(210, 50);
            button1.TabIndex = 8;
            button1.Text = "Enlarge Text";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // Settings
            // 
            Settings.AutoSize = true;
            Settings.BackColor = Color.Transparent;
            Settings.Font = new Font("Segoe UI", 18F, FontStyle.Bold);
            Settings.ForeColor = Color.Black;
            Settings.Location = new Point(355, 50);
            Settings.Name = "Settings";
            Settings.Size = new Size(134, 41);
            Settings.TabIndex = 10;
            Settings.Text = "Settings";
            // 
            // FormSettings
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(800, 450);
            Controls.Add(Settings);
            Controls.Add(button1);
            Controls.Add(button2);
            Name = "FormSettings";
            Text = "FormSettings";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button2;
        private Button button1;
        private ReaLTaiizor.Controls.BigLabel Settings;
    }
}