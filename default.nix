with import <nixpkgs> {};

stdenv.mkDerivation rec {
	name = "env-testday-analyst";
	env = buildEnv { name = name; paths = buildInputs; };
	buildInputs = [
		python
		pythonPackages.faker	
    pythonPackages.arrow
	];
}
