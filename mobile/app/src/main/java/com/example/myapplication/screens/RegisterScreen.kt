package com.example.myapplication

//import android.util.Log
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.input.PasswordVisualTransformation
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.width
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.net.Uri
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale

@Composable
fun RegisterScreen(
    onBack: () -> Unit,
    onSuccess: () -> Unit,
    onTermsClick: () -> Unit
) {
    // State should live OUTSIDE the Column body
    var email by remember { mutableStateOf("") }
    var firstNamelastName by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var checked by remember { mutableStateOf(false) }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }
    var successMessage by remember { mutableStateOf("") }
    val imageUri = remember { mutableStateOf<Uri?>(null) }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        imageUri.value = uri
    }

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

            TextField(
                value = firstNamelastName,
                onValueChange = { firstNamelastName = it },
                label = { Text("First name and Last name") },
                modifier = Modifier.fillMaxWidth()
            )

            TextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth()
            )

            TextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it },
                label = { Text("Confirm Password") },
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth()
            )

            Button(
                onClick = { launcher.launch("image/*") },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Upload Profile Picture")
            }

            imageUri.value?.let { uri ->
                AsyncImage(
                    model = uri,
                    contentDescription = "Profile Picture Preview",
                    modifier = Modifier.size(100.dp),
                    contentScale = ContentScale.Crop
                )
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(
                    checked = checked,
                    onCheckedChange = { checked = it }
                )

                Spacer(Modifier.width(8.dp))

                Text(
                    text = "I agree to the terms",
                    modifier = Modifier.clickable { onTermsClick() },
                    color = MaterialTheme.colorScheme.primary,
                    textDecoration = TextDecoration.Underline
                )
            }

            if (errorMessage.isNotEmpty()) {
                Text(
                    text = errorMessage,
                    color = MaterialTheme.colorScheme.error
                )
            }

            Button(
                onClick = {
                    if (password != confirmPassword) {
                        errorMessage = "Passwords do not match"
                        return@Button
                    }

                    isLoading = true
                    val auth = FirebaseAuth.getInstance()
                    val db = FirebaseFirestore.getInstance()

                    auth.createUserWithEmailAndPassword(email, password)
                        .addOnSuccessListener { result ->
                            val uid = result.user?.uid ?: return@addOnSuccessListener
                            val userDoc = hashMapOf(
                                "FirstnameLastname" to firstNamelastName,
                                "email" to email,
                                "admin" to 0
                            )
                            db.collection("users").document(uid).set(userDoc)
                                .addOnSuccessListener {
                                    val uri = imageUri.value
                                    if (uri != null) {
                                        val storageRef = FirebaseStorage.getInstance()
                                            .reference.child("profile_pictures/$uid/$uid")
                                        storageRef.putFile(uri)
                                            .addOnSuccessListener {
                                                storageRef.downloadUrl.addOnSuccessListener { downloadUrl ->
                                                    db.collection("users").document(uid)
                                                        .update("profilePicUrl", downloadUrl.toString())
                                                    isLoading = false
                                                    successMessage = "Account created!"
                                                }
                                            }
                                            .addOnFailureListener { e ->
                                                isLoading = false
                                                errorMessage = e.message ?: "Failed to upload image"
                                            }
                                    } else {
                                        isLoading = false
                                        //onSuccess()
                                        successMessage = "Account created!"
                                    }
                                }
                                .addOnFailureListener { e ->
                                    isLoading = false
                                    errorMessage = e.message ?: "Failed to save user data"
                                }
                        }
                        .addOnFailureListener { e ->
                            isLoading = false
                            errorMessage = e.message ?: "Registration failed"
                        }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = checked && !isLoading
            ) {
                Text(if (isLoading) "Creating Account..." else "Register")
            }

            Button(
                onClick = onBack,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Back")
            }

            if (successMessage.isNotEmpty()) {
                Text(
                    text = successMessage,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}