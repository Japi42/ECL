///////////////////////////////////////////////////
//
// Attract-Mode Frontend - ECL plugin
//
///////////////////////////////////////////////////
//
// Define the user-configurable options:
//
class UserConfig </ help="This plugin updates the control labels." /> {

	</ label="Command", help="Path to ecl.py", order=1 />
	command="/home/pi/ECL/emu-control-labels/ecl.py";

	</ label="Config", help="Path to ECL config file", order=2 />
	config="/home/pi/ECL/ecl-config.xml";

	</ label="Remote Host", help="Remote ECL hostname", order=3 />
	remotehost="";
}

class ECL
{
	config = null;

	constructor()
	{
		config = fe.get_config();
		fe.add_transition_callback( this, "on_transition" );
	}

	function build_command_opts()
	{
		local command_opts = "";
                command_opts = command_opts + "-c " + config["config"];
		if(config["remotehost"] != "") {
			command_opts = command_opts + " -r" + config["remotehost"]
		}

		return command_opts;
	}

	function on_transition( ttype, var, ttime )
	{

// Startup of a game

		if ( ttype == Transition.ToGame )
		{
			fe.plugin_command( config["command"],
			  build_command_opts() + " -e " + fe.game_info(Info.Emulator) + " -g " + fe.game_info(Info.Name));
		}

// Startup or transition back to Attract Mode.
// This should be updated to optionally display the control labels for Attract Mode
// instead of the currently selected game.  

		if ( ttype == Transition.EndNavigation ||
                     ttype == Transition.StartLayout)
		{
			fe.plugin_command( config["command"],
			  build_command_opts() + " -e " + fe.game_info(Info.Emulator) + " -g " + fe.game_info(Info.Name));
		}

		return false; // must return false
	}
}

fe.plugin[ "ECL" ] <- ECL();

