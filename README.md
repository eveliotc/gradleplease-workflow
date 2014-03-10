Gradle Please Workflow for Alfred 2
===================================

![Gradle Android icon](icon.png)

- Do you love [Alfred](http://www.alfredapp.com/)?
- Do you use [gradle](http://www.gradle.org/)?
- Have you used [Gradle Please](http://gradleplease.appspot.com/)?

Well if you answered yes! yes! yes! this workflow is for you!

![Gradle Please Workflow demo](demo.gif)

Roadmap
=======
- Allow overrides/fuzzy search to provide better results (e.g. gcm -> play services, play services -> play-services, etc.)
- Performance improvements (local and central to use cache & async)
- TODOs
- Fix bugs
- idunnolol

Troubleshooting
===============
#####I don't get any results for `support-v4` or `play-services`.
  - Make sure you have `ANDROID_HOME` enviroment variable defined pointing to your android sdk, e.g. execute `echo $ANDROID_HOME` should give you a similar output to<br/>![http://i.imgur.com/dGcRde2.png](http://i.imgur.com/dGcRde2.png)
  - Make sure you have Google and support local repositories installed<br/>![http://i.imgur.com/42fhvYR.png](http://i.imgur.com/42fhvYR.png)
  - Gradle Please uses `ANDROID_HOME` to figure out your local artifacts
  - Finally if the above is in place and somehow workflow is still unable to resolve it you could edit it and add it manually e.g.
```
  export ANDROID_HOME="YOUR_PATH_HERE"
  python gp.py {query}
```
![http://i.imgur.com/gcCvSqt.png](http://i.imgur.com/gcCvSqt.png)
