plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.redmagic.hud"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.redmagic.hud"
        minSdk = 21
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }
    buildTypes { release { isMinifyEnabled = false } }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
}
dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.12.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("rikka.shizuku:api:13.1.5")
    implementation("rikka.shizuku:provider:13.1.5")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}
