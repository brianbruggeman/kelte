from kelte import api

# Note: kelte.vendored.click does not appear to work with
#       pyinstaller on windows, so we use the api directly, which means
#       we lose some capability.  However, we can still run within a
#       virtualenvironment if we need to debug.  Alternatively, we can
#       externalize specific settings and use those if we needed
#       in-field debugging

api.main()
