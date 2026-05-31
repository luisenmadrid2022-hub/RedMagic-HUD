package com.redmagic.hud.shizuku

object ShizukuManager {

    fun isReady(): Boolean {
        return false
    }

    fun execute(command: String): String {
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
}
