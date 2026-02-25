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
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.myapplication.screens.AccountSettingsScreen
import com.example.myapplication.screens.HistoryScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() { // main start
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {

            // App-wide theme toggle state (this is what makes dark mode work)
            var isDarkMode by remember { mutableStateOf(false) }

            MyApplicationTheme(darkTheme = isDarkMode) {

                // Main "auth flow" navigation
                var screen by remember { mutableStateOf("WELCOME") }

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
                        onLogout = { screen = "WELCOME" },
                        isDarkMode = isDarkMode,
                        onDarkModeChange = { isDarkMode = it }
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DrawerApp(
    onLogout: () -> Unit,
    isDarkMode: Boolean,
    onDarkModeChange: (Boolean) -> Unit
) {
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    // Drawer navigation state
    var currentScreen by remember { mutableStateOf("Home") }

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet(
                modifier = Modifier.width(260.dp),
                drawerContainerColor = MaterialTheme.colorScheme.secondary
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
                    color = MaterialTheme.colorScheme.onBackground,
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
            containerColor = MaterialTheme.colorScheme.background,
            topBar = {
                TopAppBar(
                    title = { Text("Transcriptive AI") },
                    navigationIcon = {
                        IconButton(onClick = { scope.launch { drawerState.open() } }) {
                            Icon(
                                Icons.Default.Menu,
                                contentDescription = "Menu"
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                        titleContentColor = MaterialTheme.colorScheme.onPrimary,
                        navigationIconContentColor = MaterialTheme.colorScheme.onPrimary
                    )
                )
            }
        ) { padding ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colorScheme.background)
                    .padding(padding)
                    .verticalScroll(rememberScrollState())
            ) {
                when (currentScreen) {
                    "Home" -> HomeScreen()
                    "Transcribe" -> TranscribeScreen()
                    "History" -> HistoryScreen()

                    "Settings" -> SettingsScreen(
                        isDarkMode = isDarkMode,
                        onDarkModeChange = onDarkModeChange,
                        onAccountSettingsClick = { currentScreen = "AccountSettings" }
                    )

                    "AccountSettings" -> AccountSettingsScreen(
                        onBack = { currentScreen = "Settings" },
                        onProfileInformationClick = { currentScreen = "ProfileInformationScreen" },
                        onSecurityClick = { currentScreen = "Security" },
                        onPrivacyDataClick = { currentScreen = "PrivacyData" },
                        onTranscriptionPreferencesClick = { currentScreen = "TranscriptionPreferences" },
                        onBillingSubscriptionClick = { currentScreen = "BillingSubscription" },
                        onPaymentsClick = { currentScreen = "Payments" },
                        onSupportLegalClick = { currentScreen = "SupportLegal" }
                    )

                    "ProfileInformationScreen" -> ProfileInformationScreen(
                        onBack = { currentScreen = "AccountSettings" }
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
fun DrawerItem(label: String, onClick: () -> Unit) {
    Text(
        text = label,
        style = MaterialTheme.typography.bodyLarge,
        color = MaterialTheme.colorScheme.onBackground,
        textAlign = TextAlign.Center,
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(vertical = 12.dp)
    )
}
