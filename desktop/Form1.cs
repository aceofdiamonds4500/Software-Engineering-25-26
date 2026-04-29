using System;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Media;
using System.IO;

namespace GUI_SoftwareEng
{
    public partial class Form1 : Form
    {
        [DllImport("user32.dll")] private static extern bool ReleaseCapture();
        [DllImport("user32.dll")] private static extern IntPtr SendMessage(IntPtr hWnd, int msg, int wParam, int lParam);
        private const int WM_NCLBUTTONDOWN = 0xA1;
        private const int HTCAPTION = 0x2;

        // ===== Page instances =====
        private FormLogin? loginPage;
        private FormRegister? registerPage;
        private Form1? form1;
        private FormTranscribe? transcribePage;
        private FormDownloadUpload? downloaduploadPage;
        private FormHistory? historyPage;
        private FormSettings? settingsPage;
        private FormMain? mainPage;
        private Form? currentPage;
        private Panel? contentHost;

        // expand sidebar
        private bool sidebarExpand = true;

        // sound
        private SoundPlayer? _soundplayer;
        private SoundPlayer? _soundplayer1;

        public Form1()
        {
            InitializeComponent();

            sidebar.Visible = false; // start with sidebar hidden

            // Window chrome & dragging
            FormBorderStyle = FormBorderStyle.None;
            panel1.MouseDown += Panel1_MouseDown;

            // border for sidebar
            sidebar.BorderStyle = BorderStyle.FixedSingle;

            // Sidebar button click buttons
            button1.Click += button1_Click; // Transcribe
            button2.Click += button2_Click; // Download/Upload
            button3.Click += button3_Click; // History
            button4.Click += button4_Click; // Settings

            // Timer for sidebar
            sidebarTransition.Tick += sidebarTransition_Tick;

            // opens home on startup
            Shown += (_, __) => ShowHomePage();

            // sound effects 😎
            try
            {
                string clickPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "click.wav");
                if (File.Exists(clickPath))
                    _soundplayer = new SoundPlayer(clickPath);
                else
                    _soundplayer = null;
            }
            catch { _soundplayer = null; }

