package com.example.myapplication

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun SettingsScreen(
    isDarkMode: Boolean,
    onDarkModeChange: (Boolean) -> Unit,
    onAccountSettingsClick: () -> Unit
) {

    var tempDarkMode by remember { mutableStateOf(isDarkMode) }
    var enlargeText by remember { mutableStateOf(false) }

    // Reusable apply function
    fun applySettings() {
        onDarkModeChange(tempDarkMode)
    }

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
            Switch(
                checked = tempDarkMode,
                onCheckedChange = { tempDarkMode = it }
            )
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Enlarge Text")
            Spacer(modifier = Modifier.weight(1f))
            Switch(
                checked = enlargeText,
                onCheckedChange = { enlargeText = it }
            )
        }

        Button(
            onClick = { applySettings() },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Apply Settings")
        }

        Button(
            onClick = {
                tempDarkMode = false
                enlargeText = false
                applySettings()
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
