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
fun SettingsScreen(
    isDarkMode: Boolean,
    enlargeText: Boolean,
    onDarkModeChange: (Boolean) -> Unit,
    onEnlargeTextChange: (Boolean) -> Unit,
    onAccountSettingsClick: () -> Unit
) {
    var tempDarkMode by remember { mutableStateOf(isDarkMode) }
    var tempEnlargeText by remember { mutableStateOf(enlargeText) }
    val auth = FirebaseAuth.getInstance()
    val db = FirebaseFirestore.getInstance()
    val scope = rememberCoroutineScope()
    val uid = auth.currentUser?.uid
    var successMessage by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }

    // Load existing settings from Firestore and apply to switches
    LaunchedEffect(Unit) {
        if (uid != null) {
            db.collection("users").document(uid).get()
                .addOnSuccessListener { doc ->
                    tempDarkMode = doc.getString("darkmode") == "1"
                    tempEnlargeText = doc.getString("enlargeText") == "1"
                }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Dark Mode")
            Spacer(modifier = Modifier.weight(1f))
            Switch(
                checked = tempDarkMode,
                onCheckedChange = { tempDarkMode = it }
            )
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Enlarge Font Size")
            Spacer(modifier = Modifier.weight(1f))
            Switch(
                checked = tempEnlargeText,
                onCheckedChange = { tempEnlargeText = it }
            )
        }

        Button(
            onClick = {
                val darkModeVar = if (tempDarkMode) "1" else "0"
                val enlargeTextVar = if (tempEnlargeText) "1" else "0"

                onDarkModeChange(tempDarkMode)
                onEnlargeTextChange(tempEnlargeText)

                scope.launch {
                    if (uid != null) {
                        try {
                            db.collection("users").document(uid)
                                .update(
                                    mapOf(
                                        "darkmode" to darkModeVar,
                                        "enlargeText" to enlargeTextVar
                                    )
                                ).await()
                            successMessage = "Settings applied!"
                            errorMessage = ""
                        } catch (e: Exception) {
                            errorMessage = e.message ?: "Failed to save settings."
                            successMessage = ""
                        }
                    } else {
                        errorMessage = "User not logged in."
                    }
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Apply Settings")
        }

        Button(
            onClick = {
                tempDarkMode = false
                tempEnlargeText = false
                onDarkModeChange(false)
                onEnlargeTextChange(false)
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Reset To Default Settings")
        }

        Button(
            onClick = onAccountSettingsClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Account Settings")
        }

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