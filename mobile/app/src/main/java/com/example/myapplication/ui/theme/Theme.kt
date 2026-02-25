package com.example.myapplication.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Your CURRENT light theme look (so it stays the same)
private val LightBg = Color(220, 224, 228)          // AppBackground
private val LightDrawer = Color(210, 232, 247)      // Drawer sheet
private val LightTopBar = Color(123, 170, 224)      // TopAppBar
private val LightText = Color(30, 30, 30)

// Your DARK MODE palette
private val DarkNavy = Color(0xFF1B3C53)
private val DarkNavy2 = Color(0xFF234C6A)
private val DarkBlueGray = Color(0xFF456882)
private val WarmBeige = Color(0xFFD2C1B6)

private val LightColorScheme = lightColorScheme(
    primary = LightTopBar,
    onPrimary = LightText,

    background = LightBg,
    onBackground = LightText,

    surface = Color.White,
    onSurface = LightText,

    secondary = LightDrawer,
    onSecondary = LightText
)

private val DarkColorScheme = darkColorScheme(
    primary = DarkNavy2,
    onPrimary = WarmBeige,

    background = DarkNavy,
    onBackground = WarmBeige,

    surface = DarkBlueGray,
    onSurface = WarmBeige,

    secondary = DarkNavy2,
    onSecondary = WarmBeige
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false, // keep false so your palette isn't overridden
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
