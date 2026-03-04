package com.example.myapplication.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.sp

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

private fun bump(style: TextStyle, deltaSp: Float): TextStyle {
    val size: TextUnit = style.fontSize
    // Some styles can be Unspecified; only bump real sizes.
    return if (size == TextUnit.Unspecified) style else style.copy(fontSize = (size.value + deltaSp).sp)
}

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    enlargeText: Boolean = false,
    dynamicColor: Boolean = false, // keep false so your palette isn't overridden
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    val base = Typography
    val scaled = if (enlargeText) {
        val delta = 4f
        base.copy(
            displayLarge = bump(base.displayLarge, delta),
            displayMedium = bump(base.displayMedium, delta),
            displaySmall = bump(base.displaySmall, delta),

            headlineLarge = bump(base.headlineLarge, delta),
            headlineMedium = bump(base.headlineMedium, delta),
            headlineSmall = bump(base.headlineSmall, delta),

            titleLarge = bump(base.titleLarge, delta),
            titleMedium = bump(base.titleMedium, delta),
            titleSmall = bump(base.titleSmall, delta),

            bodyLarge = bump(base.bodyLarge, delta),
            bodyMedium = bump(base.bodyMedium, delta),
            bodySmall = bump(base.bodySmall, delta),

            labelLarge = bump(base.labelLarge, delta),
            labelMedium = bump(base.labelMedium, delta),
            labelSmall = bump(base.labelSmall, delta),
        )
    } else {
        base
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = scaled,
        content = content
    )
}