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
import androidx.compose.ui.unit.dp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore

@Composable
fun CreateGroupScreen(
    onBack: () -> Unit,
    onSuccess: () -> Unit
) {
    var organizationName by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }
    var generatedCode by remember { mutableStateOf("") }

    val auth = FirebaseAuth.getInstance()
    val db = FirebaseFirestore.getInstance()

    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text("Create a Group", style = MaterialTheme.typography.headlineSmall)

            TextField(
                value = organizationName,
                onValueChange = { organizationName = it },
                label = { Text("Organization Name") },
                modifier = Modifier.fillMaxWidth()
            )

            // Show the following if a group code is generated
            if (generatedCode.isNotEmpty()) {
                Text(
                    text = "Group Code: $generatedCode",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary
                )
                Text(
                    text = "Share this code with your team",
                    style = MaterialTheme.typography.bodySmall
                )
            }

            Button(
                onClick = {
                    if (organizationName.isBlank()) {
                        errorMessage = "Please enter an organization name"
                        return@Button
                    }

                    isLoading = true
                    errorMessage = ""

                    val uid = auth.currentUser?.uid
                    if (uid == null) {
                        errorMessage = "Not logged in"
                        isLoading = false
                        return@Button
                    }

                    // Generate random 6 character code that can be shared
                    val code = (1..6)
                        .map { ('A'..'Z') + ('0'..'9') }
                        .map { it.random() }
                        .joinToString("")

                    // Create group document in Firestore
                    val groupDoc = hashMapOf(
                        "groupID" to code,
                        "organizationName" to organizationName,
                        "createdBy" to uid,
                        "members" to listOf(uid)
                    )

                    db.collection("groups").document(code).set(groupDoc)
                        .addOnSuccessListener {
                            // Update the user's groupID and organizationName
                            db.collection("users").document(uid)
                                .update(
                                    mapOf(
                                        "groupID" to code,
                                        "organizationName" to organizationName
                                    )
                                )
                                .addOnSuccessListener {
                                    isLoading = false
                                    generatedCode = code
                                    onSuccess()
                                }
                                .addOnFailureListener { e ->
                                    isLoading = false
                                    errorMessage = e.message ?: "Failed to update user"
                                }
                        }
                        .addOnFailureListener { e ->
                            isLoading = false
                            errorMessage = e.message ?: "Failed to create group"
                        }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading
            ) {
                Text(if (isLoading) "Creating Group..." else "Create Group")
            }

            Button(
                onClick = onBack,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Back")
            }

            if (errorMessage.isNotEmpty()) {
                Text(text = errorMessage, color = MaterialTheme.colorScheme.error)
            }
        }
    }
}