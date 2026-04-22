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
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.myapplication.ui.theme.MyApplicationTheme
import kotlinx.coroutines.launch
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PaymentsScreen(
    onBack: () -> Unit,
) {

    val shape = RoundedCornerShape(12.dp)

    val SubscriptionPlans = listOf(
        "Credit Card",
        "PayPal",
        "Apple Pay",
        "Google Pay"
    )

    var expanded by remember { mutableStateOf(false) }
    var cardName by remember { mutableStateOf("") }
    var cardNumber by remember { mutableStateOf("") }
    var expDate by remember { mutableStateOf("") }
    var cvv by remember { mutableStateOf("") }
    var selectedPayment by remember { mutableStateOf("") }


    Column (modifier = Modifier
        .fillMaxSize()
        .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)) {

        // Subscription PLans dropdonw
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = selectedPayment,
                onValueChange = {}, // readOnly
                readOnly = true,
                label = { Text("Select a Payment Method") },
                trailingIcon = {
                    ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded)
                },
                modifier = Modifier
                    .menuAnchor()
                    .fillMaxWidth()
            )

            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                SubscriptionPlans.forEach { paymentMethod ->
                    DropdownMenuItem(
                        text = { Text(paymentMethod) },
                        onClick = {
                            selectedPayment = paymentMethod
                            expanded = false
                        }
                    )
                }
            }
        }

        TextField(
            value = cardName,
            onValueChange = { cardName = it },
            label = { Text("Name On Card") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
        )

        TextField(
            value = cardNumber,
            onValueChange = { cardNumber = it },
            label = { Text("Card Number") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
        )

        TextField(
            value = expDate,
            onValueChange = { expDate = it },
            label = { Text("Expiration Date") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
        )

        TextField(
            value = cvv,
            onValueChange = { cvv = it },
            label = { Text("CVV") },
            modifier = Modifier.fillMaxWidth(),
            shape = shape,
        )

        Button(
            onClick = {
                // apply settings / save selection if you want
                // e.g., call a ViewModel function here
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Add Card")
        }

        Button(
            onClick = {
                // apply settings / save selection if you want
                // e.g., call a ViewModel function here
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Apply Settings")
        }

        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }
    }
}