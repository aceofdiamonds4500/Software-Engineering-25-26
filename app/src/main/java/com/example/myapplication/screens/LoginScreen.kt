package com.example.myapplication
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.material3.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun LoginScreen(
    onContinue: () -> Unit
) {
    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Button(
            onClick = onContinue,
            modifier = Modifier
                .align(Alignment.Center)
        ) {
            Text("Login")
        }
    }

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Button(
            onClick = onContinue,
            modifier = Modifier
                .align(Alignment.Center)
                .padding(top = 128.dp)
        ) {
            Text("Register")
        }
    }

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Button(
            onClick = onContinue,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 16.dp)
        ) {
            Text("Maybe Later...")
        }
    }
}



