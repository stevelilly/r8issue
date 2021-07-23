
This repository is to demonstrate an unexpected behaviour with package obfuscation we have seen in R8 since the introduction of flattened packages.
While we note that some similar looking bugs have been fixed, this example is apparently still occurring as of R8 3.0.62 that ships with Android Gradle Plugin 7.0.0-rc01

This example is a little contrived, but it's the first example from our actual app build I've been able to consistently reproduce in an sandbox project.
The `libs/com.twilio-authenticator-1.2.9.jar` file is the raw `classes.jar` file found inside [https://repo1.maven.org/maven2/com/twilio/authenticator/1.2.9/authenticator-1.2.9.aar].
As such it includes no consumer `proguard.txt` from the AAR file. Nor does this example repository have any rules inside its `proguard-rules.pro`.

Building with

```
./gradlew app:assembleRelease
```

Then examining some relevant parts of the map file:

```
grep "^com.twilio" app/build/outputs/mapping/release/mapping.txt
```

The first few classes look obfuscated normally:

```
com.twilio.auth.TwilioAuth -> a.a:
com.twilio.auth.a -> a.b:
com.twilio.auth.internal.a -> b.a:
com.twilio.auth.internal.a.b.b -> c.a:
```

However, this package name is for some reason not obfuscated, despite all classes inside it being obfuscated:

```
com.twilio.auth.internal.authy.api.RegistrationApi -> com.twilio.auth.internal.authy.api.a:
com.twilio.auth.internal.authy.api.RegistrationApi$a -> com.twilio.auth.internal.authy.api.a$a:
com.twilio.auth.internal.authy.api.SdkApi -> com.twilio.auth.internal.authy.api.b:
com.twilio.auth.internal.authy.api.SdkApi$a -> com.twilio.auth.internal.authy.api.b$a:
com.twilio.auth.internal.authy.api.a -> com.twilio.auth.internal.authy.api.c:
com.twilio.auth.internal.authy.api.b -> com.twilio.auth.internal.authy.api.d:
com.twilio.auth.internal.authy.api.c -> com.twilio.auth.internal.authy.api.e:
com.twilio.auth.internal.authy.api.h -> com.twilio.auth.internal.authy.api.g:
com.twilio.auth.internal.authy.api.i -> com.twilio.auth.internal.authy.api.h:
com.twilio.auth.internal.authy.api.j -> com.twilio.auth.internal.authy.api.i:
```

The behaviour I expect is that since there is no unobfuscated class name inside the `com.twilio.auth.internal.authy.api` package, that package name ought to be eligible for obfuscation as well.

To compare with R8's behaviour before package flattening was introduced, 
if we now declare an older version of R8 in `build.gradle`:

```
dependencies {
        classpath "com.android.tools:r8:3.0.25-dev"  // This has to be before com.android.tools.build:gradle
        classpath "com.android.tools.build:gradle:7.0.0-rc01"
}
```

Running again:

```
./gradlew app:assembleRelease
grep "^com.twilio" app/build/outputs/mapping/release/mapping.txt
```

Now all the mappings look properly obfuscated (albeit without package flattening):

```
com.twilio.auth.TwilioAuth -> a.a.a.a:
com.twilio.auth.a -> a.a.a.b:
com.twilio.auth.internal.a -> a.a.a.c.b:
com.twilio.auth.internal.a.a -> a.a.a.c.a.a:
com.twilio.auth.internal.a.b.b -> a.a.a.c.a.b.a:
com.twilio.auth.internal.authy.api.RegistrationApi -> a.a.a.c.c.a.a:
com.twilio.auth.internal.authy.api.RegistrationApi$a -> a.a.a.c.c.a.a$a:
etc
```

# Footnote

One thing I notice is that this Twilio package has been partially obfuscated already, there is another class `com.twilio.auth.internal.authy.api.f` not in the map file that is inside the APK.
Has it perhaps by chance remapped class f -> f, then concluded that the class was "kept", and therefore needed to preserve the complete package name?

However, for reasons I can't yet explain, in our main app build the problem package is `com.twilio.auth.external` not `com.twilio.auth.internal`, inside that there are no already obfuscated class names, and yet the issue with unecessarily unobfuscated package names persists.
