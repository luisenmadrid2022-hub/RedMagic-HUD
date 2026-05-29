package com.redmagic.hud
import android.os.Bundle
import android.webkit.WebView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.allowFileAccess = true
        webView.loadUrl("file:///android_asset/index.html")
        setContentView(webView)
    }
}
