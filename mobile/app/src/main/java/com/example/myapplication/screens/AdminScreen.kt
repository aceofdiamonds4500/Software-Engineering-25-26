package com.example.myapplication.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.myapplication.TranscriptionItem
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.gson.Gson

data class UserWithTranscriptions(
    val uid: String,
    val name: String,
    val email: String,
    val transcriptions: List<TranscriptionItem>
)

@Composable
fun AdminScreen() {
    val db = FirebaseFirestore.getInstance()
    val auth = FirebaseAuth.getInstance()

    var users by remember { mutableStateOf<List<UserWithTranscriptions>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf("") }
    var groupName by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        val uid = auth.currentUser?.uid
        if (uid == null) {
            errorMessage = "Not logged in"
            isLoading = false
            return@LaunchedEffect
        }

        // Step 1: Get admin's groupID
        db.collection("users").document(uid).get()
            .addOnSuccessListener { adminDoc ->
                val groupID = adminDoc.getString("groupID") ?: ""
                groupName = adminDoc.getString("organizationName") ?: ""

                if (groupID.isEmpty()) {
                    errorMessage = "You are not in a group"
                    isLoading = false
                    return@addOnSuccessListener
                }

                // Step 2: Get group members list
                db.collection("groups").document(groupID).get()
                    .addOnSuccessListener { groupDoc ->
                        val memberUids = groupDoc.get("members") as? List<*> ?: emptyList<String>()

                        if (memberUids.isEmpty()) {
                            isLoading = false
                            return@addOnSuccessListener
                        }

                        val result = mutableListOf<UserWithTranscriptions>()
                        var completed = 0
                        val total = memberUids.size

                        // Step 3: Fetch each member's info and transcriptions
                        memberUids.forEach { memberUid ->
                            val memberUidStr = memberUid.toString()

                            db.collection("users").document(memberUidStr).get()
                                .addOnSuccessListener { userDoc ->
                                    val name = userDoc.getString("FirstnameLastname") ?: "Unknown"
                                    val email = userDoc.getString("email") ?: "Unknown"

                                    db.collection("users").document(memberUidStr)
                                        .collection("transcriptions").get()
                                        .addOnSuccessListener { transDocs ->
                                            val transcriptions = transDocs.mapNotNull { doc ->
                                                val json = doc.getString("data") ?: return@mapNotNull null
                                                runCatching { Gson().fromJson(json, TranscriptionItem::class.java) }.getOrNull()
                                            }
                                            result.add(UserWithTranscriptions(memberUidStr, name, email, transcriptions))
                                            completed++
                                            if (completed == total) {
                                                users = result.sortedBy { it.name }
                                                isLoading = false
                                            }
                                        }
                                        .addOnFailureListener {
                                            result.add(UserWithTranscriptions(memberUidStr, name, email, emptyList()))
                                            completed++
                                            if (completed == total) {
                                                users = result.sortedBy { it.name }
                                                isLoading = false
                                            }
                                        }
                                }
                                .addOnFailureListener {
                                    completed++
                                    if (completed == total) {
                                        users = result.sortedBy { it.name }
                                        isLoading = false
                                    }
                                }
                        }
                    }
                    .addOnFailureListener { e ->
                        errorMessage = e.message ?: "Failed to load group"
                        isLoading = false
                    }
            }
            .addOnFailureListener { e ->
                errorMessage = e.message ?: "Failed to load admin data"
                isLoading = false
            }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
    ) {
        Text(
            text = "Admin Panel",
            style = MaterialTheme.typography.headlineSmall,
            modifier = Modifier.padding(bottom = 4.dp)
        )
        if (groupName.isNotEmpty()) {
            Text(
                text = groupName,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                modifier = Modifier.padding(bottom = 12.dp)
            )
        }

        when {
            isLoading -> Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) { CircularProgressIndicator() }

            errorMessage.isNotEmpty() -> Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) { Text(text = errorMessage, color = Color.Red) }

            users.isEmpty() -> Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "No users found in this group.",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f)
                )
            }

            else -> LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                items(users) { user ->
                    ExpandableUserCard(user)
                }
            }
        }
    }
}

@Composable
fun ExpandableUserCard(user: UserWithTranscriptions) {
    var expanded by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { expanded = !expanded },
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = user.name,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = user.email,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                    )
                }
                Text(
                    text = if (expanded) "▲" else "▼",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                )
            }

            Text(
                text = "${user.transcriptions.size} transcription${if (user.transcriptions.size != 1) "s" else ""}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.primary
            )

            AnimatedVisibility(visible = expanded) {
                Column(
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.padding(top = 8.dp)
                ) {
                    HorizontalDivider()

                    if (user.transcriptions.isEmpty()) {
                        Text(
                            text = "No transcriptions.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                        )
                    } else {
                        user.transcriptions.forEach { item ->
                            ExpandableTranscriptionCard(item)
                            Spacer(Modifier.height(4.dp))
                        }
                    }
                }
            }
        }
    }
}