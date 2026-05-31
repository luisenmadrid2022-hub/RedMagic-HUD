package com.redmagic.hud.shizuku

object ShizukuManager {

    fun isReady(): Boolean {
        return try {
            rikka.shizuku.Shizuku.pingBinder() && rikka.shizuku.Shizuku.getVersion() > 0
        } catch (_: Exception) {
            false
        }
    }

    fun executeShizukuCommand(command: String): String {
        // Shizuku 13.1.5 does not expose public newProcess
        // Fall back to normal shell for now
        return executeNormal(command)
    }

    private fun executeNormal(command: String): String {
        val output = StringBuilder()
        try {
            val process = Runtime.getRuntime().exec(arrayOf("sh", "-c", command))
            process.inputStream.bufferedReader().use { reader ->
                var line: String?
                while (reader.readLine().also { line = it } != null) {
                    if (output.isNotEmpty()) output.append("\n")
                    output.append(line)
                }
            }
            process.waitFor()
        } catch (e: Exception) {
            throw RuntimeException("Command execution failed", e)
        }
        return output.toString().trim()
    }

    fun execute(command: String): String {
        return executeNormal(command)
    }
}
