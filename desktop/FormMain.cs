namespace GUI_SoftwareEng
{
    public partial class FormMain : Form
    {
        public FormMain()
        {
            InitializeComponent();
        }

        // =========== toggle functions for dark mode & enlarge text============
        public void ToggleTheme()
        {
            if (Welcome.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                Welcome.ForeColor = Color.White;
                label1.ForeColor = Color.White;
            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                Welcome.ForeColor = Color.Black;
                label1.ForeColor = Color.Black;
            }
        }

        public void ToggleEnlargeText()
        {
            if (Welcome.Font.Size >= 20)  // If already enlarged
            {
                Welcome.Font = new Font(Welcome.Font.FontFamily, 18, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 10);
                label1.Location = new Point(165, 150);
            }
            else  // If normal size
            {
                Welcome.Font = new Font(Welcome.Font.FontFamily, 25, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 15);
                label1.Location = new Point(90, 150);
            }
        }
    }
}
