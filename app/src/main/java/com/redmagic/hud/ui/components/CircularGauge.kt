package com.redmagic.hud.ui.components

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.redmagic.hud.ui.theme.JarvisColors
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun CircularGauge(
    value: Float,
    maxValue: Float,
    label: String,
    modifier: Modifier = Modifier,
    valueColor: Color = JarvisColors.Gold
) {
    val fraction = (value / maxValue).coerceIn(0f, 1f)
    val animatedFraction by animateFloatAsState(
        targetValue = fraction,
        animationSpec = tween(1000),
        label = "gauge"
    )

    val arcColor = when {
        animatedFraction < 0.5f -> JarvisColors.Green
        animatedFraction < 0.8f -> JarvisColors.Gold
        else -> JarvisColors.Red
    }

    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val strokeWidth = size.minDimension * 0.08f
            val radius = (size.minDimension - strokeWidth) / 2
            val topLeft = Offset(
                (size.width - radius * 2) / 2,
                (size.height - radius * 2) / 2
            )
            val arcSize = Size(radius * 2, radius * 2)

            // Background arc (270 deg)
            drawArc(
                color = JarvisColors.Border,
                startAngle = 135f,
                sweepAngle = 270f,
                useCenter = false,
                topLeft = topLeft,
                size = arcSize,
                style = Stroke(width = strokeWidth, cap = StrokeCap.Round)
            )

            // Foreground arc
            drawArc(
                color = arcColor,
                startAngle = 135f,
                sweepAngle = 270f * animatedFraction,
                useCenter = false,
                topLeft = topLeft,
                size = arcSize,
                style = Stroke(width = strokeWidth, cap = StrokeCap.Round)
            )

            // Tick marks every 30 degrees
            for (deg in 0..270 step 30) {
                val angle = Math.toRadians((135 + deg).toDouble())
                val innerR = radius * 0.85f
                val outerR = radius * 0.93f
                val isMajor = deg % 90 == 0
                val tickR1 = if (isMajor) innerR else radius * 0.88f
                val tickR2 = if (isMajor) radius * 0.95f else outerR

                val cx = size.width / 2
                val cy = size.height / 2

                val x1 = cx + tickR1 * cos(angle).toFloat()
                val y1 = cy + tickR1 * sin(angle).toFloat()
                val x2 = cx + tickR2 * cos(angle).toFloat()
                val y2 = cy + tickR2 * sin(angle).toFloat()

                drawLine(
                    color = JarvisColors.TextDim,
                    start = Offset(x1, y1),
                    end = Offset(x2, y2),
                    strokeWidth = if (isMajor) 2f else 1f
                )
            }
        }

        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = "%.0f".format(value),
                color = valueColor,
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = label,
                color = JarvisColors.TextSecondary,
                fontSize = 11.sp,
                fontWeight = FontWeight.Light
            )
        }
    }
}
