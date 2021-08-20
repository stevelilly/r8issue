This repository is to demonstrate an unexpected behaviour with package obfuscation we have seen in R8 since the introduction of flattened packages.

This example is a little contrived, but it's the first example from our actual app build I've been able to consistently reproduce in an sandbox project.
The `libs/com.twilio-authenticator-1.2.9.jar` file is the raw `classes.jar` file found inside [https://repo1.maven.org/maven2/com/twilio/authenticator/1.2.9/authenticator-1.2.9.aar].
As such it includes no consumer `proguard.txt` from the AAR file.

# Reproduction

Set the classpath to local build of R8 in `./build.gradle`

Building with R8 from commit `b87d2df7cff717e4b828c24ac19847413677f58b`:
(or with 3.0.64 from AGP 7.0.1)

```
$ ./gradlew app:assembleRelease
$ grep "^com.twilio.auth.external" app/build/outputs/mapping/release/mapping.txt
com.twilio.auth.external.ApprovalRequest -> b.a:
com.twilio.auth.external.ApprovalRequestLogo -> b.b:
com.twilio.auth.external.ApprovalRequestStatus -> b.c:
com.twilio.auth.external.ApprovalRequests -> b.d:
com.twilio.auth.external.TOTPCallback -> b.e:
com.twilio.auth.external.TimeInterval -> b.f:
com.twilio.auth.external.TimeInterval$1 -> b.f$a:
com.twilio.auth.external.TimeInterval$Builder -> b.f$b:
```

Classes are repackaged as expected.

Now doing the same thing with the next R8 commit `f53c90005e6f7201162f8e2b4eb4c94a79626f51`:
(or the latest at time of writing, `685a8c81f`)

```
$ ./gradlew app:assembleRelease
$ grep "^com.twilio.auth.external" app/build/outputs/mapping/release/mapping.txt
com.twilio.auth.external.ApprovalRequest -> com.twilio.auth.external.a:
com.twilio.auth.external.ApprovalRequestLogo -> com.twilio.auth.external.b:
com.twilio.auth.external.ApprovalRequestStatus -> com.twilio.auth.external.c:
com.twilio.auth.external.ApprovalRequests -> com.twilio.auth.external.d:
com.twilio.auth.external.TOTPCallback -> com.twilio.auth.external.e:
com.twilio.auth.external.TimeInterval -> com.twilio.auth.external.f:
com.twilio.auth.external.TimeInterval$1 -> com.twilio.auth.external.f$a:
com.twilio.auth.external.TimeInterval$Builder -> com.twilio.auth.external.f$b:
```

Now after removing following line in `proguard-rules.pro`:

```
-keep,allowobfuscation class com.twilio.auth.external.** { *; }
```

And checking again:

```
$ ./gradlew app:assembleRelease
$ grep "^com.twilio.auth.external" app/build/outputs/mapping/release/mapping.txt
com.twilio.auth.external.ApprovalRequest -> b.a:
```

Expected behaviour: -keep,allowobfuscation should allow both the class and package name to be changed within `com.twilio.auth.external.**`
Actual behaviour: classes inside `com.twilio.auth.external` are renamed, yet the package name is kept
