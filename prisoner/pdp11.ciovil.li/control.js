var control = (function() {
	function do_nothing() {};

	var terminal;

	var debug = {
		init: do_nothing,
		write_status: do_nothing,
		write: do_nothing,
		clear: do_nothing
	};

	function init(term, dbg)
	{
		terminal = term;

		if(dbg) {
			dbg.init();
			debug = dbg;
		}

		pdp11.init([time,kl11,rk05,pc11], debug);

		var paused = false;

		window.onblur = function() {
			/*
			if(pdp11.running()) {
				pdp11.stop();
				paused = true;
				debug.write("paused on blur\n");
			}
			*/
		};

		window.onfocus = function() {
			if(paused) {
				paused = false;
				debug.write("resuming after pause\n");
				pdp11.run();
			}
		};
	}

	function reinstall()
	{
		if(confirm("Do you want to rebuild the system from a clean image?")) {
			pdp11.stop();
			rk05.reimage();
			terminal.clear();
			pdp11.reset();
		}
	}

	function reset()
	{
		pdp11.stop();
		terminal.clear();
		pdp11.reset();
	}

	return {
		init: init,
		reset: reset,
		reinstall: reinstall,
		run: pdp11.run,
		stop: pdp11.stop
	};
})();
