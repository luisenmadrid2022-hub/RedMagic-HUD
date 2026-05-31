package com.redmagic.hud.service

import android.app.Service
import android.content.Intent
import android.os.IBinder
import com.redmagic.hud.data.PerformanceData
import com.redmagic.hud.data.PerformanceRepository
import kotlinx.coroutines.*

class PerformanceService : Service() {

    companion object {
        var latestData: PerformanceData? = null
            private set
    }

    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    private val repository = PerformanceRepository()
    private var isActive = false

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

    private suspend fun pollingLoop() {
        while (isActive) {
            try {
                val data = repository.getData()
                latestData = data
            } catch (_: Exception) { }
            delay(2000)
        }
    }
}
