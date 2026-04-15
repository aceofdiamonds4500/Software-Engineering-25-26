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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.myapplication.screens.AccountSettingsScreen
import com.example.myapplication.screens.HistoryScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import coil.compose.AsyncImage
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.launch
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {

            var isDarkMode by remember { mutableStateOf(false) }
            var isEnlargeText by remember { mutableStateOf(false) }

            MyApplicationTheme(
                darkTheme = isDarkMode,
                enlargeText = isEnlargeText
            ) {
                var screen by remember { mutableStateOf("WELCOME") }

                when (screen) {
                    "WELCOME" -> WelcomeScreen(
                        onLoginClick = { screen = "LOGIN" },
                        onRegisterClick = { screen = "REGISTER" },
                        onSkipClick = { screen = "MAIN" }
                    )
                    "LOGIN" -> LoginFormScreen(
                        onBack = { screen = "WELCOME" },
                        onSuccess = { screen = "MAIN" },
                        onForgotClick = { screen = "FORGOT"}
                    )
                    "FORGOT" -> ForgotPasswordScreen(
                        onBack = { screen = "LOGIN" },
                        onSuccess = { screen = "LOGIN" }
                    )
                    "REGISTER" -> RegisterScreen(
                        onBack = { screen = "WELCOME" },
                        onSuccess = { screen = "MAIN" },
                        onTermsClick = { screen = "TERMS" }
                    )
                    "TERMS" -> TermsOfService(
                        onBack = { screen = "REGISTER" }
                    )
                    "MAIN" -> DrawerApp(
                        onLogout = { screen = "WELCOME" },
                        isDarkMode = isDarkMode,
                        enlargeText = isEnlargeText,
                        onDarkModeChange = { isDarkMode = it },
                        onEnlargeTextChange = { isEnlargeText = it }
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
    enlargeText: Boolean,
    onDarkModeChange: (Boolean) -> Unit,
    onEnlargeTextChange: (Boolean) -> Unit
) {
    val drawerState = rememberDrawerState(DrawerValue.Closed)
    val scope = rememberCoroutineScope()

    var currentScreen by remember { mutableStateOf("Home") }
    var profilePicUrl by remember { mutableStateOf<String?>(null) }
    var userName by remember { mutableStateOf("") }
    var adminStatus by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        val uid = FirebaseAuth.getInstance().currentUser?.uid
        if (uid != null) {
            FirebaseFirestore.getInstance()
                .collection("users")
                .document(uid)
                .get()
                .addOnSuccessListener { doc ->
                    profilePicUrl = doc.getString("profilePicUrl")
                    userName = doc.getString("FirstnameLastname") ?: ""
                    adminStatus = doc.getLong("admin")?.toString() ?: ""
                }
        }
    }

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet(
                modifier = Modifier.width(280.dp),
                drawerContainerColor = MaterialTheme.colorScheme.surface
            ) {
                // Header
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.primary)
                        .padding(vertical = 24.dp, horizontal = 16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        // Same pfp logic as ProfileInformationScreen
                        if (profilePicUrl != null) {
                            AsyncImage(
                                model = profilePicUrl,
                                contentDescription = "Profile Picture",
                                modifier = Modifier
                                    .size(90.dp)
                                    .clip(CircleShape),
                                contentScale = ContentScale.Crop
                            )
                        } else {
                            Image(
                                painter = painterResource(id = R.drawable.profilepicture),
                                contentDescription = "Profile Picture",
                                modifier = Modifier
                                    .size(90.dp)
                                    .clip(CircleShape),
                                contentScale = ContentScale.Crop
                            )
                        }
                        Text(
                            text = "Welcome back, $userName",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onPrimary,
                            textAlign = TextAlign.Center
                        )
                    }
                }

                Spacer(Modifier.height(12.dp))

                Text(
                    text = "MENU",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
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
                if (adminStatus == "1"){
                    DrawerItem("Admin Panel") {
                        currentScreen = "Admin Panel"
                        scope.launch { drawerState.close() }
                    }
                }

                Spacer(Modifier.weight(1f))

                HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp))

                Button(
                    onClick = {
                        onLogout()
                        scope.launch { drawerState.close() }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.error
                    )
                ) {
                    Text("Log Out", color = MaterialTheme.colorScheme.onError)
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
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
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
            ) {
                when (currentScreen) {
                    "Home" -> HomeScreen()
                    "Transcribe" -> TranscribeScreen()
                    "History" -> HistoryScreen()
                    "Settings" -> SettingsScreen(
                        isDarkMode = isDarkMode,
                        enlargeText = enlargeText,
                        onDarkModeChange = onDarkModeChange,
                        onEnlargeTextChange = onEnlargeTextChange,
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
                        onBack = { currentScreen = "AccountSettings" },
                        onNameChange = { userName = it },
                        onPicChange = { profilePicUrl = it }
                    )
                    "Security" -> SecurityScreen(onBack = { currentScreen = "AccountSettings" })
                    "PrivacyData" -> PrivacyDataScreen(onBack = { currentScreen = "AccountSettings" })
                    "TranscriptionPreferences" -> TranscriptionPreferencesScreen(onBack = { currentScreen = "AccountSettings" })
                    "BillingSubscription" -> BillingSubscriptionScreen(onBack = { currentScreen = "AccountSettings" })
                    "Payments" -> PaymentsScreen(onBack = { currentScreen = "AccountSettings" })
                    "SupportLegal" -> SupportLegalScreen(onBack = { currentScreen = "AccountSettings" })
                }
            }
        }
    }
}

// each drawer item properties
@Composable
fun DrawerItem(label: String, onClick: () -> Unit) {
    TextButton(
        onClick = onClick,
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp)
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Start
        )
    }
}