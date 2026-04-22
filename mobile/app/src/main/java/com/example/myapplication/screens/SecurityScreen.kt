package com.example.myapplication

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

@Composable
fun SecurityScreen(
    onBack: () -> Unit,
) {
    val auth = FirebaseAuth.getInstance()
    val db = FirebaseFirestore.getInstance()
    val uid = auth.currentUser?.uid
    var toggleBiometrics by remember { mutableStateOf(false) }
    var biometricsVar by remember { mutableStateOf("") }
    var toggle2FA by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    var isLoading by remember { mutableStateOf(false) }
    var successMessage by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }

    // Load existing profile data
    LaunchedEffect(Unit) {
        if (uid != null) {
            db.collection("users").document(uid).get()
                .addOnSuccessListener { doc ->
                    biometricsVar = doc.getString("biometrics") ?: ""
                }
        }
    }

    Column (modifier = Modifier
        .fillMaxSize()
        .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)) {

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Enable Biometrics")
            Spacer(modifier = Modifier.weight(1f))
            Switch(checked = toggleBiometrics, onCheckedChange = { isChecked ->
                toggleBiometrics = isChecked
                biometricsVar = if (isChecked) "1" else "0"
            })
        }

        if (biometricsVar == "1") {
            toggleBiometrics = true
        } else {
            toggleBiometrics = false
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Enable 2FA")
            Spacer(modifier = Modifier.weight(1f))
            Switch(checked = toggle2FA, onCheckedChange = { toggle2FA = it })
        }
        Button(
            onClick = {
                scope.launch {
                    // apply settings and save to firebase
                        if (uid != null) {
                            db.collection("users").document(uid)
                                .update(
                                mapOf(
                                    "biometrics" to biometricsVar
                                )
                            ).await()
                        successMessage = "Settings applied!"
                    } else {
                        errorMessage = "User not logged in."
                    }
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(18.dp),
                    strokeWidth = 2.dp,
                    color = MaterialTheme.colorScheme.onPrimary
                )
            } else {
                Text("Apply Settings")
            }
        }

        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }

        // error / success messages
        if (successMessage.isNotBlank()) {
            Text(
                text = successMessage,
                color = Color.Green,
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )
        }

        if (errorMessage.isNotBlank()) {
            Text(
                text = errorMessage,
                color = Color.Red,
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )
        }
    }
}