using System;
using linux_desktop;
using System.Media;
using System.Net.Sockets;
using System.Net;
using System.Text;

public class Connection
{
    private TcpClient _client;
    private string _host;
    private int _port;
    private bool _isConnected;

    public Connection(string host, int port)
    {
        _host = host;
        _port = port;
        _client = new TcpClient();
        _isConnected = false;
    }

    public string ExchangeData(string data)
    {
        if (!_isConnected)
        {
            try
            {
                _client.Connect(_host, _port);
                _isConnected = true;
            }
            catch (Exception)
            {
                return "Error: Could not connect";
            }
        }
        try
        {
            NetworkStream stream = _client.GetStream();
            byte[] bytes = Encoding.UTF8.GetBytes(data);
            stream.Write(bytes, 0, bytes.Length);

            // Wait for response
            byte[] buffer = new byte[1024];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            if (bytesRead > 0)
            {
                string receivedMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                return receivedMessage;
            }
            else
            {
                return "Error: No response received";
            }
        }
        catch (Exception)
        {
            _isConnected = false;
            return "Error: Data exchange failed";
        }
    }
}
