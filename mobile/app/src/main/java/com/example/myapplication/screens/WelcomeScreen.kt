package com.example.myapplication

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp

@Composable
fun WelcomeScreen(
    onLoginClick: () -> Unit,
    onRegisterClick: () -> Unit,
    onSkipClick: () -> Unit
) {
    Box(modifier = Modifier.fillMaxSize()) {

        Image(
            painter = painterResource(id = R.drawable.logo),
            contentDescription = "Logo",
            modifier = Modifier
                .size(200.dp)
                .align(Alignment.TopCenter)
                .offset(y = 160.dp)
        )

        Column(
            modifier = Modifier.align(Alignment.Center),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Button(onClick = onRegisterClick) { Text("Register") }
            Button(onClick = onLoginClick) { Text("Login") }
        }

        // REMOVE IN FUTURE OR CHANGE TO DEMO MODE?
//        TextButton(
//            onClick = onSkipClick,
//            modifier = Modifier
//                .align(Alignment.BottomCenter)
//                .padding(bottom = 16.dp)
//        ) {
//            Text("Maybe Later...")
//        }
    }
}