package com.redmagic.hud.data

import com.redmagic.hud.shizuku.ShizukuCommands
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class PerformanceRepository {

    private var cache: PerformanceData? = null
    private var lastFetchMs: Long = 0
    private val cacheDurationMs = 1500L

    suspend fun getData(): PerformanceData = withContext(Dispatchers.IO) {
        val now = System.currentTimeMillis()
        if (cache != null && (now - lastFetchMs) < cacheDurationMs) {
            return@withContext cache!!
        }

        val data = fetchFresh()
        cache = data
        lastFetchMs = now
        data
    }

    private suspend fun fetchFresh(): PerformanceData {
        val commands = ShizukuCommands()

        val cpuUsage = try { commands.getCpuUsage() } catch (_: Exception) { 0f }
        val cpuTemp = try { commands.getCpuTemp() } catch (_: Exception) { 0f }
        val ramTotalKb = try { commands.getRamTotal() } catch (_: Exception) { 0L }
        val ramAvailKb = try { commands.getRamAvailable() } catch (_: Exception) { 0L }
        val batteryRaw = try { commands.getBattery() } catch (_: Exception) { "" }
        val refresh = try { commands.getRefreshRate() } catch (_: Exception) { 60 }
        val uptimeSecs = try { commands.getUptime() } catch (_: Exception) { 0f }

        val ramUsedKb = if (ramTotalKb > 0 && ramAvailKb > 0) ramTotalKb - ramAvailKb else 0L

        val batteryParts = batteryRaw.split(" ").filter { it.isNotBlank() }
        val batteryLevel = batteryParts.getOrNull(0)?.toIntOrNull() ?: 0
        val batteryTemp = (batteryParts.getOrNull(1)?.toFloatOrNull() ?: 0f) / 10f
        val isCharging = batteryParts.getOrNull(2) == "true" || batteryParts.getOrNull(3) == "true"

        return PerformanceData(
            cpuUsage = cpuUsage,
            cpuTemp = cpuTemp,
            ramUsedMb = ramUsedKb / 1024,
            ramTotalMb = ramTotalKb / 1024,
            batteryLevel = batteryLevel,
            batteryTemp = batteryTemp,
            uptimeHours = uptimeSecs / 3600f,
            refreshRate = refresh,
            isCharging = isCharging
        )
    }
}
