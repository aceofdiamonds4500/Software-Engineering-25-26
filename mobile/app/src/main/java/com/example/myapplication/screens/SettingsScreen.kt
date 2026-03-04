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
    enlargeText: Boolean,
    onDarkModeChange: (Boolean) -> Unit,
    onEnlargeTextChange: (Boolean) -> Unit,
    onAccountSettingsClick: () -> Unit
) {
    var tempDarkMode by remember { mutableStateOf(isDarkMode) }
    var tempEnlargeText by remember { mutableStateOf(enlargeText) }

    fun applySettings() {
        onDarkModeChange(tempDarkMode)
        onEnlargeTextChange(tempEnlargeText)
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
            Text("Enlarge Font Size")
            Spacer(modifier = Modifier.weight(1f))
            Switch(
                checked = tempEnlargeText,
                onCheckedChange = { tempEnlargeText = it }
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
                tempEnlargeText = false
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