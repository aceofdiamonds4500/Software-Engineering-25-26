package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.HistoricalChange
import androidx.compose.ui.unit.dp
import com.example.myapplication.screens.HistoryScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch

// ✅ Your colors
val AppBackground = Color(220, 224, 228)
val DrawerBackground = Color(210, 214, 218)
val TextDark = Color(30, 30, 30)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                DrawerApp()
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DrawerApp() {
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()
    var currentScreen by remember { mutableStateOf("Home") }

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet(
                modifier = Modifier.width(170.dp),
                drawerContainerColor = Color(210, 232, 247)
            ) {
                Spacer(Modifier.height(24.dp))
                Text(
                    text = "Menu",
                    style = MaterialTheme.typography.headlineSmall,
                    color = TextDark,
                    modifier = Modifier.padding(16.dp)
                )

                DrawerItem("Home") {
                    currentScreen = "Home"
                    scope.launch { drawerState.close() }
                }
                DrawerItem("Transcribe") {
                    currentScreen = "Transcribe"
                    scope.launch { drawerState.close() }
                }
                DrawerItem("History") {
                    currentScreen = "History"
                    scope.launch { drawerState.close() }
                }
                DrawerItem("Settings") {
                    currentScreen = "Settings"
                    scope.launch { drawerState.close() }
                }
            }
        }
    ) {
        Scaffold(
            containerColor = AppBackground,
            topBar = {
                TopAppBar(
                    title = { Text("Transcriptive AI", color = TextDark) },
                    navigationIcon = {
                        IconButton(onClick = {
                            scope.launch { drawerState.open() }
                        }) {
                            Icon(
                                Icons.Default.Menu,
                                contentDescription = "Menu",
                                tint = TextDark
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = Color(123, 170, 224)

                    )
                )
            }
        ) { padding ->
            Box(
                modifier = Modifier
                    .fillMaxSize()                           // HERE ADD MODIFIERS RIGHT HERE LOOK!
                    .background(AppBackground)
                    .padding(padding)
                    .verticalScroll(rememberScrollState()) // this only scrollable if content larger tahan page.
            ) {
                when (currentScreen) {
                    "Home" -> HomeScreen()
                    "Transcribe" -> TranscribeScreen()
                    "History" -> HistoryScreen()
                    "Settings" -> SettingsScreen()
                }
            }
        }
    }
}

@Composable
fun DrawerItem(label: String, onClick: () -> Unit) {
    Text(
        text = label,
        style = MaterialTheme.typography.bodyLarge,
        color = TextDark,
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(16.dp)
    )
}

