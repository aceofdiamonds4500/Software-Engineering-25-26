package com.example.myapplication
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch

@Composable
fun SupportLegalScreen(
    onBack: () -> Unit,
) {
    Column (modifier = Modifier
        .fillMaxSize()
        .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)) {

        Text(
            text = "The application does not provide medical, legal, or professional advice, and all generated " +
                    "content must be independently reviewed by a qualified professional. To the fullest extent" +
                    " permitted by law, the developers shall not be liable for any damages arising from the use " +
                    "or misuse of this application, including but not limited to financial loss, data loss, bodily " +
                    "injury, permanent disability, loss of limbs, or death. Users acknowledge that information ente" +
                    "red into the application may not be secure and could potentially be accessed, intercepted, " +
                    "or disclosed by unauthorized third parties, including hostile actors or foreign entities. " +
                    "The creation of an account in Transcription AI app constitutes to acceptance of these terms.",
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center,
            style = MaterialTheme.typography.bodyLarge,
            lineHeight = MaterialTheme.typography.bodyLarge.lineHeight * 1.25
        )

        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }
    }
}