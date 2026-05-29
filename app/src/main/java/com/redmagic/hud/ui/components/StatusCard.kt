package com.redmagic.hud.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.redmagic.hud.ui.theme.JarvisColors

@Composable
fun StatusCard(
    title: String,
    value: String,
    progress: Float,
    modifier: Modifier = Modifier,
    unit: String = ""
) {
    val infiniteTransition = rememberInfiniteTransition(label = "borderGlow")
    val borderAlpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 0.8f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "borderAlpha"
    )

    val progressColor = when {
        progress < 0.5f -> JarvisColors.Green
        progress < 0.8f -> JarvisColors.Gold
        else -> JarvisColors.Red
    }

    val animatedProgress by animateFloatAsState(
        targetValue = progress.coerceIn(0f, 1f),
        animationSpec = tween(600),
        label = "progress"
    )

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(12.dp))
            .background(JarvisColors.SurfaceCard.copy(alpha = 0.9f))
            .border(
                width = 1.dp,
                color = JarvisColors.Gold.copy(alpha = borderAlpha),
                shape = RoundedCornerShape(12.dp)
            )
            .padding(12.dp)
    ) {
        Column {
            Text(
                text = title,
                color = JarvisColors.TextSecondary,
                fontSize = 11.sp,
                fontWeight = FontWeight.Light
            )
            Spacer(Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.Bottom) {
                Text(
                    text = value,
                    color = JarvisColors.TextPrimary,
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Bold
                )
                if (unit.isNotBlank()) {
                    Spacer(Modifier.width(4.dp))
                    Text(
                        text = unit,
                        color = JarvisColors.TextSecondary,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Light
                    )
                }
            }
            Spacer(Modifier.height(8.dp))
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(4.dp)
                    .clip(RoundedCornerShape(2.dp))
                    .background(JarvisColors.Border)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(animatedProgress)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(2.dp))
                        .background(progressColor)
                )
            }
        }
    }
}
