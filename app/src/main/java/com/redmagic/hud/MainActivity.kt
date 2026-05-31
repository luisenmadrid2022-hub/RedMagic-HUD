package com.redmagic.hud

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.redmagic.hud.service.PerformanceService
import com.redmagic.hud.shizuku.ShizukuManager
import com.redmagic.hud.ui.screens.MainScreen

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        startService(Intent(this, PerformanceService::class.java))

        setContent {
            var shizukuReady by remember { mutableStateOf(false) }

            LaunchedEffect(Unit) {
                shizukuReady = ShizukuManager.isReady()
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
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
    }
}
