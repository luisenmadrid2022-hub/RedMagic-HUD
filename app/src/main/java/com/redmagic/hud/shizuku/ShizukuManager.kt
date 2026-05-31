package com.redmagic.hud.shizuku

import android.os.RemoteException
import rikka.shizuku.Shizuku

object ShizukuManager {

    fun isReady(): Boolean {
        return try {
            Shizuku.pingBinder() && Shizuku.getVersion() > 0
        } catch (_: Exception) {
            false
        }
    }

    fun execute(command: String): String {
        val output = StringBuilder()
        try {
            val process = Shizuku.newProcess(arrayOf("sh", "-c", command), null)
            process.inputStream.bufferedReader().use { reader ->
                var line: String?
                while (reader.readLine().also { line = it } != null) {
                    if (output.isNotEmpty()) output.append("\n")
                    output.append(line)
                }
            }
            process.waitFor()
        } catch (e: RemoteException) {
            throw RuntimeException("Shizuku execution failed", e)
        }
        return output.toString().trim()
    }
}
