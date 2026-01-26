package com.example.myapplication

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun SettingsScreen(
    onAccountSettingsClick: () -> Unit
) {
    var darkMode by remember { mutableStateOf(false) }
    var enlargeText by remember { mutableStateOf(false) }
    var testSwitch by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Dark Mode")
            Spacer(modifier = Modifier.weight(1f))
            Switch(checked = darkMode, onCheckedChange = { darkMode = it })
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Enlarge Text")
            Spacer(modifier = Modifier.weight(1f))
            Switch(checked = enlargeText, onCheckedChange = { enlargeText = it })
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Test Switch")
            Spacer(modifier = Modifier.weight(1f))
            Switch(checked = testSwitch, onCheckedChange = { testSwitch = it })
        }

        Button(
            onClick = { /* Apply settings if you want */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Apply Settings")
        }

        Button(
            onClick = {
                darkMode = false
                enlargeText = false
                testSwitch = false
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Reset To Default Settings")
        }

        Button(
            onClick = onAccountSettingsClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Account Settings")
        }
    }
}