            try
            {
                string slidePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "slide.wav");
                if (File.Exists(slidePath))
                    _soundplayer1 = new SoundPlayer(slidePath);
                else
                    _soundplayer1 = null;
            }
            catch { _soundplayer1 = null; }
        }

        // make border for style!
        protected override CreateParams CreateParams
        {
            get
            {
                const int WS_BORDER = 0x00800000;
                var cp = base.CreateParams;
                cp.Style |= WS_BORDER;
                return cp;
            }
        }

        // makes sure it has content host panel to dock pages into
        private void EnsureContentHost()
        {
            if (contentHost != null) return;
            contentHost = new Panel
            {
                Name = "contentHost",
                Dock = DockStyle.Fill,
            };
            Controls.Add(contentHost);
            contentHost.SendToBack();
        }

        // ===== Window dragging on the top panel =====
        private void Panel1_MouseDown(object? sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                ReleaseCapture();
                SendMessage(Handle, WM_NCLBUTTONDOWN, HTCAPTION, 0);
            }
        }

        // ===== Window controls =====
        private void pictureBox2_Click(object? sender, EventArgs e) => Close();
        private void pictureBox3_Click(object? sender, EventArgs e) => WindowState = FormWindowState.Minimized;

        // ===== Sidebar toggle =====
        private void pictureBox1_Click(object? sender, EventArgs e) 
        {
            try { _soundplayer1?.Play(); } catch { }
            sidebarTransition.Start();
        }

        private void sidebarTransition_Tick(object? sender, EventArgs e)
        {
            // Smoooooth expand/collapse 👌
            if (sidebarExpand)
            {
                sidebar.Width -= 10;
                if (sidebar.Width <= 50)
                {
                    sidebarExpand = false;
                    sidebarTransition.Stop();
                }
            }
            else
            {
                sidebar.Width += 10;
                if (sidebar.Width >= 254)
                {
                    sidebarExpand = true;
                    sidebarTransition.Stop();
                }
            }
        }

        // ===== Page Showing Logic =====
        private void ShowPage(Form? page)
        {
            if (page == null) return;
            
            EnsureContentHost();
            
            if (contentHost == null) return;

            // Add the page to the host
            if (!contentHost.Controls.Contains(page))
            {
                page.TopLevel = false;
                page.FormBorderStyle = FormBorderStyle.None;
                page.Dock = DockStyle.Fill;
                contentHost.Controls.Add(page);
                page.Show();
            }

            // Hide all other pages, show only the requested one
            foreach (Control ctl in contentHost.Controls)
            {
                ctl.Visible = ReferenceEquals(ctl, page);
            }

            // Bring the requested page to the front and focus it
            page.BringToFront();
            page.Focus();
            currentPage = page;

            // Collapse the sidebar after button presed
            CollapseSidebarIfOpen();
        }

        // Collapse only if currently expanded
        private void CollapseSidebarIfOpen()
        {
            if (sidebarTransition.Enabled)
            {
                return;
            }

            if (sidebarExpand)
            {
                sidebarTransition.Start();
            }
        }

        // ===== loads all pages =====
        private void ShowHomePage()
        {            
            if (loginPage == null || loginPage.IsDisposed)
            {
                loginPage = new FormLogin(this);
            }
            /*if (registerPage == null || registerPage.IsDisposed)
            {
                registerPage = new FormRegister(this);
            }*/
            if (transcribePage == null || transcribePage.IsDisposed)
            {
                transcribePage = new FormTranscribe();
            }
            if (downloaduploadPage == null || downloaduploadPage.IsDisposed)
            {
                downloaduploadPage = new FormDownloadUpload(transcribePage);
            }
            if (historyPage == null || historyPage.IsDisposed)
            {
                historyPage = new FormHistory();
            }
            if (settingsPage == null || settingsPage.IsDisposed)
            {
                settingsPage = new FormSettings(this);
            }
            ShowPage(loginPage);
        }
        // Called by login page when login is successful, shows main page
        public void LoginSuccessful()
        {
            if (mainPage == null || mainPage.IsDisposed)
            { 
                mainPage = new FormMain();
                ShowPage(mainPage);
                sidebar.Visible = true; // show sidebar after login
            }
        }
        public void ShowRegisterPage()
        {
            if (registerPage == null || registerPage.IsDisposed)
                registerPage = new FormRegister(this);
            ShowPage(registerPage);
        }

        public void LoginSuccessful()
        {
            sidebar.Visible = true;
            if(loginPage  == null || loginPage.IsDisposed)
            {
                loginPage = new FormLogin(this);
            }
            ShowPage(mainPage);
        }

        public void ShowRegisterPage()
        {
            if (registerPage == null || registerPage.IsDisposed)
            {
                registerPage = new FormRegister(this);
            }
            ShowPage(registerPage);
        }

        public void ShowLoginPage()
        {
            if (loginPage == null || loginPage.IsDisposed)
            {
                loginPage = new FormLogin(this);
            }
            ShowPage(loginPage);
        }

        private void label1_Click(object? sender, EventArgs e)
        {
            try { _soundplayer?.Play(); } catch { }
            ShowHomePage();
        }

        private void button1_Click(object? sender, EventArgs e)
        {
            try { _soundplayer?.Play(); } catch { }
            if (transcribePage == null || transcribePage.IsDisposed)
                transcribePage = new FormTranscribe();
            ShowPage(transcribePage);
        }

        private void button2_Click(object? sender, EventArgs e)
        {
            try { _soundplayer?.Play(); } catch { }
            if (downloaduploadPage == null || downloaduploadPage.IsDisposed)
                downloaduploadPage = new FormDownloadUpload(transcribePage ?? new FormTranscribe());
            ShowPage(downloaduploadPage);
        }

        private void button3_Click(object? sender, EventArgs e)
        {
            try { _soundplayer?.Play(); } catch { }
            if (historyPage == null || historyPage.IsDisposed)
                historyPage = new FormHistory();
            ShowPage(historyPage);
        }

        private void button4_Click(object? sender, EventArgs e)
        {
            try { _soundplayer?.Play(); } catch { }
            if (settingsPage == null || settingsPage.IsDisposed)
                settingsPage = new FormSettings(this);
            ShowPage(settingsPage);
        }

        // ===== settings toggles =====
        public void BroadcastToggleTheme()
        {
            if (mainPage == null) mainPage = new FormMain();
            if (transcribePage == null) transcribePage = new FormTranscribe();
            if (downloaduploadPage == null) downloaduploadPage = new FormDownloadUpload(transcribePage);
            if (historyPage == null) historyPage = new FormHistory();
            if (settingsPage == null) settingsPage = new FormSettings(this);


            // toggle all the pages theme
            ToggleTheme();
            mainPage?.ToggleTheme();
            transcribePage?.ToggleTheme();
            downloaduploadPage?.ToggleTheme();
            historyPage?.ToggleTheme();
            settingsPage?.ToggleTheme();
        }

        public void BroadcastToggleEnlargeText()
        {
            if (mainPage == null) mainPage = new FormMain();
            if (transcribePage == null) transcribePage = new FormTranscribe();
            if (downloaduploadPage == null) downloaduploadPage = new FormDownloadUpload(transcribePage);
            if (historyPage == null) historyPage = new FormHistory();
            if (settingsPage == null) settingsPage = new FormSettings(this);

            // toggles text size
            mainPage?.ToggleEnlargeText();
            transcribePage?.ToggleEnlargeText();
            downloaduploadPage?.ToggleEnlargeText();
            historyPage?.ToggleEnlargeText();
            settingsPage?.ToggleEnlargeText();
        }

        // =========== toggle functions for dark mode ============
        public void ToggleTheme()
        {
            if (panel1.BackColor == Color.FromArgb(123, 170, 224))
            {
                panel1.BackColor = Color.FromArgb(20, 28, 48);
                pictureBox2.BackColor = Color.FromArgb(20, 28, 48);
                pictureBox3.BackColor = Color.FromArgb(20, 28, 48);
                sidebar.BackColor = Color.FromArgb(32, 42, 72);
                button1.BackColor = Color.FromArgb(32, 42, 72);
                button2.BackColor = Color.FromArgb(32, 42, 72);
                button3.BackColor = Color.FromArgb(32, 42, 72);
                button4.BackColor = Color.FromArgb(32, 42, 72);
                label1.ForeColor = Color.White;
                button1.ForeColor = Color.White;
                button2.ForeColor = Color.White;
                button3.ForeColor = Color.White;
                button4.ForeColor = Color.White;
            }
            else
            {
                panel1.BackColor = Color.FromArgb(123, 170, 224);
                pictureBox2.BackColor = Color.FromArgb(123, 170, 224);
                pictureBox3.BackColor = Color.FromArgb(123, 170, 224);
                sidebar.BackColor = Color.FromArgb(210, 232, 247);
                button1.BackColor = Color.FromArgb(210, 232, 247);
                button2.BackColor = Color.FromArgb(210, 232, 247);
                button3.BackColor = Color.FromArgb(210, 232, 247);
                button4.BackColor = Color.FromArgb(210, 232, 247);
                label1.ForeColor = Color.Black;
                button1.ForeColor = Color.Black;
                button2.ForeColor = Color.Black;
                button3.ForeColor = Color.Black;
                button4.ForeColor = Color.Black;
            }
        }
    }
}
