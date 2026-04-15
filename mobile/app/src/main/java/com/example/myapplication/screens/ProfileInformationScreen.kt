package com.example.myapplication

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.google.firebase.auth.EmailAuthProvider
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

@Composable
fun ProfileInformationScreen(
    onBack: () -> Unit,
    onNameChange: (String) -> Unit = {},
    onPicChange: (String?) -> Unit = {},
) {
    val auth = FirebaseAuth.getInstance()
    val db = FirebaseFirestore.getInstance()
    val storage = FirebaseStorage.getInstance()
    val scope = rememberCoroutineScope()
    var firstNamelastName by remember { mutableStateOf("") }
    var currentPassword by remember { mutableStateOf("") }
    var newPassword by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var profilePicUrl by remember { mutableStateOf<String?>(null) }
    var selectedImageUri by remember { mutableStateOf<Uri?>(null) }
    var isLoading by remember { mutableStateOf(false) }
    var successMessage by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }
    val uid = auth.currentUser?.uid
    val userEmail = auth.currentUser?.email ?: ""

    // Load existing profile data
    LaunchedEffect(Unit) {
        if (uid != null) {
            db.collection("users").document(uid).get()
                .addOnSuccessListener { doc ->
                    firstNamelastName = doc.getString("FirstnameLastname") ?: ""
                    profilePicUrl = doc.getString("profilePicUrl")
                }
        }
    }

    // Image picker launcher
    val imagePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        selectedImageUri = uri
        successMessage = ""
        errorMessage = ""
    }

    val shape = RoundedCornerShape(12.dp)

    // theme stuff copied and pasted
    val tfColors = TextFieldDefaults.colors(
        focusedContainerColor = MaterialTheme.colorScheme.surface,
        unfocusedContainerColor = MaterialTheme.colorScheme.surface,
        disabledContainerColor = MaterialTheme.colorScheme.surface,
        focusedTextColor = MaterialTheme.colorScheme.onSurface,
        unfocusedTextColor = MaterialTheme.colorScheme.onSurface,
        disabledTextColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
        focusedLabelColor = MaterialTheme.colorScheme.onSurface,
        unfocusedLabelColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
        cursorColor = MaterialTheme.colorScheme.primary,
        focusedIndicatorColor = Color.Transparent,
        unfocusedIndicatorColor = Color.Transparent,
        disabledIndicatorColor = Color.Transparent
    )

    fun saveChanges() {
        if (uid == null) return

        // validates password to make sure they match
        val changingPassword = newPassword.isNotBlank() || confirmPassword.isNotBlank()
        if (changingPassword) {
            if (currentPassword.isBlank()) {
                errorMessage = "Enter your current password to change it."
                successMessage = ""
                return
            }
            if (newPassword != confirmPassword) {
                errorMessage = "New passwords do not match."
                successMessage = ""
                return
            }
            if (newPassword.length < 6) {
                errorMessage = "New password must be at least 6 characters."
                successMessage = ""
                return
            }
        }

        isLoading = true
        errorMessage = ""
        successMessage = ""

        scope.launch {
            try {
                // upload pfp if one is selected
                var finalPicUrl = profilePicUrl
                if (selectedImageUri != null) {
                    val ref = storage.reference.child("profilePictures/$uid.jpg")
                    ref.putFile(selectedImageUri!!).await()
                    finalPicUrl = ref.downloadUrl.await().toString()
                }

                // Update Firestore n/ new name
                db.collection("users").document(uid)
                    .update(
                        mapOf(
                            "FirstnameLastname" to firstNamelastName,
                            "profilePicUrl" to finalPicUrl
                        )
                    ).await()

                // Change password if requested
                if (changingPassword) {
                    val user = auth.currentUser!!
                    val credential = EmailAuthProvider.getCredential(userEmail, currentPassword)
                    user.reauthenticate(credential).await()
                    user.updatePassword(newPassword).await()
                    // Clear password fields after succes
                    currentPassword = ""
                    newPassword = ""
                    confirmPassword = ""
                }

                profilePicUrl = finalPicUrl
                selectedImageUri = null
                successMessage = "Changes saved successfully."
                onNameChange(firstNamelastName)   // update sidebar name live
                onPicChange(finalPicUrl)           // update sidebar pfp live
            } catch (e: Exception) {
                errorMessage = when {
                    e.message?.contains("password") == true ||
                            e.message?.contains("credential") == true ->
                        "Current password is incorrect."
                    else -> "Something went wrong. Please try again."
                }
            } finally {
                isLoading = false
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {

        // profile picture
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {

            when {
                selectedImageUri != null -> {
                    AsyncImage(
                        model = selectedImageUri,
                        contentDescription = "Profile Picture",
                        modifier = Modifier
                            .size(100.dp)
                            .clip(CircleShape),
                        contentScale = ContentScale.Crop
                    )
                }
                profilePicUrl != null -> {
                    AsyncImage(
                        model = profilePicUrl,
                        contentDescription = "Profile Picture",
                        modifier = Modifier
                            .size(100.dp)
                            .clip(CircleShape),
                        contentScale = ContentScale.Crop
                    )
                }
                else -> {
                    Image(
                        painter = painterResource(id = R.drawable.profilepicture),
                        contentDescription = "Profile Picture",
                        modifier = Modifier
                            .size(100.dp)
                            .clip(CircleShape),
                        contentScale = ContentScale.Crop
                    )
                }
            }

            Button(
                onClick = { imagePickerLauncher.launch("image/*") },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Change Profile Picture")
            }
        }

        // name stuff and also joins name to single var
        val parts = firstNamelastName.split(" ", limit = 2)
        val displayFirst = parts.getOrElse(0) { "" }
        val displayLast  = parts.getOrElse(1) { "" }

        TextField(
            value = displayFirst,
            onValueChange = {
                firstNamelastName = "$it $displayLast".trim()
                successMessage = ""
                errorMessage = ""
            },
            label = { Text("First Name") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors,
            singleLine = true
        )

        TextField(
            value = displayLast,
            onValueChange = {
                firstNamelastName = "$displayFirst $it".trim()
                successMessage = ""
                errorMessage = ""
            },
            label = { Text("Last Name") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors,
            singleLine = true
        )

        // password stuff
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = "Change Password",
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
        )

        TextField(
            value = currentPassword,
            onValueChange = {
                currentPassword = it
                successMessage = ""
                errorMessage = ""
            },
            label = { Text("Current Password") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors,
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
        )

        TextField(
            value = newPassword,
            onValueChange = {
                newPassword = it
                successMessage = ""
                errorMessage = ""
            },
            label = { Text("New Password") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors,
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
        )

        TextField(
            value = confirmPassword,
            onValueChange = {
                confirmPassword = it
                successMessage = ""
                errorMessage = ""
            },
            label = { Text("Confirm New Password") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors,
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
        )

        Spacer(modifier = Modifier.height(4.dp))

        // save button
        Button(
            onClick = { saveChanges() },
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
                Text("Save Changes")
            }
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

        // back button
        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }
    }
}