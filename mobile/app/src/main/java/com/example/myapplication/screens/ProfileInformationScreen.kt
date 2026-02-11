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
            modifier = Modifier.fillMaxWidth()
        )

        TextField(
            value = sampleName,
            onValueChange = { sampleName = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth()
        )

        TextField(
            value = sampleName,
            onValueChange = { sampleName = it },
            label = { Text("Date of Birth [mm/dd/yyyy]") },
            modifier = Modifier.fillMaxWidth()
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