using Google.Cloud.Firestore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GUI_SoftwareEng
{
    internal static class FirestoreHelper
    {
        static string fireconfig = @"
        {
            ""type"": ""service_account"",
            ""project_id"": ""transcriptive-ai"",
            ""private_key_id"": ""520601982cef6c190e033965791a11e6cc6c9fd6"",
            ""private_key"": ""-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQD1btgQkhxrGjQt\nMubJ6ap9r9R9YhscXKQOSIFzJAKkXYNo/DD16RRL7qqEZzEAv3BDGKG6oabAFFgy\n7IcWGvJZ7DaW8R52Qiw11v6b6ItsKhB5ObUS7ux1+7H5PWZBFzAfU8n0zqZCiPgQ\nYob9S+Nc49XnXLqKWPGNwwKYJwQugbmIUeYsFMTF+/ZKOVjyE/i2vjqPbij58CjZ\nbUhuZkZTIgCAnUsI3WHZOlkcBXiiriYCobkEPA8tcJ5K9J+DL2c/WrJVGGULShFD\nIJYHTLXQ/AGX/mEGfFI3C9E5IWba4ceziIQ5d0a+avtMWQ2pXAXcRVI3UZukHhSW\nkrWQ8JdrAgMBAAECggEAKaobANkk/OOSZvfkqPNDb5nJS027x3lMmmYhn5/F2QxM\n8iYZ060xNmC6TsbL0VIuZx2H2wx1J9dsT5zKo+yIJs7MR5yALNg39B3e1C3KeV68\ntC+hNykbOD41rNeJA9TBZRgOyUHJhLMG1ZU8UESxQMQmvGOIAVNvEj9AMf8xnQkw\njhy4kvcrPPjDvk4Nj5NV5//qDypR/5HsbuVqlGHWBuwiKxRBFtiSHyVi4g7Saw8K\nMddMf2nP1q9aC6RiVAdpkRkyifQzsITnXDQv5tLVh1e1tEoeFViMvlDfoxBvkQbl\n0YAwqz9XsVLNUe3zqUK8lzCW/kbZ7Lsml3HgyunIpQKBgQD+WSf3oSceC9Ouu8bE\n1xiqFd6y3j0mcoReTcu5wSmW7Wv4kAA9+wY/TNVfCcdvFG8RzpjHKMoPoXi0RKOH\nHOoT++ZWzY4EvFD9TWgv+ayXaRH7O7RpC+GCwaRaYs3NSG0POY16Duscem8eJyCV\n1ICqmXY62+zIZhSTqv5lNcXrfwKBgQD3Bt3YI1G9sCjK0/pC40+VGdeIW4zc4wbG\nvcv6KXiYI7nBr1LlkPXXwqEaEXd+jcOflCv1X3WPG4NfqhriSwJ6eP5BKAIVXuTU\n7rN7yT7HCyqChgiWjfhyxs/CT+Y3x5NohLQDyzdLGOirh7KvR/qwNG9XcYiCZONb\nVLPAema6FQKBgH4oxO1MLvX1UdM66rXaJy6+WE8KcvRuGwAXwHRrvnBRZZvN+YDE\n0W12c+OHGzgav5jqi9dFgSxNoGxyG1a6XdT5vl/R556rtdRen84kHpqfkD64d50f\nOoU7/YSju4cWZJoHpwgi/DWM+S7Qo5YN6KA2LHG3gnRIRe6VA0g6auiLAoGAaItn\naAnKllTvbqe3yocZLyj4pqTYQMN0IrhAk2bpurmj6+yfULjA0sd0Fuw9fjnRCMBU\nukvkHOSv/NSo/AxyyBJcyIZ+Gz1F6zf6jfDluKdpHkRLbiw3cZviYYIfFIxKPnmr\nFc/zXrzz+2Q6oyP7XIdUd9V8yHKaJhT63gLvZuECgYAOjvO2tETB7tQ126IxM5BG\nkPIf53GGFJSkTcu6zCVAxZytYVROQ17Y3ZEKLgs6mPdOwRvWeil/iWl83yAChSUb\nqViPVbGLVTfKafZPyE/Mgrz/pEE3wBajgizH2ebM9JF7udagWxcU41afyYBzbBi8\npJ2Dm/hbyPWUerCbS21hVw==\n-----END PRIVATE KEY-----\n"",
            ""client_email"": ""firebase-adminsdk-fbsvc@transcriptive-ai.iam.gserviceaccount.com"",
            ""client_id"": ""109239181082076537644"",
            ""auth_uri"": ""https://accounts.google.com/o/oauth2/auth"",
            ""token_uri"": ""https://oauth2.googleapis.com/token"",
            ""auth_provider_x509_cert_url"": ""https://www.googleapis.com/oauth2/v1/certs"",
            ""client_x509_cert_url"": ""https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40transcriptive-ai.iam.gserviceaccount.com"",
            ""universe_domain"": ""googleapis.com""
        } ";

        static string filePath = "";
        public static FirestoreDb? Database { get; private set; }

        public static void SetEnvironmentVariable()
        {
            filePath = Path.Combine(Path.GetTempPath(), Path.GetFileNameWithoutExtension(Path.GetRandomFileName())) + ".json";
            File.WriteAllText(filePath, fireconfig);
            File.SetAttributes(filePath, FileAttributes.Hidden);
            Environment.SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", filePath);
            Database = FirestoreDb.Create("transcriptive-ai");
            File.Delete(filePath);
        }
    }
}
