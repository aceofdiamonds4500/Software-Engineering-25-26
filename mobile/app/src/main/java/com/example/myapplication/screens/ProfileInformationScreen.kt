package com.example.myapplication
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch



@Composable
fun ProfileInformationScreen(
    onBack: () -> Unit,
) {
    var username by remember { mutableStateOf("") } // shoudl use these instead
    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }
    var sampleName by remember { mutableStateOf("") } // remopve

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

    Column (modifier = Modifier
        .fillMaxSize()
        .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),

    ) {
        Image(
            painter = painterResource(id = R.drawable.profilepicture), // change this
            contentDescription = "Profile Picture",
            modifier = Modifier
                .size(120.dp)
                .align(Alignment.CenterHorizontally)
        )

        Button(
            onClick = { // bruh
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Change Profile Picture")
        }

        TextField(
            value = sampleName,
            onValueChange = { sampleName = it },
            label = { Text("Profile Name") }, // instead of name make like username then have options to change first last name dob etc....
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors
        )

        TextField(
            value = sampleName,
            onValueChange = { sampleName = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors
        )

        TextField(
            value = sampleName,
            onValueChange = { sampleName = it },
            label = { Text("Date of Birth [mm/dd/yyyy]") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
            colors = tfColors
        )


        Button(
            onClick = { /* Apply settings if you want */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Save Changes")
        }

        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }
    }
}