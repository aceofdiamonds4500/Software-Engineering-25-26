package com.example.myapplication

import android.content.Intent
import android.provider.Settings
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricManager.Authenticators.*
import androidx.biometric.BiometricPrompt
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import androidx.activity.compose.LocalActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts

@Composable
fun LoginFormScreen(
    onBack: () -> Unit,
    onSuccess: () -> Unit,
    onForgotClick: () -> Unit
) {

    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }

    val activity = LocalActivity.current as FragmentActivity
    val auth = FirebaseAuth.getInstance()
    val db = FirebaseFirestore.getInstance()

    val enrollLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { }

    fun launchBiometrics(onApproved:() -> Unit, onDenied: () -> Unit) {
        val biometricManager = BiometricManager.from(activity)

        when (biometricManager.canAuthenticate(BIOMETRIC_STRONG)) {
            BiometricManager.BIOMETRIC_SUCCESS -> {
                val executor = ContextCompat.getMainExecutor(activity)
                val prompt = BiometricPrompt(activity, executor,
                    object : BiometricPrompt.AuthenticationCallback() {
                        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                            onApproved()
                        }
                        override fun onAuthenticationFailed() {
                            // Bad attempt, prompt stays open
                        }
                        override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                            onDenied()
                            errorMessage = "Biometric error: $errString"
                        }
                    })

                val promptInfo = BiometricPrompt.PromptInfo.Builder()
                    .setTitle("Biometric login for my app")
                    .setSubtitle("Log in using your biometric credential")
                    .setNegativeButtonText("Cancel")
                    .setAllowedAuthenticators(BIOMETRIC_STRONG)
                    .build()

                prompt.authenticate(promptInfo)
            }
            BiometricManager.BIOMETRIC_ERROR_NONE_ENROLLED -> {
                val enrollIntent = Intent(Settings.ACTION_BIOMETRIC_ENROLL).apply {
                    putExtra(Settings.EXTRA_BIOMETRIC_AUTHENTICATORS_ALLOWED, BIOMETRIC_STRONG)
                }
                enrollLauncher.launch(enrollIntent)
                onDenied()
            }
            BiometricManager.BIOMETRIC_ERROR_NO_HARDWARE,
            BiometricManager.BIOMETRIC_ERROR_HW_UNAVAILABLE -> {
                // No biometric hardware, skip straight through
                onApproved()
            }
            else -> onApproved()
        }
    }

    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ){

            TextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                modifier = Modifier.fillMaxWidth()
            )

            TextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                visualTransformation = PasswordVisualTransformation(), // hides password w/ ****
                modifier = Modifier.fillMaxWidth()
            )

            // login button
            Button(
                onClick = {
                    isLoading = true
                    auth.signInWithEmailAndPassword(email, password) // logs in user w/ firebase
                        .addOnSuccessListener {
                            val uid = auth.currentUser?.uid ?: return@addOnSuccessListener

                            db.collection("users").document(uid).get()
                                .addOnSuccessListener { doc ->
                                    isLoading = false
                                    val biometricsEnabled = doc.getString("biometrics") == "1"

                                    if (biometricsEnabled) {
                                        launchBiometrics(onSuccess, onDenied = {
                                            auth.signOut()
                                            errorMessage = "Biometric login failed"
                                        })
                                    } else {
                                        onSuccess()
                                    }
                                }
                                .addOnFailureListener { e ->
                                    isLoading = false
                                    errorMessage = e.message ?: "Failed to load user data"
                                }
                        }
                        .addOnFailureListener { e ->
                            isLoading = false
                            errorMessage = e.message ?: "Login failed"
                        }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading
            ) {
                Text(if (isLoading) "Logging in..." else "Login")
            }

            // back button
            Button(
                onClick = onBack,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Back")
            }

            // forgot password text button
            Text(
                text = "Forgot password?",
                modifier = Modifier
                    .clickable { onForgotClick() }
                    .fillMaxWidth(),
                textAlign = TextAlign.Center,
                style = MaterialTheme.typography.bodyLarge,
                lineHeight = MaterialTheme.typography.bodyLarge.lineHeight * 1.25
            )

            if (errorMessage.isNotEmpty()) {
                Text(text = errorMessage, color = MaterialTheme.colorScheme.error)
            }
        }
    }
}
