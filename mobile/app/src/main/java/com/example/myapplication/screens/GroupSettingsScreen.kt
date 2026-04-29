package com.example.myapplication

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.unit.dp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore

data class GroupMember(
    val name: String,
    val isAdmin: Boolean
)

@Composable
fun GroupSettingsScreen(
    onBack: () -> Unit,
    onLeaveGroup: () -> Unit
) {
    val auth = FirebaseAuth.getInstance()
    val db = FirebaseFirestore.getInstance()
    val clipboard = LocalClipboardManager.current

    var groupID by remember { mutableStateOf("") }
    var organizationName by remember { mutableStateOf("") }
    var members by remember { mutableStateOf<List<GroupMember>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf("") }
    var showLeaveDialog by remember { mutableStateOf(false) }
    var notInGroup by remember { mutableStateOf(false) }

    // Join group state
    var groupCodeInput by remember { mutableStateOf("") }
    var isJoining by remember { mutableStateOf(false) }
    var joinError by remember { mutableStateOf("") }

    fun loadGroup(uid: String) {
        db.collection("users").document(uid).get()
            .addOnSuccessListener { userDoc ->
                groupID = userDoc.getString("groupID") ?: ""
                organizationName = userDoc.getString("organizationName") ?: ""

                if (groupID.isEmpty()) {
                    isLoading = false
                    notInGroup = true
                    return@addOnSuccessListener
                }

                notInGroup = false

                db.collection("groups").document(groupID).get()
                    .addOnSuccessListener { groupDoc ->
                        val memberUids = groupDoc.get("members") as? List<*> ?: emptyList<String>()

                        if (memberUids.isEmpty()) {
                            isLoading = false
                            return@addOnSuccessListener
                        }

                        val fetchedMembers = mutableListOf<GroupMember>()
                        var fetched = 0

                        memberUids.forEach { memberUid ->
                            db.collection("users").document(memberUid.toString()).get()
                                .addOnSuccessListener { memberDoc ->
                                    val name = memberDoc.getString("FirstnameLastname") ?: "Unknown"
                                    val isAdmin = memberDoc.getLong("admin") == 1L
                                    fetchedMembers.add(GroupMember(name, isAdmin))
                                    fetched++
                                    if (fetched == memberUids.size) {
                                        members = fetchedMembers.sortedByDescending { it.isAdmin }
                                        isLoading = false
                                    }
                                }
                                .addOnFailureListener {
                                    fetched++
                                    if (fetched == memberUids.size) {
                                        members = fetchedMembers.sortedByDescending { it.isAdmin }
                                        isLoading = false
                                    }
                                }
                        }
                    }
                    .addOnFailureListener { e ->
                        isLoading = false
                        errorMessage = e.message ?: "Failed to load group"
                    }
            }
            .addOnFailureListener { e ->
                isLoading = false
                errorMessage = e.message ?: "Failed to load user"
            }
    }

    LaunchedEffect(Unit) {
        val uid = auth.currentUser?.uid ?: return@LaunchedEffect
        loadGroup(uid)
    }

    if (showLeaveDialog) {
        AlertDialog(
            onDismissRequest = { showLeaveDialog = false },
            title = { Text("Leave Group") },
            text = { Text("Are you sure you want to leave $organizationName?") },
            confirmButton = {
                TextButton(onClick = {
                    showLeaveDialog = false
                    val uid = auth.currentUser?.uid ?: return@TextButton

                    db.collection("groups").document(groupID)
                        .update("members", FieldValue.arrayRemove(uid))

                    db.collection("users").document(uid)
                        .update(mapOf(
                            "groupID" to "",
                            "organizationName" to ""
                        ))
                        .addOnSuccessListener { onLeaveGroup() }
                }) {
                    Text("Leave", color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = {
                TextButton(onClick = { showLeaveDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        if (isLoading) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
            return@Column
        }

        if (errorMessage.isNotEmpty()) {
            Text(text = errorMessage, color = MaterialTheme.colorScheme.error)
        }

        if (notInGroup) {
            Text(
                text = "Group Settings",
                style = MaterialTheme.typography.headlineSmall
            )

            Text(
                text = "You are not in a group",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
            )

            HorizontalDivider()

            Text("Join a Group", style = MaterialTheme.typography.titleMedium)

            TextField(
                value = groupCodeInput,
                onValueChange = { groupCodeInput = it.uppercase() },
                label = { Text("Group Code") },
                modifier = Modifier.fillMaxWidth()
            )

            if (joinError.isNotEmpty()) {
                Text(text = joinError, color = MaterialTheme.colorScheme.error)
            }

            Button(
                onClick = {
                    if (groupCodeInput.isBlank()) {
                        joinError = "Please enter a group code"
                        return@Button
                    }

                    isJoining = true
                    joinError = ""

                    val uid = auth.currentUser?.uid
                    if (uid == null) {
                        joinError = "Not logged in"
                        isJoining = false
                        return@Button
                    }

                    db.collection("groups").document(groupCodeInput).get()
                        .addOnSuccessListener { doc ->
                            if (!doc.exists()) {
                                isJoining = false
                                joinError = "Group not found"
                                return@addOnSuccessListener
                            }

                            val orgName = doc.getString("organizationName") ?: ""

                            db.collection("groups").document(groupCodeInput)
                                .update("members", FieldValue.arrayUnion(uid))
                                .addOnSuccessListener {
                                    db.collection("users").document(uid)
                                        .update(mapOf(
                                            "groupID" to groupCodeInput,
                                            "organizationName" to orgName
                                        ))
                                        .addOnSuccessListener {
                                            isJoining = false
                                            groupCodeInput = ""
                                            isLoading = true
                                            loadGroup(uid) // reload screen with group info
                                        }
                                        .addOnFailureListener { e ->
                                            isJoining = false
                                            joinError = e.message ?: "Failed to update user"
                                        }
                                }
                                .addOnFailureListener { e ->
                                    isJoining = false
                                    joinError = e.message ?: "Failed to join group"
                                }
                        }
                        .addOnFailureListener { e ->
                            isJoining = false
                            joinError = e.message ?: "Failed to find group"
                        }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isJoining
            ) {
                Text(if (isJoining) "Joining..." else "Join Group")
            }

        } else {
            // In a group — show group info
            Text(
                text = organizationName,
                style = MaterialTheme.typography.headlineSmall
            )

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "Group Code: $groupID",
                    style = MaterialTheme.typography.bodyLarge
                )
                Button(onClick = {
                    clipboard.setText(AnnotatedString(groupID))
                }) {
                    Text("Copy")
                }
            }

            HorizontalDivider()

            Text("Members", style = MaterialTheme.typography.titleMedium)

            LazyColumn(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(members) { member ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = member.name,
                            style = MaterialTheme.typography.bodyLarge
                        )
                        Text(
                            text = if (member.isAdmin) "Admin" else "User",
                            style = MaterialTheme.typography.bodySmall,
                            color = if (member.isAdmin)
                                MaterialTheme.colorScheme.primary
                            else
                                MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                        )
                    }
                }
            }

            Button(
                onClick = { showLeaveDialog = true },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.error
                )
            ) {
                Text("Leave Group", color = MaterialTheme.colorScheme.onError)
            }
        }

        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }
    }
}