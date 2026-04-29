package com.example.myapplication

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.google.firebase.auth.FirebaseAuth

@Composable
fun ForgotPasswordScreen(
    onBack: () -> Unit
) {

    var email by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }
    var isSuccess by remember { mutableStateOf(false) }

    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {

            TextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                modifier = Modifier.fillMaxWidth()
            )

            // password reset button
            Button(
                onClick = {
                    isLoading = true
                    val auth = FirebaseAuth.getInstance()
                    auth.sendPasswordResetEmail(email)
                          .addOnSuccessListener {
                              isLoading = false
                              isSuccess = true
                          }
                          .addOnFailureListener { e ->
                              isLoading = false
                              errorMessage = e.message ?: "Password reset failed"
                          }
                          },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading
            ) {
                Text(if (isLoading) "Resetting Password..." else "Rest Password")
            }

            // back button
            Button(
                onClick = onBack,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Back")
            }

            // error / success message
            if (isSuccess)
            {
                Text(text = "Password reset email sent", color = Color.Green)
            }
            if (errorMessage.isNotEmpty()) {
                Text(text = errorMessage, color = Color.Red)
            }
        }
    }
}
