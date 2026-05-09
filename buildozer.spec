[app]

# (Data from your project requirements)
title = Phish
package.name = phish
package.domain = org.university.project
# ADD THIS LINE
version = 1.0

# Include all necessary files and folders from your directory
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,pkl,db
source.include_patterns = saved_model/*, datasets/*

# Critical dependencies for your ML models
requirements = python3,kivy,scikit-learn,pandas,joblib,numpy

# Android specific settings
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Permissions for sophisticated detection
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE