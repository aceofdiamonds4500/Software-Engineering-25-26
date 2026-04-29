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

// Logo-matched palette
private val Teal       = Color(0xFF4DB899)
private val TealDark   = Color(0xFF3A9E82)
private val TealLight  = Color(0xFF7DD4B8)
private val Charcoal   = Color(0xFF1E1E1E)
private val Surface    = Color(0xFF2A2A2A)
private val SurfaceVar = Color(0xFF333333)
private val OnDark     = Color(0xFFF0F0F0)
private val OnTeal     = Color(0xFF0F0F0F)

// Light theme: teal accents on light background
private val LightBg    = Color(0xFFF2F5F4)
private val LightSurf  = Color(0xFFFFFFFF)
private val LightText  = Color(0xFF1A1A1A)

private val LightColorScheme = lightColorScheme(
    primary            = Teal,
    onPrimary          = OnTeal,
    primaryContainer   = TealLight,
    onPrimaryContainer = OnTeal,
    background         = LightBg,
    onBackground       = LightText,
    surface            = LightSurf,
    onSurface          = LightText,
    surfaceVariant     = Color(0xFFE0EFEA),
    onSurfaceVariant   = LightText,
    secondary          = TealDark,
    onSecondary        = OnDark,
    error              = Color(0xFFB00020),
    onError            = Color.White
)

private val DarkColorScheme = darkColorScheme(
    primary            = Teal,
    onPrimary          = OnTeal,
    primaryContainer   = TealDark,
    onPrimaryContainer = OnDark,
    background         = Charcoal,
    onBackground       = OnDark,
    surface            = Surface,
    onSurface          = OnDark,
    surfaceVariant     = SurfaceVar,
    onSurfaceVariant   = OnDark,
    secondary          = TealDark,
    onSecondary        = OnDark,
    error              = Color(0xFFCF6679),
    onError            = Color.Black
)

private fun bump(style: TextStyle, deltaSp: Float): TextStyle {
    val size: TextUnit = style.fontSize
    return if (size == TextUnit.Unspecified) style else style.copy(fontSize = (size.value + deltaSp).sp)
}

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    enlargeText: Boolean = false,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    val base = Typography
    val scaled = if (enlargeText) {
        val delta = 4f
        base.copy(
            displayLarge  = bump(base.displayLarge, delta),
            displayMedium = bump(base.displayMedium, delta),
            displaySmall  = bump(base.displaySmall, delta),
            headlineLarge  = bump(base.headlineLarge, delta),
            headlineMedium = bump(base.headlineMedium, delta),
            headlineSmall  = bump(base.headlineSmall, delta),
            titleLarge  = bump(base.titleLarge, delta),
            titleMedium = bump(base.titleMedium, delta),
            titleSmall  = bump(base.titleSmall, delta),
            bodyLarge   = bump(base.bodyLarge, delta),
            bodyMedium  = bump(base.bodyMedium, delta),
            bodySmall   = bump(base.bodySmall, delta),
            labelLarge  = bump(base.labelLarge, delta),
            labelMedium = bump(base.labelMedium, delta),
            labelSmall  = bump(base.labelSmall, delta),
        )
    } else base

    MaterialTheme(
        colorScheme = colorScheme,
        typography = scaled,
        content = content
    )
}