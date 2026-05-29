package com.redmagic.hud.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.redmagic.hud.ui.theme.JarvisColors

data class QuickAction(
    val id: String,
    val label: String,
    val command: String
)

@Composable
fun QuickActionsPanel(
    actions: List<QuickAction>,
    onExecute: (QuickAction) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        Text(
            text = "ACCIONES RAPIDAS",
            color = JarvisColors.TextDim,
            fontSize = 10.sp,
            letterSpacing = 2.sp,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(actions.size) { index ->
                val action = actions[index]
                ActionButton(action = action, onClick = { onExecute(action) })
            }
        }
    }
}

@Composable
private fun ActionButton(
    action: QuickAction,
    onClick: () -> Unit
) {
    var pressed by remember { mutableStateOf(false) }

    val bgColor by animateColorAsState(
        targetValue = if (pressed) JarvisColors.Gold.copy(alpha = 0.2f) else JarvisColors.SurfaceCard,
        animationSpec = tween(200),
        label = "buttonBg"
    )

    Box(
        modifier = Modifier
            .aspectRatio(1.2f)
            .clip(RoundedCornerShape(8.dp))
            .background(bgColor)
            .border(
                width = 1.dp,
                color = JarvisColors.Border,
                shape = RoundedCornerShape(8.dp)
            )
            .clickable(
                onClick = {
                    pressed = true
                    onClick()
                }
            ),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = action.label,
            color = JarvisColors.TextPrimary,
            fontSize = 11.sp,
            fontWeight = FontWeight.Medium,
            textAlign = TextAlign.Center
        )
    }

    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(200)
        pressed = false
    }
}
