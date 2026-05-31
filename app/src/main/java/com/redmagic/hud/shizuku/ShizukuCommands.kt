package com.redmagic.hud.shizuku

typealias ShizukuExecutor = (String) -> String

class ShizukuCommands {

    private val sh: ShizukuExecutor = { cmd -> ShizukuManager.execute(cmd) }

    fun getCpuUsage(): Float {
        val out = sh("top -bn1 -d 0.1 | grep \"CPU:\" | awk '{print 100 - $8}'")
        return out.lines().firstOrNull { it.isNotBlank() }?.toFloatOrNull() ?: 0f
    }

    fun getCpuTemp(): Float {
        val out = sh("cat /sys/class/thermal/thermal_zone*/temp | head -1")
        return (out.lines().firstOrNull { it.isNotBlank() }?.toFloatOrNull() ?: 0f) / 1000f
    }

    fun getRamTotal(): Long {
        val out = sh("grep MemTotal /proc/meminfo | awk '{print $2}'")
        return out.lines().firstOrNull { it.isNotBlank() }?.toLongOrNull() ?: 0L
    }

    fun getRamAvailable(): Long {
        val out = sh("grep MemAvailable /proc/meminfo | awk '{print $2}'")
        return out.lines().firstOrNull { it.isNotBlank() }?.toLongOrNull() ?: 0L
    }

    fun getBattery(): String {
        val out = sh("dumpsys battery | grep -E \"level|temperature|AC powered|USB powered\" | awk '{print $2}' | tr '\\n' ' '")
        return out
    }

    fun getRefreshRate(): Int {
        val out = sh("settings get system user_refresh_rate")
        return out.lines().firstOrNull { it.isNotBlank() }?.toIntOrNull() ?: 60
    }

    fun getUptime(): Float {
        val out = sh("cat /proc/uptime | awk '{print $1}'")
        return out.lines().firstOrNull { it.isNotBlank() }?.toFloatOrNull() ?: 0f
    }

    fun executeCommand(command: String): String {
        return sh(command)
    }
}
