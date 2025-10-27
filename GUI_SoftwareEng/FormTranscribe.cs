using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Media;
using SimpleTCP;
using System.Net;

namespace GUI_SoftwareEng
{
    public partial class FormTranscribe : Form
    {
        private SoundPlayer _soundplayer;
        private SimpleTcpClient _client;
        private bool _isConnected;
        public FormTranscribe(SimpleTcpClient client)
        {
            InitializeComponent();
            _soundplayer = new SoundPlayer("click.wav");
            _client = client;
            _isConnected = false;
            _client.DataReceived += Client_DataReceived;
        }

        // transcription button
        private void button1_Click(object sender, EventArgs e)
        {
            _soundplayer.Play();

            if (!_isConnected)
            {
                try
                {
                    _client.Connect("127.0.0.1", 65067);
                    _isConnected = true;
                }
                catch (Exception ex)
                {
                    richTextBox2.Text = "Error: Could not connect\r\n";
                    return;
                }
            }
            if (_isConnected)
            {
                _client.WriteLineAndGetReply(richTextBox1.Text, TimeSpan.FromSeconds(3));
            }
        }
        private void Client_DataReceived(object sender, SimpleTCP.Message e)
        {
            richTextBox2.Invoke((MethodInvoker)delegate
            {
                richTextBox2.Text = e.MessageString.Replace("\u0013", string.Empty) + "\r\n";
            });
        }
        // setters & getters for textboxes 
        public string InputText
        {
            get => richTextBox1.Text;
            set => richTextBox1.Text = value;
        }
        public string OutputText
        {
            get => richTextBox2.Text;
            set => richTextBox2.Text = value;
        }

        // =========== toggle functions for dark mode & enlarge text============
        public void ToggleTheme()
        {
            if (Transcribe.ForeColor == Color.Black)
            {
                BackColor = Color.FromArgb(24, 30, 54);
                label1.ForeColor = Color.White;
                label2.ForeColor = Color.White;
                Transcribe.ForeColor = Color.White;
                button1.BackColor = Color.FromArgb(32, 42, 72);
                button1.ForeColor = Color.White;
            }
            else
            {
                BackColor = Color.FromArgb(220, 224, 228);
                label1.ForeColor = Color.Black;
                label2.ForeColor = Color.Black;
                Transcribe.ForeColor = Color.Black;
                richTextBox1.BackColor = Color.White;
                button1.BackColor = Color.FromArgb(210, 232, 247);
                button1.ForeColor = Color.Black;
            }
        }
        public void ToggleEnlargeText()
        {
            if (Transcribe.Font.Size == 18)
            {
                Transcribe.Font = new Font(Transcribe.Font.FontFamily, 20, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 13);
                label2.Font = new Font(label2.Font.FontFamily, 13);
                button1.Font = new Font(button1.Font.FontFamily, 12);
                button1.Size = new Size(265, 70);
                button1.Location = new Point(290, 200);
            }
            else
            {
                Transcribe.Font = new Font(Transcribe.Font.FontFamily, 18, FontStyle.Bold);
                label1.Font = new Font(label1.Font.FontFamily, 10);
                label2.Font = new Font(label2.Font.FontFamily, 10);
                button1.Font = new Font(button1.Font.FontFamily, 10);
            }
        }

        
    }
}
