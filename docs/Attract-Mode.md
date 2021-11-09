
## Using ECL with Attract Mode

To use ECL with Attract Mode, copy the plugin (extras/ECL.nut) into your attract mode plugins folder (~/.attract/plugins).  

Update your attract mode configuration file (~/.attract/attract.cfg) with the following section to enable the plugin and set the options:

```
plugin	ECL
	enabled              yes
	param                command /home/pi/ECL/emu-control-labels/ecl.py
	param                config /home/pi/ECL/ecl-config-luma.xml
	param                remotehost japi-ecl-pi1
```

"command" is the full path to the ecl.py script.  
"config" is the full path toy your ECL configuration file.
"remotehost" is the hostname or IP address of a remote ECL instance, if you have ECL running in listen-mode on another host (pi zero) controlling your displays.  If you don't have a remote host then leave blank.

You can also set these options via the Attract Mode settings interface.

Once configured, when you select a game in Attract Mode the controls will update with the appropriate labels.  The plugin passes in the emulator and the romname.  You should define emulators in your ecl-config.xml with IDs that match the emulators defined in attract mode.  

