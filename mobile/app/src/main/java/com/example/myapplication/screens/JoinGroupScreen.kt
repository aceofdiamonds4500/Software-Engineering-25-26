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
import com.google.firebase.firestore.FieldValue

@Composable
fun JoinGroupScreen(
    onBack: () -> Unit,
    onSuccess: () -> Unit
) {
    var groupCode by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }

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
            Text("Join a Group", style = MaterialTheme.typography.headlineSmall)

            TextField(
                value = groupCode,
                onValueChange = { groupCode = it.uppercase() },
                label = { Text("Group Code") },
                modifier = Modifier.fillMaxWidth()
            )

            Button(
                onClick = {
                    if (groupCode.isBlank()) {
                        errorMessage = "Please enter a group code"
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

                    // Check if group exists if not EORROROROROR
                    db.collection("groups").document(groupCode).get()
                        .addOnSuccessListener { doc ->
                            if (!doc.exists()) {
                                isLoading = false
                                errorMessage = "Group not found"
                                return@addOnSuccessListener
                            }

                            val orgName = doc.getString("organizationName") ?: ""

                            // Add user to members array
                            db.collection("groups").document(groupCode)
                                .update("members", FieldValue.arrayUnion(uid))
                                .addOnSuccessListener {
                                    // Update user's groupID and organizationName
                                    db.collection("users").document(uid)
                                        .update(
                                            mapOf(
                                                "groupID" to groupCode,
                                                "organizationName" to orgName
                                            )
                                        )
                                        .addOnSuccessListener {
                                            isLoading = false
                                            onSuccess()
                                        }
                                        .addOnFailureListener { e ->
                                            isLoading = false
                                            errorMessage = e.message ?: "Failed to update user"
                                        }
                                }
                                .addOnFailureListener { e ->
                                    isLoading = false
                                    errorMessage = e.message ?: "Failed to join group"
                                }
                        }
                        .addOnFailureListener { e ->
                            isLoading = false
                            errorMessage = e.message ?: "Failed to find group"
                        }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading
            ) {
                Text(if (isLoading) "Joining Group..." else "Join Group")
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