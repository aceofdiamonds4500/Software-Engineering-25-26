package com.example.myapplication
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.material3.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.style.TextAlign

@Composable
fun HomeScreen() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp, vertical = 16.dp)
    ) {
        Text(  /* instead of home page make it a dashboard show users last transcription?
                  show user's stats like current number of transcriptions stores to that account
                  etc...*/
            text = "Transcriptive is an AI-powered medical transcription assistant " +
                    "that helps reduce errors and improve data accuracy. " +
                    "It takes patient notes, detects diagnoses, medications, and " +
                    "procedures, and highlights possible mistakes in real time. " +
                    "Designed for clinicians and transcriptionists, Transcriptive " +
                    "delivers fast, accurate, and reliable results to support better " +
                    "medical research and practice.",
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center,
            style = MaterialTheme.typography.bodyLarge,
            lineHeight = MaterialTheme.typography.bodyLarge.lineHeight * 1.25
        )
    }
}
