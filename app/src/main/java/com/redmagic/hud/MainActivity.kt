package com.redmagic.hud

import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.os.Bundle
import android.os.IBinder
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.redmagic.hud.service.PerformanceService
import com.redmagic.hud.shizuku.ShizukuManager
import com.redmagic.hud.ui.screens.MainScreen
import com.redmagic.hud.ui.theme.JarvisColors

class MainActivity : ComponentActivity() {

    private var service: PerformanceService? = null
    private var bound = false

    private val connection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, binder: IBinder?) {
            bound = true
        }

        override fun onServiceDisconnected(name: ComponentName?) {
            bound = false
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        startService(Intent(this, PerformanceService::class.java))
        bindService(Intent(this, PerformanceService::class.java), connection, Context.BIND_AUTO_CREATE)

        setContent {
            var shizukuReady by remember { mutableStateOf(false) }

            LaunchedEffect(Unit) {
                shizukuReady = ShizukuManager.isReady()
                if (shizukuReady) {
                    service?.setVisible(true)
                }
            }

            androidx.compose.foundation.layout.Box(
                modifier = Modifier.fillMaxSize()
            ) {
                MainScreen(
                    onExecuteCommand = { command ->
                        if (ShizukuManager.isReady()) {
                            try {
                                val result = ShizukuManager.execute(command)
                                if (result.isNotBlank()) {
                                    Toast.makeText(this@MainActivity, result.take(100), Toast.LENGTH_SHORT).show()
                                } else {
                                    Toast.makeText(this@MainActivity, "Comando ejecutado", Toast.LENGTH_SHORT).show()
                                }
                            } catch (e: Exception) {
                                Toast.makeText(this@MainActivity, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            Toast.makeText(this@MainActivity, "Shizuku no disponible", Toast.LENGTH_SHORT).show()
                        }
                    }
                )

                if (!shizukuReady) {
                    // Shizuku not ready indicator
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        service?.setVisible(true)
    }

    override fun onPause() {
        super.onPause()
        service?.setVisible(false)
    }

    override fun onDestroy() {
        if (bound) {
            unbindService(connection)
            bound = false
        }
        super.onDestroy()
    }
}
