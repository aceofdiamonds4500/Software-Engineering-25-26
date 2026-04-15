package com.example.myapplication
import com.example.myapplication.network.Connection

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.gson.Gson
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

data class TranscriptionItem(
    val id: String = "",
    val title: String = "",
    val date: String = "",
    val preview: String = "",
    val specialty: String = "",
    val transcription: String = "",
    val description: String = "",
    val keywords: String = "",
    val diagnosis: String = ""
)

data class ClassifyFields(
    val Description: String,
    val Transcription: String,
    val Keywords: String
)

data class ClassifyPayload(
    val command: String,
    val timestamp: String,
    val fields: ClassifyFields
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TranscribeScreen() {

    // list of all specialities
    val specialties = listOf(
        "Allergy / Immunology",
        "Bariatrics",
        "Cardiovascular / Pulmonary",
        "Chiropractic",
        "Consult - History and Phy.",
        "Cosmetic / Plastic Surgery",
        "Dentistry",
        "Dermatology",
        "Dietetics / Nutrition",
        "Discharge Summary",
        "Emergency Room Reports",
        "Endocrinology",
        "ENT - Otolaryngology",
        "Family Medicine",
        "Gastroenterology",
        "General Medicine",
        "Hematology - Oncology",
        "Infectious Disease",
        "Internal Medicine",
        "Lab Medicine - Pathology",
        "Letters",
        "Nephrology",
        "Neurology",
        "Neurosurgery",
        "Obstetrics / Gynecology",
        "Office Notes",
        "Ophthalmology",
        "Orthopedic",
        "Pain Management",
        "Pediatrics - Neonatal",
        "Physical Medicine - Rehab",
        "Podiatry",
        "Psychiatry / Psychology",
        "Radiology",
        "Rheumatology",
        "Sleep Medicine",
        "Speech - Language",
        "Surgery",
        "Urology"
    )

    val gson = remember { Gson() }
    var expanded by remember { mutableStateOf(false) }
    var sampleName by remember { mutableStateOf("") }
    var selectedSpecialty by remember { mutableStateOf("") }
    var transcription by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var keywords by remember { mutableStateOf("") }
    var outputText by remember { mutableStateOf("") }
    var saveMessage by remember { mutableStateOf("") }
    var isSaving by remember { mutableStateOf(false) }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf("") }
    var successMessage by remember { mutableStateOf("") }
    val outputScrollState = rememberScrollState()
    val scope = rememberCoroutineScope()
    val shape = RoundedCornerShape(12.dp)

    // theme stuff
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
    val otfColors = OutlinedTextFieldDefaults.colors(
        focusedBorderColor = MaterialTheme.colorScheme.primary,
        unfocusedBorderColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.45f),
        focusedTextColor = MaterialTheme.colorScheme.onSurface,
        unfocusedTextColor = MaterialTheme.colorScheme.onSurface,
        focusedLabelColor = MaterialTheme.colorScheme.onSurface,
        unfocusedLabelColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
        cursorColor = MaterialTheme.colorScheme.primary
    )

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Specialties dropdown box
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = selectedSpecialty,
                onValueChange = {},
                readOnly = true,
                label = { Text("Pick a Specialty") },
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                modifier = Modifier
                    .menuAnchor()
                    .fillMaxWidth(),
                shape = shape,
                colors = otfColors
            )
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                specialties.forEach { specialty ->
                    DropdownMenuItem(
                        text = { Text(specialty) },
                        onClick = {
                            selectedSpecialty = specialty
                            expanded = false
                        }
                    )
                }
            }
        }
        // all input fields to be sent
        TextField(
            value = sampleName,
            onValueChange = { sampleName = it },
            label = { Text("Sample Name") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors
        )
        TextField(
            value = transcription,
            onValueChange = { transcription = it },
            label = { Text("Transcription") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors
        )
        TextField(
            value = description,
            onValueChange = { description = it },
            label = { Text("Description") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors
        )
        TextField(
            value = keywords,
            onValueChange = { keywords = it },
            label = { Text("Keywords") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors
        )

        Spacer(Modifier.height(16.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // clear all fields button
            Button(
                onClick = {
                    sampleName = ""
                    transcription = ""
                    description = ""
                    keywords = ""
                    selectedSpecialty = ""
                    outputText = ""
                    saveMessage = ""
                    successMessage = ""
                    errorMessage = ""
                },
                modifier = Modifier.weight(1f)
            ) { Text("Clear Info") }

            // calculate info button
            Button(
                onClick = {
                    successMessage = ""
                    errorMessage = ""
                    isLoading = true

                    val payload = ClassifyPayload(
                        command = "CLASSIFY",
                        timestamp = System.currentTimeMillis().toString(),
                        fields = ClassifyFields(
                            Description = description,
                            Transcription = transcription,
                            Keywords = keywords
                        )
                    )

                    val json = gson.toJson(payload)

                    scope.launch {
                        try {
                            val result = withContext(Dispatchers.IO) {
                                val connection = Connection("10.0.2.2", 5867)
                                val output = connection.exchangeData(json)
                                connection.exchangeData("""{"command": "DISCONNECT"}""")
                                connection.close()
                                output
                            }
                            outputText = result
                            successMessage = "Classification complete!"
                            errorMessage = ""
                        } catch (e: Exception) {
                            errorMessage = e.message ?: "Failed to connect to server."
                            successMessage = ""
                        } finally {
                            isLoading = false
                        }
                    }
                },
                enabled = !isLoading,
                modifier = Modifier.weight(1f)
            ) {
                Text(if (isLoading) "Thinking..." else "Calculate Info")
            }
        }

        // error/success message
        if (successMessage.isNotEmpty()) {
            Text(
                text = successMessage,
                color = Color.Green
            )
        }
        if (errorMessage.isNotEmpty()) {
            Text(
                text = errorMessage,
                color = MaterialTheme.colorScheme.error
            )
        }

        // Save to Firebase button
        Button(
            onClick = {
                // get current user's account
                val uid = FirebaseAuth.getInstance().currentUser?.uid
                if (uid == null) {
                    saveMessage = "Not logged in."
                    return@Button
                }

                isSaving = true

                // goes to database and adds new transcription
                val db = FirebaseFirestore.getInstance()
                val transcriptionsRef = db.collection("users").document(uid)
                    .collection("transcriptions")

                transcriptionsRef.get().addOnSuccessListener { docs ->
                    val count = docs.size() + 1
                    val date = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())

                    val item = TranscriptionItem(
                        title = "Transcription $count",
                        date = date,
                        preview = transcription.take(100),
                        specialty = selectedSpecialty,
                        transcription = transcription,
                        description = description,
                        keywords = keywords,
                        diagnosis = outputText
                    )

                    val json = gson.toJson(item)

                    transcriptionsRef.add(hashMapOf("data" to json))
                        .addOnSuccessListener {
                            isSaving = false
                            saveMessage = "Saved as Transcription $count!"
                        }
                        .addOnFailureListener { e ->
                            isSaving = false
                            saveMessage = e.message ?: "Failed to save."
                        }
                }.addOnFailureListener { e ->
                    isSaving = false
                    saveMessage = e.message ?: "Failed to count transcriptions."
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isSaving
        ) {
            Text(if (isSaving) "Saving..." else "Save Transcription")
        }

        if (saveMessage.isNotEmpty()) {
            Text(
                text = saveMessage,
                color = if (saveMessage.startsWith("Saved"))
                    MaterialTheme.colorScheme.primary
                else
                    MaterialTheme.colorScheme.error
            )
        }

        Spacer(Modifier.height(24.dp))

        TextField(
            value = outputText,
            onValueChange = {},
            readOnly = true,
            label = { Text("Result") },
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
                .verticalScroll(outputScrollState),
            maxLines = Int.MAX_VALUE,
            shape = shape,
            colors = tfColors
        )
    }
}