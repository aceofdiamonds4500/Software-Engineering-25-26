package com.example.myapplication.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun AccountSettingsScreen(
    onBack: () -> Unit,
    onProfileInformationClick: () -> Unit,
    onSecurityClick: () -> Unit,
    onPrivacyDataClick: () -> Unit,
    onTranscriptionPreferencesClick: () -> Unit,
    onBillingSubscriptionClick: () -> Unit,
    onPaymentsClick: () -> Unit,
    onSupportLegalClick: () -> Unit
)
{
    Column (modifier = Modifier
        .fillMaxSize()
        .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)) {

        Button(
            onClick = onProfileInformationClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Profile Information") // user's name, email, phone number, role, organization etc...
        }

        Button(
            onClick = onSecurityClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Security") // change password, enable 2fa enable fingerprint/faceid, pfp, etc....
        }

        Button(
            onClick = onPrivacyDataClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Privacy & Data") // shows what happens to data can download all profile data, transcription history, delete all transcriptions, or delete account
        }

        Button(
            onClick = onTranscriptionPreferencesClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Transcription Preferences") // shows how info would output, autosave switch on/off,
        }

        Button(
            onClick = onBillingSubscriptionClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Billing / Subscription") // different subscriptions like free, basic, pro
        }

        Button(
            onClick =  onPaymentsClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Payment Methods") // payment methods
        }

        Button(
            onClick =  onSupportLegalClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Support & Legal") // get access to support, terms of service, privacy policy, report bugs, app version etc.....
        }


        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }

    }



}