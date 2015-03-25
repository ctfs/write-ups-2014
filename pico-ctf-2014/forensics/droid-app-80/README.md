# Pico CTF 2014 : Droid App

**Category:** Forensics
**Points:** 80
**Description:**

>An Android application was released for the toaster bots, but it seems like this one is some sort of debug version. Can you discover the presence of any debug information being stored, so we can plug this?
You can download the apk here.

**Hint:**
>Android apk files are notoriously easy to decompile. We heard there are even online services that does this automatically nowadays.

## Write-up

We decompile the apk using [jadx](https://github.com/skylot/jadx) and recursively `grep` the output to find any debug information:

```
$ jadx -x ToasterBot.apk 
INFO  - output directory: ToasterBot
INFO  - loading ...
WARN  - Indent < 0
[...]
$ grep debug -ir .
1∣09ː07∣droid-app-80▶ grep debug -ri ToasterBot
ToasterBot/android/support/v4/app/BackStackRecord.java:            if (FragmentManagerImpl.DEBUG) {
ToasterBot/android/support/v4/app/BackStackRecord.java:                    if (FragmentManagerImpl.DEBUG) {
[...]
ToasterBot/android/support/v7/internal/widget/ListPopupWindow.java:        int maxHeight = getMaxAvailableHeight(getAnchorView(), this.mDropDownVerticalOffset, this.mPopup.getInputMethodMode() == 2 ? true : DEBUG);
ToasterBot/picoapp453/picoctf/com/picoapp/BuildConfig.java:    public static final boolean DEBUG = false;
ToasterBot/picoapp453/picoctf/com/picoapp/ToasterActivity.java:        Log.d("Debug tag", this.mystery);
```

The last `Log` function call seems promising, lets try to find mystery:

```bash
$ grep mystery -ri ToasterBot
ToasterBot/picoapp453/picoctf/com/picoapp/ToasterActivity.java:    String mystery;
ToasterBot/picoapp453/picoctf/com/picoapp/ToasterActivity.java:        this.mystery = new String(new char[]{'f', 'l', 'a', 'g', ' ', 'i', 's', ':', ' ', 'w', 'h', 'a', 't', '_', 'd', 'o', 'e', 's', '_', 't', 'h', 'e', '_', 'l', 'o', 'g', 'c', 'a', 't', '_', 's', 'a', 'y'});
ToasterBot/picoapp453/picoctf/com/picoapp/ToasterActivity.java:        Log.d("Debug tag", this.mystery);
```

The flag is `what_does_the_logchat_say`.

## Other write-ups and resources

* <https://ctf-team.vulnhub.com/picoctf-2014-droidapp/>
