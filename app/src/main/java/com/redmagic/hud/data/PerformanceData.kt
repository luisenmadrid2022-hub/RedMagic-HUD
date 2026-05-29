package com.redmagic.hud.data

data class PerformanceData(
    val cpuUsage: Float = 0f,
    val cpuTemp: Float = 0f,
    val ramUsedMb: Long = 0,
    val ramTotalMb: Long = 0,
    val batteryLevel: Int = 0,
    val batteryTemp: Float = 0f,
    val uptimeHours: Float = 0f,
    val refreshRate: Int = 60,
    val isCharging: Boolean = false
) {
    val ramPercent: Float
        get() = if (ramTotalMb > 0) (ramUsedMb.toFloat() / ramTotalMb) * 100f else 0f

    val cpuPercentFormatted: String
        get() = "%.0f".format(cpuUsage)

    val cpuTempFormatted: String
        get() = "%.1f°C".format(cpuTemp)

    val ramFormatted: String
        get() = "${ramUsedMb / 1024}/${ramTotalMb / 1024} GB"

    val batteryFormatted: String
        get() = "$batteryLevel%"

    val uptimeFormatted: String
        get() = "%.1fh".format(uptimeHours)
}
