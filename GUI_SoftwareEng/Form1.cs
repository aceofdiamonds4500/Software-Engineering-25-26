using System;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace GUI_SoftwareEng
{
    public partial class Form1 : Form
    {
        [DllImport("user32.dll")] private static extern bool ReleaseCapture();
        [DllImport("user32.dll")] private static extern IntPtr SendMessage(IntPtr hWnd, int msg, int wParam, int lParam);
        private const int WM_NCLBUTTONDOWN = 0xA1;
        private const int HTCAPTION = 0x2;

        // ===== Page instances =====
        private FormTranscribe? transcribePage;
        private FormDownloadUpload? downloaduploadPage;
        private FormHistory? historyPage;
        private FormSettings? settingsPage;
        private FormMain? mainPage;
        private Form? currentPage;
        private Panel? contentHost;

        private bool sidebarExpand = true;

        public Form1()
        {
            InitializeComponent();

            // Window chrome & dragging
            FormBorderStyle = FormBorderStyle.None;
            panel1.MouseDown += Panel1_MouseDown;

            // border for sidebar
            sidebar.BorderStyle = BorderStyle.FixedSingle;

            // Sidebar button click buttons
            button1.Click += button1_Click_1; // Transcribe
            button2.Click += button2_Click;   // Download/Upload
            button3.Click += button3_Click;   // History
            button4.Click += button4_Click;   // Settings

            // Timer for sidebar
            sidebarTransition.Tick += sidebarTransition_Tick;

            // opens home on startup
            Shown += (_, __) => ShowHomePage();
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

        // Ensure it has content host panel to dock pages into
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
        private void pictureBox1_Click(object? sender, EventArgs e) => sidebarTransition.Start();

        private void sidebarTransition_Tick(object? sender, EventArgs e)
        {
            // Smooooooth expand/collapse
            if (sidebarExpand)
            {
                sidebar.Width -= 10;
                if (sidebar.Width <= 55)
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
        private void ShowPage(Form page)
        {
            EnsureContentHost();

            // Add the page to the host
            if (!contentHost!.Controls.Contains(page))
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
            if (sidebarTransition.Enabled) return;
            if (sidebarExpand)
            {
                sidebarTransition.Start(); 
            }
        }

        // ===== loads home page first =====
        private void ShowHomePage()
        {
            if (mainPage == null || mainPage.IsDisposed)
                mainPage = new FormMain();
            ShowPage(mainPage);
        }

        private void label1_Click(object? sender, EventArgs e) => ShowHomePage();

        private void button1_Click_1(object? sender, EventArgs e)
        {
            if (transcribePage == null || transcribePage.IsDisposed)
                transcribePage = new FormTranscribe();

            ShowPage(transcribePage);
        }

        private void button2_Click(object? sender, EventArgs e)
        {
            if (transcribePage == null || transcribePage.IsDisposed)
                transcribePage = new FormTranscribe();

            if (downloaduploadPage == null || downloaduploadPage.IsDisposed)
                downloaduploadPage = new FormDownloadUpload(transcribePage);

            ShowPage(downloaduploadPage);
        }

        private void button3_Click(object? sender, EventArgs e)
        {
            if (historyPage == null || historyPage.IsDisposed)
                historyPage = new FormHistory();
            ShowPage(historyPage);
        }

        private void button4_Click(object? sender, EventArgs e)
        {
            if (settingsPage == null || settingsPage.IsDisposed)
                settingsPage = new FormSettings();
            ShowPage(settingsPage);
        }
    }
}
