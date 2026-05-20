{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  name = "his-project-shell";

  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.streamlit
    pkgs.python311Packages.pandas
    pkgs.python311Packages.numpy
    pkgs.python311Packages.plotly
    pkgs.python311Packages.altair
    pkgs.python311Packages.python-dotenv
    pkgs.python311Packages.python-dateutil
    pkgs.python311Packages.requests
    pkgs.python311Packages.click
    pkgs.python311Packages.bcrypt

    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
    pkgs.openssl
    pkgs.libyaml
    pkgs.pkgConfig
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=$(nix-build '<nixpkgs>' -A gcc.cc.lib)/lib:$LD_LIBRARY_PATH

    if [ -d ".venv" ]; then
      source .venv/bin/activate
    fi

    echo "🏥 Hospital Information System Environment Loaded (Python 3.11)"
    echo "Run 'streamlit run app.py' to start the application."
  '';
}
