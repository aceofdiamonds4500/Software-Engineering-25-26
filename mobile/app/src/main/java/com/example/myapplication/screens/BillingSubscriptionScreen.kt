package com.example.myapplication

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
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
fun BillingSubscriptionScreen(
    onBack: () -> Unit,
) {
    val SubscriptionPlans = listOf(
        "Trial [FREE FOR 7 DAYS]",
        "Basic [$49.99 / MONTH]",
        "Pro [$149.99 / MONTH]",
        "Enterprise [$999.99 / MONTH]",
    )

    val BillingCycle = listOf(
        "Monthly",
        "Quartly",
        "Bi-Yearly",
        "Yearly"
    )

    var expanded by remember { mutableStateOf(false) }
    var expanded2 by remember { mutableStateOf(false) }
    var selectedSubscriptionPlan by remember {  mutableStateOf(SubscriptionPlans[0]) }
    var selectedBillingCycle by remember {  mutableStateOf(BillingCycle[0]) }


    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {

        // Subscription PLans dropdonw
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = { expanded = !expanded }
        ) {
            OutlinedTextField(
                value = selectedSubscriptionPlan,
                onValueChange = {}, // readOnly
                readOnly = true,
                label = { Text("Select a Plan") },
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
                SubscriptionPlans.forEach { plans ->
                    DropdownMenuItem(
                        text = { Text(plans) },
                        onClick = {
                            selectedSubscriptionPlan = plans
                            expanded = false
                        }
                    )
                }
            }
        }

        // Billing Cycle
        ExposedDropdownMenuBox(
            expanded = expanded2,
            onExpandedChange = { expanded2 = !expanded2 }
        ) {
            OutlinedTextField(
                value = selectedBillingCycle,
                onValueChange = {},
                readOnly = true,
                label = { Text("Select a Billing Cycle") },
                trailingIcon = {
                    ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded2)
                },
                modifier = Modifier
                    .menuAnchor()
                    .fillMaxWidth()
            )

            ExposedDropdownMenu(
                expanded = expanded2,
                onDismissRequest = { expanded2 = false }
            ) {
                BillingCycle.forEach { cycle ->
                    DropdownMenuItem(
                        text = { Text(cycle) },
                        onClick = {
                            selectedBillingCycle = cycle
                            expanded2 = false
                        }
                    )
                }
            }
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
