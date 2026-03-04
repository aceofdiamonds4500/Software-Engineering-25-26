package com.example.myapplication

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun TermsOfService(
    onBack: () -> Unit
) {

    val tosText =
        "The application does not provide medical, legal, or professional advice, and all generated " +
                "content must be independently reviewed by a qualified professional.\n\n" +
                "To the fullest extent permitted by law, the developers shall not be liable for any damages " +
                "arising from the use or misuse of this application, including but not limited to financial " +
                "loss, data loss, bodily injury, permanent disability, loss of limbs, or death.\n\n" +
                "Users acknowledge that information entered into the application may not be secure and could " +
                "potentially be accessed, intercepted, or disclosed by unauthorized third parties, including " +
                "hostile actors or foreign entities.\n\n" +
                "Creating an account in the Transcriptive AI app constitutes acceptance of these terms."

    val scrollState = rememberScrollState()

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        contentAlignment = Alignment.Center
    ) {

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(scrollState),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = MaterialTheme.shapes.large
            ) {
                Text(
                    text = tosText,
                    modifier = Modifier.padding(20.dp),
                    style = MaterialTheme.typography.bodyMedium
                )
            }

            Button(
                onClick = onBack,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Back")
            }
        }
    }
}