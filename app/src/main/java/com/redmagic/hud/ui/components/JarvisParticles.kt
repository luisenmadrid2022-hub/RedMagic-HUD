package com.redmagic.hud.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import com.redmagic.hud.ui.theme.JarvisColors
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random

data class Particle(
    var angle: Float,
    var radius: Float,
    var speed: Float,
    var size: Float,
    var alpha: Float,
    var phase: Float
)

@Composable
fun JarvisParticles(modifier: Modifier = Modifier) {
    val particles = remember {
        List(40) {
            Particle(
                angle = Random.nextFloat() * 360f,
                radius = Random.nextFloat() * 180f + 20f,
                speed = Random.nextFloat() * 0.3f + 0.1f,
                size = Random.nextFloat() * 3f + 1.5f,
                alpha = Random.nextFloat() * 0.6f + 0.2f,
                phase = Random.nextFloat() * 360f
            )
        }
    }

    val infiniteTransition = rememberInfiniteTransition(label = "particles")
    val globalPhase by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(12000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "globalPhase"
    )

    Canvas(modifier = modifier) {
        val center = Offset(size.width / 2, size.height / 2)

        drawRings(center, size.minDimension)

        particles.forEachIndexed { i, p ->
            val radians = Math.toRadians((p.angle + globalPhase * p.speed).toDouble())
            val x = center.x + p.radius * cos(radians).toFloat()
            val y = center.y + p.radius * sin(radians).toFloat()
            val pos = Offset(x, y)

            val glowAlpha = p.alpha * (0.7f + 0.3f * sin(Math.toRadians((globalPhase + p.phase * 60f)).toFloat()))

            // Node glow
            drawCircle(
                color = JarvisColors.Gold.copy(alpha = glowAlpha * 0.3f),
                radius = p.size * 4f,
                center = pos
            )
            // Node body
            drawCircle(
                color = JarvisColors.Gold.copy(alpha = glowAlpha),
                radius = p.size,
                center = pos
            )
            // Node core
            drawCircle(
                color = JarvisColors.Amber.copy(alpha = glowAlpha * 0.8f),
                radius = p.size * 0.4f,
                center = pos
            )

            // Connections to nearby particles
            for (j in i + 1 until particles.size) {
                val p2 = particles[j]
                val rad2 = Math.toRadians((p2.angle + globalPhase * p2.speed).toDouble())
                val x2 = center.x + p2.radius * cos(rad2).toFloat()
                val y2 = center.y + p2.radius * sin(rad2).toFloat()
                val pos2 = Offset(x2, y2)
                val dist = (pos - pos2).getDistance()

                if (dist < 120f) {
                    val connAlpha = (1f - dist / 120f) * 0.25f
                    drawLine(
                        color = JarvisColors.Cyan.copy(alpha = connAlpha),
                        start = pos,
                        end = pos2,
                        strokeWidth = 0.8f
                    )
                }
            }
        }
    }
}

private fun DrawScope.drawRings(center: Offset, maxDim: Float) {
    val ringRadii = listOf(60f, 120f, 180f)
    ringRadii.forEach { radius ->
        if (radius * 2 < maxDim) {
            drawCircle(
                color = JarvisColors.Border.copy(alpha = 0.15f),
                radius = radius,
                center = center,
                style = Stroke(width = 1f)
            )
        }
    }
}
