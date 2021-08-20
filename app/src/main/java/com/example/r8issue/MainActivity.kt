package com.example.r8issue

import android.app.Activity
import android.os.Bundle
import com.twilio.auth.TwilioAuth
import java.util.*

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val authy = TwilioAuth.getInstance(this)
        val request = authy.getRequest(UUID.randomUUID().toString())
        authy.approveRequest(request)
    }
}
