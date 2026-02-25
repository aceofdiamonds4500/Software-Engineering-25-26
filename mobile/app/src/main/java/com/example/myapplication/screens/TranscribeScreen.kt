package com.example.myapplication

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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TranscribeScreen() {

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

    var expanded by remember { mutableStateOf(false) }
    var sampleName by remember { mutableStateOf("") }
    var selectedSpecialty by remember { mutableStateOf("") }
    var transcription by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var keywords by remember { mutableStateOf("") }
    var outputText by remember {
        mutableStateOf(
            "Test to make sure i can scroll it\nTest to make sure i can scroll it\nTest to make sure i can scroll it\n" +
                    "Test to make sure i can scroll it\nTest to make sure i can scroll it\nTest to make sure i can scroll it\n" +
                    "Test to make sure i can scroll it\nTest to make sure i can scroll it\nTest to make sure i can scroll it\n"
        )
    }
    val outputScrollState = rememberScrollState()

    val shape = RoundedCornerShape(12.dp)

    // TextField colors that match your theme (works for both light + dark)
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

        // remove the harsh underline look (cleaner on dark mode)
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
            Button(
                onClick = {
                    sampleName = ""
                    transcription = ""
                    description = ""
                    keywords = ""
                    selectedSpecialty = ""
                    outputText = ""
                },
                modifier = Modifier.weight(1f)
            ) { Text("Clear Info") }

            Button(
                onClick = { /* calculate info later */ },
                modifier = Modifier.weight(1f)
            ) { Text("Calculate Info") }
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
