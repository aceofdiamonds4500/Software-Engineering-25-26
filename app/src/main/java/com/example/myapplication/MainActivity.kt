package com.example.myapplication
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.myapplication.screens.HistoryScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch

// colors
val AppBackground = Color(220, 224, 228)
val DrawerBackground = Color(210, 214, 218)
val TextDark = Color(30, 30, 30)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {

                var showMainScreen by remember { mutableStateOf(false) }

                if (showMainScreen) {
                    DrawerApp(
                        onLogout = { showMainScreen = false }
                    )
                } else {
                    LoginScreen(
                        onContinue = { showMainScreen = true }
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DrawerApp(onLogout: () -> Unit) {
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()
    var currentScreen by remember { mutableStateOf("Home") }

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet(
                modifier = Modifier.width(260.dp),
                drawerContainerColor = Color(210, 232, 247)
            ) {
                Spacer(Modifier.height(24.dp))

                // profile image
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp, bottom = 12.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Image(
                        painter = painterResource(id = R.drawable.profilepicture),
                        contentDescription = "Profile Picture",
                        modifier = Modifier.size(120.dp)
                    )
                }

                Spacer(Modifier.height(24.dp))
                Text(
                    text = "Menu",
                    style = MaterialTheme.typography.headlineSmall,
                    color = TextDark,
                    textAlign = TextAlign.Center,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
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
                DrawerItem("Log Out") {
                    onLogout()
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
                        IconButton(onClick = { scope.launch { drawerState.open() } }) {
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
                    .fillMaxSize()
                    .background(AppBackground)
                    .padding(padding)
                    .verticalScroll(rememberScrollState())
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
        textAlign = TextAlign.Center,
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(vertical = 12.dp)
    )
}
