namespace GUI_SoftwareEng
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            panel1 = new Panel();
            pictureBox3 = new PictureBox();
            label1 = new Label();
            pictureBox1 = new PictureBox();
            pictureBox2 = new PictureBox();
            sidebar = new FlowLayoutPanel();
            panel2 = new Panel();
            button1 = new Button();
            panel3 = new Panel();
            button2 = new Button();
            panel4 = new Panel();
            button3 = new Button();
            panel5 = new Panel();
            button4 = new Button();
            sidebarTransition = new System.Windows.Forms.Timer(components);
            panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)pictureBox3).BeginInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox2).BeginInit();
            sidebar.SuspendLayout();
            panel2.SuspendLayout();
            panel3.SuspendLayout();
            panel4.SuspendLayout();
            panel5.SuspendLayout();
            SuspendLayout();
            // 
            // panel1
            // 
            panel1.BackColor = Color.FromArgb(123, 170, 224);
            panel1.Controls.Add(pictureBox3);
            panel1.Controls.Add(label1);
            panel1.Controls.Add(pictureBox1);
            panel1.Location = new Point(-5, -3);
            panel1.Margin = new Padding(3, 2, 3, 2);
            panel1.Name = "panel1";
            panel1.Size = new Size(723, 34);
            panel1.TabIndex = 1;
            // 
            // pictureBox3
            // 
            pictureBox3.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            pictureBox3.BackColor = Color.FromArgb(123, 170, 224);
            pictureBox3.Image = (Image)resources.GetObject("pictureBox3.Image");
            pictureBox3.Location = new Point(663, 7);
            pictureBox3.Margin = new Padding(3, 2, 3, 2);
            pictureBox3.Name = "pictureBox3";
            pictureBox3.Size = new Size(26, 24);
            pictureBox3.TabIndex = 4;
            pictureBox3.TabStop = false;
            pictureBox3.Click += pictureBox3_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label1.Location = new Point(55, 8);
            label1.Name = "label1";
            label1.Size = new Size(118, 20);
            label1.TabIndex = 3;
            label1.Text = "Transcriptive AI";
            label1.Click += label1_Click;
            // 
            // pictureBox1
            // 
            pictureBox1.Image = (Image)resources.GetObject("pictureBox1.Image");
            pictureBox1.Location = new Point(18, 7);
            pictureBox1.Margin = new Padding(3, 2, 3, 2);
            pictureBox1.Name = "pictureBox1";
            pictureBox1.Size = new Size(27, 22);
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBox1.TabIndex = 2;
            pictureBox1.TabStop = false;
            pictureBox1.Click += pictureBox1_Click;
            // 
            // pictureBox2
            // 
            pictureBox2.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            pictureBox2.BackColor = Color.FromArgb(123, 170, 224);
            pictureBox2.Image = (Image)resources.GetObject("pictureBox2.Image");
            pictureBox2.Location = new Point(690, 4);
            pictureBox2.Margin = new Padding(3, 2, 3, 2);
            pictureBox2.Name = "pictureBox2";
            pictureBox2.Size = new Size(24, 24);
            pictureBox2.SizeMode = PictureBoxSizeMode.AutoSize;
            pictureBox2.TabIndex = 3;
            pictureBox2.TabStop = false;
            pictureBox2.Click += pictureBox2_Click;
            // 
            // sidebar
            // 
            sidebar.BackColor = Color.FromArgb(210, 232, 247);
            sidebar.Controls.Add(panel2);
            sidebar.Controls.Add(panel3);
            sidebar.Controls.Add(panel4);
            sidebar.Controls.Add(panel5);
            sidebar.Location = new Point(-3, 30);
            sidebar.Margin = new Padding(3, 2, 3, 2);
            sidebar.Name = "sidebar";
            sidebar.Size = new Size(44, 365);
            sidebar.TabIndex = 2;
            // 
            // panel2
            // 
            panel2.Controls.Add(button1);
            panel2.Location = new Point(3, 2);
            panel2.Margin = new Padding(3, 2, 3, 2);
            panel2.Name = "panel2";
            panel2.Size = new Size(219, 35);
            panel2.TabIndex = 6;
            // 
            // button1
            // 
            button1.BackColor = Color.FromArgb(210, 232, 247);
            button1.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button1.Image = (Image)resources.GetObject("button1.Image");
            button1.ImageAlign = ContentAlignment.MiddleLeft;
            button1.Location = new Point(-4, -8);
            button1.Margin = new Padding(3, 2, 3, 2);
            button1.Name = "button1";
            button1.Padding = new Padding(9, 0, 9, 0);
            button1.Size = new Size(245, 52);
            button1.TabIndex = 5;
            button1.Text = "Transcribe";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // panel3
            // 
            panel3.Controls.Add(button2);
            panel3.Location = new Point(3, 41);
            panel3.Margin = new Padding(3, 2, 3, 2);
            panel3.Name = "panel3";
            panel3.Size = new Size(219, 35);
            panel3.TabIndex = 6;
            // 
            // button2
            // 
            button2.BackColor = Color.FromArgb(210, 232, 247);
            button2.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button2.Image = (Image)resources.GetObject("button2.Image");
            button2.ImageAlign = ContentAlignment.MiddleLeft;
            button2.Location = new Point(-4, -9);
            button2.Margin = new Padding(3, 2, 3, 2);
            button2.Name = "button2";
            button2.Padding = new Padding(9, 0, 0, 0);
            button2.Size = new Size(245, 52);
            button2.TabIndex = 6;
            button2.Text = "Download/Upload";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button4_Click;
            // 
            // panel4
            // 
            panel4.Controls.Add(button3);
            panel4.Location = new Point(3, 80);
            panel4.Margin = new Padding(3, 2, 3, 2);
            panel4.Name = "panel4";
            panel4.Size = new Size(219, 35);
            panel4.TabIndex = 7;
            // 
            // button3
            // 
            button3.BackColor = Color.FromArgb(210, 232, 247);
            button3.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button3.Image = (Image)resources.GetObject("button3.Image");
            button3.ImageAlign = ContentAlignment.MiddleLeft;
            button3.Location = new Point(-4, -10);
            button3.Margin = new Padding(3, 2, 3, 2);
            button3.Name = "button3";
            button3.Padding = new Padding(9, 0, 9, 0);
            button3.Size = new Size(245, 52);
            button3.TabIndex = 3;
            button3.Text = "History";
            button3.UseVisualStyleBackColor = false;
            // 
            // panel5
            // 
            panel5.Controls.Add(button4);
            panel5.Location = new Point(3, 119);
            panel5.Margin = new Padding(3, 2, 3, 2);
            panel5.Name = "panel5";
            panel5.Size = new Size(219, 35);
            panel5.TabIndex = 8;
            // 
            // button4
            // 
            button4.BackColor = Color.FromArgb(210, 232, 247);
            button4.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            button4.Image = (Image)resources.GetObject("button4.Image");
            button4.ImageAlign = ContentAlignment.MiddleLeft;
            button4.Location = new Point(-4, -8);
            button4.Margin = new Padding(3, 2, 3, 2);
            button4.Name = "button4";
            button4.Padding = new Padding(9, 0, 9, 0);
            button4.Size = new Size(245, 52);
            button4.TabIndex = 6;
            button4.Text = "Settings";
            button4.UseVisualStyleBackColor = false;
            // 
            // sidebarTransition
            // 
            sidebarTransition.Interval = 5;
            sidebarTransition.Tick += sidebarTransition_Tick;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(220, 224, 228);
            ClientSize = new Size(716, 394);
            Controls.Add(pictureBox2);
            Controls.Add(panel1);
            Controls.Add(sidebar);
            FormBorderStyle = FormBorderStyle.None;
            Margin = new Padding(3, 2, 3, 2);
            Name = "Form1";
            ShowIcon = false;
            Text = "Transcriptive AI";
            panel1.ResumeLayout(false);
            panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)pictureBox3).EndInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
            ((System.ComponentModel.ISupportInitialize)pictureBox2).EndInit();
            sidebar.ResumeLayout(false);
            panel2.ResumeLayout(false);
            panel3.ResumeLayout(false);
            panel4.ResumeLayout(false);
            panel5.ResumeLayout(false);
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private Panel panel1;
        private PictureBox pictureBox1;
        private Label label1;
        protected FlowLayoutPanel sidebar;
        private Button button3;
        private Button button1;
        private Button button4;
        private Button button2;
        private System.Windows.Forms.Timer sidebarTransition;
        private Panel panel2;
        private Panel panel3;
        private Panel panel4;
        private Panel panel5;
        private PictureBox pictureBox3;
        private PictureBox pictureBox2;
    }
}
