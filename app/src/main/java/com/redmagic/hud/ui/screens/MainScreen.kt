package com.redmagic.hud.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.redmagic.hud.data.PerformanceData
import com.redmagic.hud.service.PerformanceService
import com.redmagic.hud.ui.components.*
import com.redmagic.hud.ui.theme.JarvisColors
import kotlinx.coroutines.delay

@Composable
fun MainScreen(
    onExecuteCommand: (String) -> Unit
) {
    var data by remember { mutableStateOf(PerformanceData()) }

    LaunchedEffect(Unit) {
        while (true) {
            val latest = PerformanceService.latestData
            if (latest != null) data = latest
            delay(1500)
        }
    }

    val quickActions = listOf(
        QuickAction("game", "Game Mode", "cmd thermalservice override-status 0 && settings put system user_refresh_rate 120"),
        QuickAction("eco", "Eco Mode", "cmd thermalservice override-status 1 && settings put system user_refresh_rate 90"),
        QuickAction("tune", "Ultimate", "settings put system user_refresh_rate 120 && settings put global animator_duration_scale 0.5"),
        QuickAction("thermal_on", "Thermal ON", "cmd thermalservice override-status 1"),
        QuickAction("thermal_off", "Thermal OFF", "cmd thermalservice override-status 0"),
        QuickAction("clean", "Clean RAM", "am broadcast -a android.intent.action.CLOSE_SYSTEM_DIALOGS")
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(JarvisColors.Background)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp)
        ) {
            // Header
            Text(
                text = "REDMAGIC HUD",
                color = JarvisColors.Gold,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 3.sp
            )
            Text(
                text = "System Performance Monitor",
                color = JarvisColors.TextDim,
                fontSize = 10.sp,
                letterSpacing = 2.sp
            )

            Spacer(Modifier.height(16.dp))

            // Particle canvas
            JarvisParticles(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
            )

            Spacer(Modifier.height(16.dp))

            // CPU + Temp row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                StatusCard(
                    title = "CPU USAGE",
                    value = data.cpuPercentFormatted,
                    progress = data.cpuUsage / 100f,
                    unit = "%",
                    modifier = Modifier.weight(1f)
                )
                StatusCard(
                    title = "CPU TEMP",
                    value = data.cpuTempFormatted,
                    progress = data.cpuTemp / 80f,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(Modifier.height(12.dp))

            // RAM + Battery row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                StatusCard(
                    title = "RAM",
                    value = data.ramFormatted,
                    progress = data.ramPercent / 100f,
                    modifier = Modifier.weight(1f)
                )
                StatusCard(
                    title = "BATTERY",
                    value = data.batteryFormatted,
                    progress = data.batteryLevel / 100f,
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(Modifier.height(12.dp))

            // Uptime
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                StatusCard(
                    title = "UPTIME",
                    value = data.uptimeFormatted,
                    progress = data.uptimeHours / 24f,
                    modifier = Modifier.weight(1f)
                )
                StatusCard(
                    title = "REFRESH",
                    value = "${data.refreshRate}",
                    progress = data.refreshRate / 120f,
                    unit = "Hz",
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(Modifier.height(24.dp))

            // Circular gauge
            CircularGauge(
                value = data.cpuUsage,
                maxValue = 100f,
                label = "CPU %",
                modifier = Modifier
                    .align(Alignment.CenterHorizontally)
                    .size(180.dp)
            )

            Spacer(Modifier.height(24.dp))

            // Quick actions
            QuickActionsPanel(
                actions = quickActions,
                onExecute = { action -> onExecuteCommand(action.command) }
            )

            Spacer(Modifier.height(32.dp))
        }
    }
}
