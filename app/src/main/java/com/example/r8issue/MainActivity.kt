package com.example.r8issue

import android.app.Activity
import android.os.Bundle
import com.twilio.auth.TwilioAuth

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        TwilioAuth.getInstance(this)
    }
}