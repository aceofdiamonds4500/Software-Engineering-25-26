package com.example.myapplication

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import java.text.SimpleDateFormat
import java.util.*

data class TranscriptionData(
    @SerializedName("date")          val date: String = "",
    @SerializedName("title")         val title: String = "",
    @SerializedName("preview")       val preview: String = "",
    @SerializedName("transcription") val transcription: String = "",
    @SerializedName("specialty")     val specialty: String = "",
    @SerializedName("diagnosis")     val diagnosis: String = "",
    @SerializedName("keywords")      val keywords: String = ""
)

@Composable
fun HomeScreen() {

    val auth = FirebaseAuth.getInstance()
    val db = FirebaseFirestore.getInstance()
    val uid = auth.currentUser?.uid ?: return
    val gson = remember { Gson() }

    var fullName by remember { mutableStateOf("") }
    var transcriptions by remember { mutableStateOf<List<TranscriptionData>>(emptyList()) }
    var thisMonthCount by remember { mutableIntStateOf(0) }
    var weeklyData by remember { mutableStateOf<List<Pair<String, Int>>>(emptyList()) }

    // get current user's info and load any current transcriptions in database
    LaunchedEffect(uid) {
        db.collection("users").document(uid).get()
            .addOnSuccessListener { doc ->
                fullName = doc.getString("FirstnameLastname") ?: "Doctor"
            }
        // get all transcriptions for current user
        db.collection("users").document(uid).collection("transcriptions")
            .get()
            .addOnSuccessListener { snap ->
                val parsed = snap.documents.mapNotNull { doc ->
                    val raw = doc.getString("data") ?: return@mapNotNull null
                    runCatching { gson.fromJson(raw, TranscriptionData::class.java) }.getOrNull()
                }

                val dateFmt = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
                val sorted = parsed.sortedByDescending {
                    runCatching { dateFmt.parse(it.date)?.time ?: 0L }.getOrElse { 0L }
                }

                transcriptions = sorted

                val currentMonth = SimpleDateFormat("yyyy-MM", Locale.getDefault()).format(Date())
                thisMonthCount = sorted.count { it.date.startsWith(currentMonth) }

                val dayFmt = SimpleDateFormat("EEE", Locale.getDefault())
                weeklyData = (6 downTo 0).map { i ->
                    val day = Calendar.getInstance().apply { add(Calendar.DAY_OF_YEAR, -i) }
                    val label = if (i == 0) "Today" else dayFmt.format(day.time)
                    val dayStr = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(day.time)
                    val count = sorted.count { it.date == dayStr }
                    label to count
                }
            }
    }
    // end of get current user's info and load any current transcriptions in database
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 20.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Text(
                text = "Welcome back, $fullName",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "Here's your activity overview.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        item {
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Column(modifier = Modifier.padding(20.dp)) {
                    Text(
                        text = "This Month",
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = "$thisMonthCount",
                        fontSize = 48.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Text(
                        text = "transcription${if (thisMonthCount != 1) "s" else ""} submitted",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
                    )
                }
            }
        }

        if (weeklyData.isNotEmpty()) {
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Text(
                            text = "Last 7 Days",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(Modifier.height(16.dp))
                        WeeklyBarChart(data = weeklyData)
                    }
                }
            }
        }

        item {
            Text(
                text = "Recent Transcriptions",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
        }

        if (transcriptions.isEmpty()) {
            item {
                Text(
                    text = "No transcriptions yet.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            items(transcriptions.take(5)) { t ->
                RecentTranscriptionCard(t)
            }
        }
        item { Spacer(Modifier.height(24.dp)) }

    }
}

// defineitly not copied from github
@Composable
fun WeeklyBarChart(data: List<Pair<String, Int>>) {
    val maxCount = data.maxOfOrNull { it.second }?.coerceAtLeast(1) ?: 1
    val barColor = MaterialTheme.colorScheme.primary
    val dimColor = MaterialTheme.colorScheme.surfaceVariant

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(120.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Bottom
    ) {
        data.forEach { (label, count) ->
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Bottom,
                modifier = Modifier.weight(1f)
            ) {
                if (count > 0) {
                    Text(text = "$count", fontSize = 10.sp)
                }
                Spacer(Modifier.height(2.dp))
                Box(
                    modifier = Modifier
                        .fillMaxWidth(0.6f)
                        .height(((count.toFloat() / maxCount) * 80).dp.coerceAtLeast(4.dp))
                        .clip(RoundedCornerShape(topStart = 4.dp, topEnd = 4.dp))
                        .background(if (count > 0) barColor else dimColor)
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    text = label,
                    fontSize = 9.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1
                )
            }
        }
    }
}

// copied and pasted from history bc im lazy
@Composable
fun RecentTranscriptionCard(t: TranscriptionData) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        )
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = t.title.ifBlank { "Untitled" },
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.weight(1f)
                )
                Text(
                    text = t.date,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            if (t.specialty.isNotBlank()) {
                Spacer(Modifier.height(4.dp))
                Text(
                    text = t.specialty,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
            if (t.preview.isNotBlank()) {
                Spacer(Modifier.height(4.dp))
                Text(
                    text = t.preview,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}