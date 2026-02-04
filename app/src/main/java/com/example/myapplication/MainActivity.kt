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
import com.example.myapplication.screens.AccountSettingsScreen
import com.example.myapplication.screens.HistoryScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch

// colors
val AppBackground = Color(220, 224, 228)
val DrawerBackground = Color(210, 214, 218)
val TextDark = Color(30, 30, 30)

class MainActivity : ComponentActivity() {           // main start
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {

                // Main "auth flow" navigation
                var screen by remember { mutableStateOf("WELCOME") }
// this for beginning welcome screen to transition to main page....
                when (screen) {
                    "WELCOME" -> WelcomeScreen(
                        onLoginClick = { screen = "LOGIN" },
                        onRegisterClick = { screen = "REGISTER" },
                        onSkipClick = { screen = "MAIN" }
                    )

                    "LOGIN" -> LoginFormScreen(
                        onBack = { screen = "WELCOME" },
                        onSuccess = { screen = "MAIN" }
                    )

                    "REGISTER" -> RegisterScreen(
                        onBack = { screen = "WELCOME" },
                        onSuccess = { screen = "MAIN" }
                    )

                    // After login/register/skip, everything is handled inside DrawerApp
                    "MAIN" -> DrawerApp(
                        onLogout = { screen = "WELCOME" }
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DrawerApp(onLogout: () -> Unit) {                             // menu this the menu it is menu
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    // Drawer navigation state (includes AccountSettings now)
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
                        painter = painterResource(id = R.drawable.profilepicture), // this changes depending on users pfp??????????
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

                Spacer(Modifier.height(345.dp))

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

                    "Settings" -> SettingsScreen(
                        onAccountSettingsClick = { currentScreen = "AccountSettings" }
                    )

                    "AccountSettings" -> AccountSettingsScreen(
                        onBack = { currentScreen = "Settings" },
                        onProfileInformationClick = { currentScreen = "ProfileInformationScreen"},
                        onSecurityClick = { currentScreen = "Security" },
                        onPrivacyDataClick = { currentScreen = "PrivacyData" },
                        onTranscriptionPreferencesClick = { currentScreen = "TranscriptionPreferences" },
                        onBillingSubscriptionClick = { currentScreen = "BillingSubscription" },
                        onPaymentsClick = { currentScreen = "Payments" }, 
                        onSupportLegalClick = { currentScreen = "SupportLegal" }
                    )

                    "ProfileInformationScreen" -> ProfileInformationScreen(
                        onBack = { currentScreen = "AccountSettings"}
                    )

                    "Security" -> SecurityScreen(
                        onBack = { currentScreen = "AccountSettings" }
                    )

                    "PrivacyData" -> PrivacyDataScreen(
                        onBack = { currentScreen = "AccountSettings" }
                    )

                    "TranscriptionPreferences" -> TranscriptionPreferencesScreen(
                        onBack = { currentScreen = "AccountSettings" }
                    )
                    "BillingSubscription" -> BillingSubscriptionScreen(
                        onBack = { currentScreen = "AccountSettings" }
                    )

                    "Payments" -> PaymentsScreen(
                        onBack = { currentScreen = "AccountSettings" }
                    )

                    "SupportLegal" -> SupportLegalScreen(
                        onBack = { currentScreen = "AccountSettings" }
                    )

                }
            }
        }
    }
}

@Composable
fun DrawerItem(label: String, onClick: () -> Unit) { // what each item in drawer looks like
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
