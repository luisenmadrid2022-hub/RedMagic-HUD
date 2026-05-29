package com.redmagic.hud.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.redmagic.hud.data.PerformanceData
import com.redmagic.hud.data.PerformanceRepository
import kotlinx.coroutines.*

class PerformanceService : Service() {

    companion object {
        const val CHANNEL_ID = "redmagic_hud_monitor"
        const val NOTIFICATION_ID = 1001

        var latestData: PerformanceData? = null
            private set
    }

    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    private val repository = PerformanceRepository()
    private var isActive = false
    private var intervalMs = 2000L

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, buildNotification(PerformanceData()))
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        isActive = true
        scope.launch { pollingLoop() }
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        isActive = false
        scope.cancel()
        super.onDestroy()
    }

    fun setVisible(visible: Boolean) {
        intervalMs = if (visible) 2000L else 5000L
    }

    private suspend fun pollingLoop() {
        while (isActive) {
            try {
                val data = repository.getData()
                latestData = data
                updateNotification(data)
            } catch (_: Exception) { }
            delay(intervalMs)
        }
    }

    private fun updateNotification(data: PerformanceData) {
        val notificationManager = getSystemService(NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(NOTIFICATION_ID, buildNotification(data))
    }

    private fun buildNotification(data: PerformanceData): Notification {
        val content = "CPU: ${data.cpuPercentFormatted}% | RAM: ${data.ramFormatted} | Bat: ${data.batteryFormatted}"
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("RedMagic HUD")
            .setContentText(content)
            .setSmallIcon(android.R.drawable.ic_menu_info_details)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "RedMagic HUD Monitor",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Monitoreo de rendimiento del sistema"
                setShowBadge(false)
            }
            val manager = getSystemService(NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(channel)
        }
    }
}
